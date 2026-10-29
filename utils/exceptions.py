from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException, RequestValidationError

def handle_http_exception(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    formatted_errors = []
    for error in errors:
        loc = error.get("loc", [])
        field_name = loc[-1] if loc else "unknown field"
        error_type = error.get("type")
        if error_type == "missing":
            formatted_errors.append({
                "code": "MISSING_FIELD",
                "message": f"The '{field_name}' field is required"
            })
        else:
            invalid_input = error.get("input")
            formatted_errors.append({"code": "INVALID_INPUT",
                                 "message": f"Invalid input: '{invalid_input}'"})
    return JSONResponse(status_code=400, content={"error": formatted_errors})
