from starlette.config import Config

APP_VERSION = '0.0.1'
APP_NAME = 'Captcha API'
API_PREFIX = '/api'

config = Config('../.env')

IS_DEBUG: bool = config("IS_DEBUG", cast=bool, default=False)

CAPTCHA_MODEL_1: str = config('CAPTCHA_MODEL_1')