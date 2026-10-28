from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse

from routes.events import router as events_router
from routes.auth import router as auth_router

#from routes.rsvps import router as rsvps_router
#from routes.users import router as users_router
#from routes.venues import router as venues_router

app = FastAPI(title="NC Plus One")
app.include_router(events_router)
app.include_router(auth_router)

#app.include_router(rsvps_router)
#app.include_router(users_router)
#app.include_router(venues_router)

@app.exception_handler(HTTPException)
def handle_http_exception(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    formatted_errors = []
    for error in errors:
        invalid_input = error.get("input")
        formatted_errors.append({"code": "INVALID_INPUT",
                                 "message": f"Invalid input: '{invalid_input}'"})
    return JSONResponse(status_code=400, content={"error": formatted_errors})