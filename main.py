from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException
from utils.exceptions import validation_exception_handler, handle_http_exception

from routes.events import router as events_router
from routes.auth import router as auth_router
from routes.users import router as user_router



app = FastAPI(title="NC Plus One")
app.include_router(events_router)
app.include_router(auth_router)
app.include_router(user_router)



app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, handle_http_exception)
