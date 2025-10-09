from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.router import router as chat_router

app = FastAPI(
    title="Sigorta Chatbot API",
    description="FastAPI + Gemini entegre chatbot sistemi",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)


app.mount("/", StaticFiles(directory="app/static", html=True), name="static")

@app.get("/health")
def health():
    return {"status": "ok"}
