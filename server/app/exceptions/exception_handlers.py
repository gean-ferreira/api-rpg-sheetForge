from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def validation_exception_handler(request, exc: RequestValidationError):
    errors = [{"message": err["msg"], "field": err["loc"][-1]} for err in exc.errors()]
    return JSONResponse(
        status_code=422,
        content={"detail": "Houve um erro de validação dos dados", "errors": errors},
    )
