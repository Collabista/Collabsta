from fastapi import FastAPI

from app.core.config import settings

app = FastAPI(
    title="Collabsta API",
    version="0.1.0",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
