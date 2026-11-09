import os
import time
import logging

from collections import defaultdict, deque
from contextlib import asynccontextmanager
from logging.handlers import RotatingFileHandler
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.responses import JSONResponse

from src.api.model_service import ModelService
from src.api.schemas import PredictionRequest, PredictionResponse
from src.api.security import verify_api_key


PROJECT_ROOT = Path(__file__).resolve().parents[2]

load_dotenv(PROJECT_ROOT / ".env")

MODEL_PATH = PROJECT_ROOT / "models" / "mnist_baseline.pth"
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

RATE_LIMIT = int(os.getenv("RATE_LIMIT_REQUESTS", "60"))
RATE_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))

if RATE_LIMIT < 1 or RATE_WINDOW < 1:
    raise RuntimeError("Rate-limit configuration must be positive")


# Logging configuration
logger = logging.getLogger("mnist_api")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = RotatingFileHandler(
        LOG_DIR / "api.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=3
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)


# Model lifecycle
@asynccontextmanager
async def lifespan(app: FastAPI):

    if not MODEL_PATH.exists():
        raise RuntimeError(f"Model file not found: {MODEL_PATH}")

    app.state.model_service = ModelService(MODEL_PATH)

    logger.info("MNIST model loaded successfully")

    yield

    app.state.model_service = None
    logger.info("MNIST API shutting down")


app = FastAPI(
    title="MNIST Digit Recognition API",
    description="AI Quality Engineering - Model Prediction Service",
    version="1.0.0",
    lifespan=lifespan
)


# Simple in-memory rate limiter
request_history = defaultdict(deque)


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):

    client_ip = (
        request.client.host if request.client else "unknown"
    )

    now = time.monotonic()
    history = request_history[client_ip]

    while history and now - history[0] >= RATE_WINDOW:
        history.popleft()

    if len(history) >= RATE_LIMIT:
        logger.warning("Rate limit exceeded for client %s", client_ip)

        return JSONResponse(
            status_code=429,
            content={"detail": "Rate limit exceeded"}
        )

    history.append(now)

    return await call_next(request)


# Request logging middleware
@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):

    start_time = time.perf_counter()

    try:
        response = await call_next(request)

        elapsed_ms = (
            time.perf_counter() - start_time
        ) * 1000

        logger.info(
            "method=%s path=%s status=%s duration_ms=%.2f",
            request.method,
            request.url.path,
            response.status_code,
            elapsed_ms
        )

        response.headers["X-Process-Time-Ms"] = str(
            round(elapsed_ms, 2)
        )

        return response

    except Exception:
        logger.exception(
            "Unhandled exception for %s %s",
            request.method,
            request.url.path
        )
        raise


@app.get("/health")
async def health_check():

    return {
        "status": "UP",
        "service": "MNIST Digit Recognition API"
    }


@app.post(
    "/predict",
    response_model=PredictionResponse,
    dependencies=[Depends(verify_api_key)]
)
async def predict(
    payload: PredictionRequest,
    request: Request
):

    start_time = time.perf_counter()

    try:

        result = request.app.state.model_service.predict(
            payload.image
        )

        processing_time_ms = (
            time.perf_counter() - start_time
        ) * 1000

        logger.info(
            "prediction_completed digit=%s processing_time_ms=%.2f",
            result["predicted_digit"],
            processing_time_ms
        )

        return PredictionResponse(
            predicted_digit=result["predicted_digit"],
            confidence=result["confidence"],
            processing_time_ms=round(processing_time_ms, 4)
        )

    except Exception:
        logger.exception("Prediction failed")

        raise HTTPException(
            status_code=500,
            detail="Prediction processing failed"
        )