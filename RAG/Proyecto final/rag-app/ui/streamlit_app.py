"""
Interfaz Streamlit en formato chat, con top_k y filtro por documento en
la barra lateral, e histórico persistente (se guarda en Chroma vía la API,
así que sobrevive a cerrar y reabrir Streamlit).

Streamlit NUNCA habla con Chroma ni con Google AI directamente — todo
pasa por la API de FastAPI vía HTTP.

Correr con: streamlit run ui/streamlit_app.py
(la API debe estar corriendo aparte: uvicorn app.main:app --port 8000)
"""

import httpx
import streamlit as st

API_URL = "http://localhost:8000"

st.set_page_config(page_title="RAG PLD/FT", page_icon="⚖️")
st.title("Consulta normativa PLD/FT en México")


# ---------- Utilidades ----------

def api_get(path: str, timeout: float = 5.0, **kwargs):
    try:
        r = httpx.get(f"{API_URL}{path}", timeout=timeout, **kwargs)
        return r.json(), None
    except httpx.ConnectError:
        return None, "No se pudo conectar con la API. ¿Está corriendo `uvicorn app.main:app --port 8000`?"
    except Exception as e:
        return None, str(e)


def api_post(path: str, timeout: float = 30.0, **kwargs):
    try:
        r = httpx.post(f"{API_URL}{path}", timeout=timeout, **kwargs)
        return r.json(), None
    except httpx.ConnectError:
        return None, "No se pudo conectar con la API. ¿Está corriendo `uvicorn app.main:app --port 8000`?"
    except (httpx.ReadTimeout, httpx.TimeoutException):
        return None, "Google AI está tardando más de lo normal (alta demanda). Intenta de nuevo en un momento."
    except Exception as e:
        return None, str(e)


def mostrar_citas(citas: list[dict]):
    with st.expander(f"Ver {len(citas)} chunk(s) usados como evidencia"):
        for i, c in enumerate(citas, start=1):
            st.markdown(f"**[{i}] {c['source']}** (chunk {c['chunk_index']}, score {c['score']:.3f})")
            st.caption(c["text"])
            st.divider()


# ---------- Cargar histórico del servidor una sola vez por sesión ----------

if "history" not in st.session_state:
    data, _ = api_get("/history")
    st.session_state.history = data.get("history", []) if data else []


# ---------- Sidebar: estado, configuración e histórico ----------

with st.sidebar:
    st.subheader("Estado de la API")
    health, error = api_get("/health")
    if error:
        st.error(error)
    elif health and health.get("chroma_ok"):
        st.success("API y ChromaDB activos")
        st.metric("Chunks indexados", health.get("chunks_indexados", 0))
    else:
        st.warning("La API responde pero Chroma no está accesible.")
        if health:
            st.caption(health.get("error", ""))

    st.divider()
    st.subheader("Configuración de búsqueda")
    top_k = st.selectbox(
        "Chunks a recuperar por pregunta (top_k)",
        options=[1, 2, 3, 4, 5, 6, 8],
        index=2,  # 3 por defecto
    )

    fuentes_data, fuentes_conn_error = api_get("/sources", timeout=8.0)
    fuentes = fuentes_data.get("sources", []) if fuentes_data else []
    fuentes_error = fuentes_conn_error or (fuentes_data.get("error") if fuentes_data else None)
    if fuentes_error:
        st.caption(f"⚠️ No se pudo cargar la lista de documentos: {fuentes_error}")
    fuente_seleccionada = st.selectbox(
        "Buscar solo en un documento (opcional)",
        options=["Todos los documentos"] + fuentes,
    )
    source_filter = None if fuente_seleccionada == "Todos los documentos" else fuente_seleccionada

    st.divider()
    st.subheader("Histórico de preguntas")
    if not st.session_state.history:
        st.caption("Aún no has hecho ninguna pregunta.")
    else:
        for item in reversed(st.session_state.history):
            etiqueta = item["question"] if len(item["question"]) <= 40 else item["question"][:37] + "..."
            with st.expander(etiqueta):
                if item["abstained"]:
                    st.caption(f"⚠️ {item['answer']}")
                else:
                    st.caption(item["answer"])


# ---------- Sección 1: cargar documentos ----------

st.header("1. Cargar documentos")

archivos = st.file_uploader(
    "Sube tus leyes u otros documentos (.txt, .md, .pdf)",
    type=["txt", "md", "pdf"],
    accept_multiple_files=True,
)

if st.button("Indexar documentos", disabled=not archivos):
    resultados = []
    barra = st.progress(0.0)
    for i, archivo in enumerate(archivos):
        files = {"file": (archivo.name, archivo.getvalue(), archivo.type or "text/plain")}
        data, error = api_post("/ingest", files=files, timeout=300.0)
        if error:
            resultados.append({"documento": archivo.name, "error": error})
        else:
            resultados.append(data)
        barra.progress((i + 1) / len(archivos))

    # Se guarda en session_state (no en una variable local) para que
    # sobreviva al st.rerun() de abajo, que es lo que hace que el
    # contador de chunks y la lista de fuentes del sidebar se actualicen
    # de inmediato, sin necesidad de F5.
    st.session_state["ultimo_ingest"] = resultados
    st.rerun()

if "ultimo_ingest" in st.session_state:
    for r in st.session_state["ultimo_ingest"]:
        if r.get("error"):
            st.error(f"{r['documento']}: {r['error']}")
        else:
            st.success(f"{r['documento']}: {r['chunks_indexados']} chunks indexados")


# ---------- Sección 2: preguntas en formato chat ----------

st.header("2. Hacer preguntas")

if health and health.get("chunks_indexados", 0) == 0:
    st.info("Todavía no hay documentos indexados. Sube al menos uno arriba antes de preguntar.")

# Muestra el historial de la conversación ya ocurrida
for item in st.session_state.history:
    with st.chat_message("user"):
        st.markdown(item["question"])
    with st.chat_message("assistant"):
        if item["abstained"]:
            st.warning(item["answer"])
        else:
            st.markdown(item["answer"])
        if item["citations"]:
            mostrar_citas(item["citations"])

# Caja de chat: al enviar, se puede preguntar de nuevo de inmediato
pregunta = st.chat_input("Escribe tu pregunta")

if pregunta:
    with st.chat_message("user"):
        st.markdown(pregunta)

    with st.chat_message("assistant"):
        with st.spinner("Buscando y generando respuesta... Esto puede tardar unos segundos."):
            payload = {"question": pregunta, "top_k": top_k}
            if source_filter:
                payload["source"] = source_filter
            data, error = api_post("/query", json=payload, timeout=90.0)

        if error:
            st.error(error)
            respuesta, abstained, citas = f"[error de conexión] {error}", True, []
        else:
            respuesta = data["answer"]
            abstained = data.get("abstained", False)
            citas = data.get("citations", [])
            if abstained:
                st.warning(respuesta)
            else:
                st.markdown(respuesta)
            if citas:
                mostrar_citas(citas)

    # La API ya guardó esta pregunta en el histórico persistente (Chroma);
    # aquí solo se refleja en la sesión actual para no tener que recargar.
    st.session_state.history.append(
        {"question": pregunta, "answer": respuesta, "citations": citas, "abstained": abstained}
    )