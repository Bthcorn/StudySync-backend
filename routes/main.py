from fastapi import APIRouter

from routes import user, auth, folder, quiz, question, choice, flashcard

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(user.router)
api_router.include_router(folder.router)
api_router.include_router(quiz.router)
api_router.include_router(question.router)
api_router.include_router(choice.router)
api_router.include_router(flashcard.router)
