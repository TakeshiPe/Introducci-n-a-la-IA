#Traduce errores técnicos (de Google AI o de red) a mensajes claros para el usuario final.

def humanize_error(e: Exception) -> str:
    texto = str(e)

    if "429" in texto or "RESOURCE_EXHAUSTED" in texto:
        return (
            "Se alcanzó el límite de peticiones a Google AI (cuota del plan "
            "gratuito). Espera un poco antes de volver a preguntar."
        )
    if "503" in texto or "UNAVAILABLE" in texto or "overloaded" in texto.lower():
        return (
            "Los servidores de Google AI están saturados en este momento. "
            "Intenta de nuevo en uno o dos minutos."
        )
    if "DEADLINE_EXCEEDED" in texto or "timed out" in texto.lower() or "timeout" in texto.lower():
        return (
            "Google AI tardó demasiado en responder (probablemente por alta "
            "demanda). Intenta de nuevo."
        )
    if "API_KEY" in texto or "PERMISSION_DENIED" in texto or "401" in texto:
        return "Hay un problema con la clave de Google AI (GOOGLE_API_KEY). Revisa el archivo .env."

    # Error no reconocido: se muestra tal cual, pero con contexto.
    return f"Ocurrió un error inesperado al consultar con Google AI: {texto}"