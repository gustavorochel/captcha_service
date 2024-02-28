from typing import Callable
from fastapi import FastAPI
from loguru import logger
from keras.models import load_model

from app.core.config import (
    CAPTCHA_MODEL_1
)

def _load_models(app):
    logger.info('Loading models...')

    app.state.models = dict()

    app.state.models['model_1'] = {
        'model': [load_model(CAPTCHA_MODEL_1)],
        'n_digits': [5],
        'possible_digits': '0123456789',
        'n_types': 1
    }

def _startup_model(app: FastAPI) -> None:
    _load_models(app)

def _shutdown_model(app: FastAPI) -> None:
    app.state.models = None

def start_app_handler(app: FastAPI) -> Callable:
    def startup() -> None:
        logger.info("Running app start handler.")
        _startup_model(app)
    return startup

def stop_app_handler(app: FastAPI) -> Callable:
    def shutdown() -> None:
        logger.info("Running app shutdown handler.")
        _shutdown_model(app)
    return shutdown
