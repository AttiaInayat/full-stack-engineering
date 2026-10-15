from fastapi import FastAPI

from production.app.api.routes.chat import router as chat_router


app = FastAPI(
    title="LangGraph AI API",
    description="Production-style LangGraph API",
    version="1.0.0"
)


app.include_router(chat_router)