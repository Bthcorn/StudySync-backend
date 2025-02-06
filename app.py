from fastapi import FastAPI
from routes.main import api_router

app = FastAPI(
    title="StudySync API",
    description="API for StudySync",
    version="0.1.0",
)


@app.get("/")
async def root():
    return {"message": "Hello World Test"}


app.include_router(api_router)
