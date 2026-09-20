from fastapi import FastAPI

from app.api.routers.tours import router

app = FastAPI()
app.include_router(router)








