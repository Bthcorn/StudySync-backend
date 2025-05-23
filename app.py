from fastapi import FastAPI
from routes.main import api_router
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(
    title="StudySync API",
    description="API for StudySync",
    version="0.1.0",
)


@app.get("/")
async def root():
    return {"message": "Hello World Test"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
