from fastapi import APIRouter, File, Form
from starlette.requests import Request
from fastapi import HTTPException

from app.models.payload import PredictionPayload
from app.models.prediction import PredictionResult
from app.services.captcha_model import CaptchaModelService

import numpy as np
import cv2
import base64
from PIL import Image
import io

router = APIRouter()

@router.post(
    '/predict_captcha',
    response_model=PredictionResult,
    name='predict_captcha'
)
async def predict_captcha(
    request: Request,
    block_data: PredictionPayload = None,
) -> PredictionResult:

    im_bytes = base64.b64decode(block_data.base_64_image)

    image_from_base64 = Image.open(io.BytesIO(im_bytes)).convert('L')

    decoded_image = np.array(image_from_base64)

    captcha_detected = CaptchaModelService(
        request
    ).predict(decoded_image)

    return PredictionResult(
        captcha_value=captcha_detected
    )