from pydantic import BaseModel

class PredictionPayload(BaseModel):
    base_64_image: str
