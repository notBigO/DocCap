import cv2
import numpy as np
import pytesseract


def preprocess_image(image_content):
    nparr = np.frombuffer(image_content, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    return thresh


def perform_ocr(image_content):
    try:
        processed_image = preprocess_image(image_content)
        extracted_text = pytesseract.image_to_string(processed_image)
        return extracted_text
    except Exception as e:
        raise Exception(f"OCR failed: {e}")
