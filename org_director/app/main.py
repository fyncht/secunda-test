from fastapi import FastAPI
from .routers import buildings, activities, organizations

app = FastAPI(title="Org Directory API", version="1.0.0")

app.include_router(buildings.router)
app.include_router(activities.router)
app.include_router(organizations.router)
