class AppException(Exception):
    """Es la base para las excepciones personalizadas."""
    def __init__(self, detail: str, error_code: str, status_code: int = 400):
        self.detail = detail
        self.error_code = error_code
        self.status_code = status_code
        super().__init__(self.detail)


class NotFoundException(AppException):
    # herada de AppException y establece un código de estado 404 por defecto, recurso no encontrado
    def __init__(self, detail: str, error_code: str = "NOT_FOUND"):
        super().__init__(detail=detail, error_code=error_code, status_code=404)


class BusinessRuleException(AppException):
    # herada de AppException y establece un código de estado 400 por defecto, reglas del negocio violadas
    def __init__(self, detail: str, error_code: str = "BUSINESS_RULE_VIOLATION"):
        super().__init__(detail=detail, error_code=error_code, status_code=400)


class UnauthorizedException(AppException):
    # herada de AppException y establece un código de estado 401 por defecto, se puede usar para errores de autenticación
    def __init__(self, detail: str, error_code: str = "UNAUTHORIZED"):
        super().__init__(detail=detail, error_code=error_code, status_code=401)
