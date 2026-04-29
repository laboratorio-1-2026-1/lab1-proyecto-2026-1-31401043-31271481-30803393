from typing import List, Optional

from pydantic import BaseModel


class ValidationErrorDetail(BaseModel):
    loc: List[str]
    msg: str
    type: str


class ErrorResponse(BaseModel):
    error: str
    codigoInterno: str
    mensaje: str
    timestamp: str
    validation_errors: Optional[List[ValidationErrorDetail]] = None
