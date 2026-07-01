from fastapi import FastAPI
from app.api.routes import router
from app.core.config import settings
from app.classification.document_classifier import get_classifier

app = FastAPI(
    title=settings.app_name,
    description="API for Document Classification & Extraction using OCR and NLP",
    version="1.0.0"
)

app.include_router(router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    # Pre-load the classifier model to avoid delay on first request
    get_classifier()

@app.get("/health")
def health_check():
    return {"status": "ok", "app_name": settings.app_name}
