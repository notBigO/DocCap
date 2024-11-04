from venv import logger
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

        configs = [
            "--oem 3 --psm 3",
            "--oem 3 --psm 4",
            "--oem 3 --psm 6",
        ]

        best_result = ""
        max_confidence = 0

        for config in configs:
            try:
                data = pytesseract.image_to_data(
                    processed_image, config=config, output_type=pytesseract.Output.DICT
                )

                confidences = [int(conf) for conf in data["conf"] if conf != "-1"]
                avg_confidence = (
                    sum(confidences) / len(confidences) if confidences else 0
                )

                if avg_confidence > max_confidence:
                    max_confidence = avg_confidence
                    best_result = pytesseract.image_to_string(
                        processed_image, config=config
                    )

            except Exception as e:
                logger.warning(f"OCR configuration {config} failed: {str(e)}")
                continue

        if not best_result:
            raise Exception("All OCR attempts failed")

        return best_result

    except Exception as e:
        logger.error(f"OCR processing failed: {str(e)}")
        raise Exception(f"OCR failed: {str(e)}")
