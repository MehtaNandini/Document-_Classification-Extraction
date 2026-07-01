from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Document Classification & Extraction API"
    debug: bool = True
    classification_model_name: str = "facebook/bart-large-mnli"
    ocr_engine: str = "pytesseract"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
