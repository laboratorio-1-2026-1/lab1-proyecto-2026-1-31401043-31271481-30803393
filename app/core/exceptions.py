from datetime import datetime, timezone
from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.errors import AppException
from app.schemas.error import ErrorResponse, ValidationErrorDetail


def setup_exception_handlers(app: FastAPI):
    #  Exception handlers, se utilizan para manejar las excepciones en la app y devolver respuestas JSON con un formato consistente.
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        try:
            error_phrase = HTTPStatus(exc.status_code).phrase
        except ValueError:
            error_phrase = "Error"
            
        error_response = ErrorResponse(
            error=error_phrase,
            codigoInterno=exc.error_code,
            mensaje=exc.detail,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        return JSONResponse(status_code=exc.status_code, content=error_response.model_dump(exclude_none=True))

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        # Para cada error de validación, extraemos la ubicación, el mensaje y el tipo, y los agregamos a una lista de detalles de validación.
        details = []
        for error in exc.errors():
            details.append(
                ValidationErrorDetail(
                    loc=[str(loc_item) for loc_item in error.get("loc", [])], msg=error.get("msg", ""), type=error.get("type", "")
                )
            )

        error_response = ErrorResponse(
            error="Unprocessable Entity",
            codigoInterno="VALIDATION_ERROR",
            mensaje="The request contains invalid data.",
            timestamp=datetime.now(timezone.utc).isoformat(),
            validation_errors=details,
        )
        return JSONResponse(status_code=422, content=error_response.model_dump(exclude_none=True))

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        # Obtenemos la frase de error correspondiente al status code
        try:
            error_phrase = HTTPStatus(exc.status_code).phrase
        except ValueError:
            error_phrase = "Error"
            
        error_response = ErrorResponse(
            error=error_phrase,
            codigoInterno="HTTP_ERROR",
            mensaje=str(exc.detail),
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        return JSONResponse(status_code=exc.status_code, content=error_response.model_dump(exclude_none=True))

    @app.exception_handler(IntegrityError)
    async def sqlalchemy_integrity_error_handler(request: Request, exc: IntegrityError):
        # Obtenemos la frase de error correspondiente al status code
        msg = str(exc.orig).lower()
        detail = "Database integrity error."
        status_code = 400
        error_code = "DATABASE_INTEGRITY_ERROR"

        if "unique constraint" in msg or "duplicate key" in msg:
            detail = "The resource already exists or violates uniqueness constraints."
            status_code = 409
            error_code = "UNIQUE_CONSTRAINT_VIOLATION"
        elif "foreign key constraint" in msg or "violates foreign key" in msg:
            detail = "A referenced resource does not exist (invalid foreign key)."
            status_code = 400
            error_code = "INVALID_FOREIGN_KEY"

        try:
            error_phrase = HTTPStatus(status_code).phrase
        except ValueError:
            error_phrase = "Error"

        error_response = ErrorResponse(
            error=error_phrase,
            codigoInterno=error_code,
            mensaje=detail,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

        return JSONResponse(status_code=status_code, content=error_response.model_dump(exclude_none=True))
