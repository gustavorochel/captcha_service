from pydantic import BaseModel

class PredictionResult(BaseModel):
    captcha_value: str
