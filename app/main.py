from fastapi import FastAPI
import uvicorn

from app.routes.predictions import router as predictions_router

app = FastAPI(
    title="Sports AI Prediction API",
    description="Improved sports prediction API with team-strength scoring and authenticated endpoints.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.include_router(predictions_router)


@app.get("/", tags=["health"])
def home():
    return {"status": "ok", "message": "Sports AI Prediction API is running"}


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


