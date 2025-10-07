from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import settings
from app.router import router as chat_router

app = FastAPI(title=settings.app_name, version=settings.version, docs_url="/swagger", redoc_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.allow_origins.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)

@app.get("/health", tags=["health"])
def health():
    return {"status":"ok","version":settings.version}

app.mount("/static", StaticFiles(directory="app/static", html=True), name="static")
