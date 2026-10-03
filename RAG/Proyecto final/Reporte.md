# Proyecto final — Sistema RAG

Para el desarrollo del proyecto final que utilice un sistema RAG (generación aumentada por recuperación), se desarrolló un chatbot para que el usuario pueda consultar diferentes documentos jurídicos y normativos en materia de Prevención de Lavado de Dinero y Financiamiento al Terrorismo (PLD/FT).

Para esto, el dominio del chatbot consiste en los siguientes documentos:

* Disposiciones de carácter general a que se refiere el artículo 115 de la Ley de Instituciones de Crédito (_DisposicionesCG.pdf_)
* Ley Federal para la Prevención e Identificación de Operaciones con Recursos de Procedencia Ilícita (_LFPIORPI.pdf_)
* Ley de Instituciones de Crédito (_LIC.pdf_)
* Reglas de Carácter General a que se refiere la LFPIORPI (_RCG\_LFPIORPI.pdf_)
* Reglamento de la LFPIORPI (_Reg\_LFPIORPI.pdf_)

Al indexar los documentos en formato PDF dentro de la aplicación, se obtienen 2305 chunks, los cuales respetan la estructura del texto, para esto, los documentos se dividen por párrafos (líneas en blanco o saltos de linea); también dentro de cada párrafo se divide por oraciones para que ninguna operación se corte por la mitad; las oraciones consecutivas son agrupadas hasta alcanzar un tamaño de chunk de 200 palabras. La superposición (_overlap_) entre chunks consecutivos se hace con las 2 últimas oraciones del chunk anterior, no con palabras sueltas.

Para la representación del texto en forma de vector (_embedding_), inicialmente se utilizó el modelo `gemini-embedding-001` el cual es el modelo vigente, sin embargo, dado que los documentos indexados son de gran tamaño, al utilizar una `GOOGLE-API-KEY` ésta sólo permitía 100 RPM (peticiones por minuto), las cuales alcanzaba inmediatamente y, en consecuencia, no se podía utilizar de manera correcta. Por esto, se incluyó un modelo de `sentence-transformers` multilingüe, el cual funciona bien en español. 

Para generar le respuesta, se utiliza Gemini (`genai`) mediante el modelo `gemini-flash-latest`, el cual mantiene apuntando al Flash estable vigente, para no tener que actualizar el nombre del modelo manualmente cada vez que se publica una nueva versión. Se manejan dos capas de abstención:
1. Por score: si el mejor chunk recuperado tiene un score menor a 0.5, no se llama a Gemini, pues no hay evidencia parecida.
2. Por el modelo: aunque el score pase el umbral, los chunks podrían no contener la verdadera respuesta, por lo que en el prompt se le instruye a Gemini que en esos casos responda con la respuesta de no evidencia. Si esto sucede, el código detecta esa frase para marcar `abstained=true`. 

Adicionalmente, se utiliza `chroma` para manejar información persistente en disco; guarda la lista de chunks junto con sus vectores. El ID de cada chunk se construye con `source` + `index` para que sea estable y legible. Adicionalmente busca los `top-k`chunks más cercanos al vector de la pregunta. De igual manera, se puede filtrar por `source`, buscando sólo en ese documento. Devuelve una lista de diccionarios: `{text, source, chunk_index, score}`

En resumen, se trabaja con lo siguiente:

| Modelo | ¿Qué hace? |
| --- | --- |
| `google-ai` | Genera la respuesta final para el usuario |
| `sentence-transformers` | Representa los textos de manera numérica |
| `chroma` | Almacena, indexa y busca representaciones numéricas de datos |

Para probar la aplicación se realizan tres preguntas cuya respuesta pueda encontrarse dentro del _corpus_ proporcionado y una pregunta fuera del rango. Las cuales son:

* ¿Quién es el beneficiario controlador de una persona moral?
* ¿Cuántas veces al año debe actualizarse el perfil transaccional de un cliente?
* ¿De cuánto debe ser la comercialización de vehículos nuevos o usados para ser considerada como actividad vulnerable?
* ¿Cuáles son los requisitos para tramitar el divorcio en México? (Pregunta fuera de rango)

En las primeras tres preguntas, la respuesta corresponde a lo estipulado dentro de la documentación proporcionada, mientras que, en la última pregunta, al no contar con información que respalde la respuesta, responde lo siguiente:

```
No cuento con evidencia suficiente en el corpus para responder esta pregunta.
```

Es decir, funciona de acuerdo con lo esperado.

Las evidencias (capturas de pantalla de las preguntas y JSON de stramlit) se encuentran en el repositorio.