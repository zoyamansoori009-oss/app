from fastapi import FastAPI
from app.database import engine, Base
from app.auth_routes import router as auth_router
from app.dashboard import router as dashboard_router

app = FastAPI()

@app.get("/")
def home():
    return{"message": "FastAPI Running"}


Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(dashboard_router)