from fastapi import Query

class PaginationParams:
    """Clase para manejar los parámetros de paginación comunes en las rutas que devuelven listas de recursos."""
    def __init__(
        self,
        skip: int = Query(0, ge=0, description="Número de registros a omitir"),
        limit: int = Query(100, le=1000, description="Límite de registros a devolver")
    ):
        self.skip = skip
        self.limit = limit
