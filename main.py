from fastapi import FastAPI

from routes.events import router as events_router
#from routes.rsvps import router as rsvps_router
#from routes.users import router as users_router
#from routes.venues import router as venues_router

app = FastAPI(title="NC Plus One")
app.include_router(events_router)
#app.include_router(rsvps_router)
#app.include_router(users_router)
#app.include_router(venues_router)

