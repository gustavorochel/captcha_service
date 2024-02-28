import numpy as np
import tensorflow as tf
from fastapi import HTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
import cv2
from loguru import logger

class CaptchaModelService(object):
    def __init__(self, request):
        self.models = request.app.state.models

    def select_model(self):
        model_id = 'model_1'
        return {**{'id': model_id}, **self.models[model_id]}

    def detect_n_digits(self, image):
        def count_digits(contours_found):
            digits = list()
            for contour in contours_found:
                (x, y, w, h) = cv2.boundingRect(contour)
                if w >= 8 and (h >= 10 and h <= 25):
                    if w / h > 1:
                        half_width = int(w / 2)
                        digits.append((x, y, half_width, h))
                        digits.append((x + half_width, y, half_width, h))
                    else:
                        digits.append((x, y, w, h))
            return digits

        thresholded_image = cv2.threshold(
            image,
            0,
            255,
            cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU
        )[1]

        contours_found = cv2.findContours(
            thresholded_image.copy(),
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )[0]

        digits_found = count_digits(contours_found)

        return 0 if len(digits_found) <= 4 else 1

    def detect_captcha(self, selected_model, image):
        POSSIBLE_DIGITS = selected_model.get('possible_digits')
        INDEX = 0

        if selected_model.get('n_types') > 1:
            INDEX = self.select_submodel(selected_model.get('id'), image)

        N_DIGITS = selected_model.get('n_digits')[INDEX]

        if image is not None:
            image = image / 255.0
        else:
            return False
        
        res = np.array(selected_model.get('model')[INDEX](
            tf.convert_to_tensor(
                image[np.newaxis, :, :, np.newaxis]
            )
        ))

        result = np.reshape(res, (N_DIGITS, len(POSSIBLE_DIGITS)))
        k_index = [np.argmax(i) for i in result]

        detected_captcha = ''.join([POSSIBLE_DIGITS[k] for k in k_index])

        return detected_captcha

    def predict(self, decoded_image):
        try:
            selected_model = self.select_model()
            detected_captcha = self.detect_captcha(
                selected_model=selected_model, image=decoded_image
            )
            return detected_captcha
        except Exception:
            logger.exception('An error occured while detecting captcha')
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occured while detecting captcha"
            )
