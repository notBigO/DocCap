from datetime import datetime
import re


def validate_document_details(extracted_text):
    print(extracted_text)

    name_match = re.search(
        r"^([A-Z][a-z]+),\s*([A-Z][a-z]+)", extracted_text, re.MULTILINE
    )
    name = f"{name_match.group(2)} {name_match.group(1)}" if name_match else None

    doc_number_match = re.search(
        r"(\d{3}\s*\.\s*\d{4}\s*\.\s*\d{4}[A-Z])", extracted_text
    )
    doc_number = doc_number_match.group(1) if doc_number_match else None

    if doc_number:
        doc_number = doc_number.replace(" ", "")

    date_match = re.search(r"EXPIRES:\s*(\d{2}-\d{2}-\d{4})", extracted_text)
    expiry_date_str = date_match.group(1) if date_match else None

    if not all([name, doc_number, expiry_date_str]):
        raise ValueError("Could not extract all required document details")

    try:
        return {
            "name": name,
            "document_number": doc_number,
            "expiration_date": expiry_date_str,
        }

    except ValueError as e:
        raise ValueError(f"Invalid document details: {str(e)}")
