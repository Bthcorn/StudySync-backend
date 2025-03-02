from fastapi import APIRouter

from routes import user, auth, folder

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(user.router)
api_router.include_router(folder.router)
