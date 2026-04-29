import logging
import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

# Configurar logger profesional
logger = logging.getLogger("gym_api")
logger.setLevel(logging.INFO)

# Evitar duplicar handlers si se recarga la app
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "\033[90m%(asctime)s\033[0m | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def _colorear_status(status_code: int) -> str:
    """Aplica colores ANSI según el rango del status code."""
    if 200 <= status_code < 300:
        return f"\033[92m{status_code}\033[0m"   # Verde — éxito
    elif 300 <= status_code < 400:
        return f"\033[93m{status_code}\033[0m"   # Amarillo — redirección
    elif 400 <= status_code < 500:
        return f"\033[91m{status_code}\033[0m"   # Rojo — error del cliente
    elif status_code >= 500:
        return f"\033[1;91m{status_code}\033[0m" # Rojo bold — error del servidor
    return str(status_code)


def _colorear_metodo(method: str) -> str:
    """Aplica colores ANSI según el método HTTP."""
    colores = {
        "GET":    f"\033[94m{method:7s}\033[0m",   # Azul
        "POST":   f"\033[92m{method:7s}\033[0m",   # Verde
        "PATCH":  f"\033[93m{method:7s}\033[0m",   # Amarillo
        "PUT":    f"\033[93m{method:7s}\033[0m",   # Amarillo
        "DELETE": f"\033[91m{method:7s}\033[0m",   # Rojo
    }
    return colores.get(method, f"{method:7s}")


def _formatear_tiempo(segundos: float) -> str:
    """Formatea el tiempo de respuesta con color según la duración."""
    ms = segundos * 1000
    if ms < 100:
        return f"\033[92m{ms:.1f}ms\033[0m"    # Verde — rápido
    elif ms < 500:
        return f"\033[93m{ms:.1f}ms\033[0m"    # Amarillo — aceptable
    else:
        return f"\033[91m{ms:.1f}ms\033[0m"    # Rojo — lento


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Obtener IP del cliente
        client_ip = request.client.host if request.client else "Unknown"

        # Procesar la petición
        response = await call_next(request)

        # Calcular tiempo de procesamiento
        process_time = time.time() - start_time

        # Agregar header de tiempo de respuesta (útil para el frontend/debugging)
        response.headers["X-Process-Time"] = f"{process_time:.4f}s"

        # Construir log con colores
        metodo = _colorear_metodo(request.method)
        status = _colorear_status(response.status_code)
        tiempo = _formatear_tiempo(process_time)
        path = request.url.path

        # Incluir query params si existen
        if request.query_params:
            path += f"?{request.query_params}"

        log_line = f"{metodo} {status} {path} \033[90m│\033[0m {client_ip} \033[90m│\033[0m {tiempo}"

        # Elegir nivel de log según el status code
        if response.status_code >= 500:
            logger.error(log_line)
        elif response.status_code >= 400:
            logger.warning(log_line)
        else:
            logger.info(log_line)

        return response
