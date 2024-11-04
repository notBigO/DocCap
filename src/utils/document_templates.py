from datetime import datetime
import re
from utils.document_types import DocumentField, DocumentTemplate, DocumentType


class DocumentTemplates:
    @staticmethod
    def get_drivers_license_template() -> DocumentTemplate:
        return DocumentTemplate(
            DocumentType.DRIVERS_LICENSE,
            {
                "name": DocumentField(
                    name="name",
                    patterns=[
                        r"^([A-Z][a-z]+),\s*([A-Z][a-z]+)",
                        r"NAME:\s*([A-Z][a-z]+)\s+([A-Z][a-z]+)",
                        r"([A-Z][a-z]+)\s+([A-Z][a-z]+)\s+DOB",
                    ],
                    preprocessing_func=lambda x: x.strip().upper(),
                    validation_func=lambda x: len(x.split()) >= 2,
                ),
                "document_number": DocumentField(
                    name="document_number",
                    patterns=[
                        r"(\d{3}\s*\.\s*\d{4}\s*\.\s*\d{4}[A-Z])",
                        r"LIC#\s*(\w+-\w+-\w+)",
                        r"DL\s*(\w+\d+\w*)",
                    ],
                    preprocessing_func=lambda x: re.sub(r"[\s\.]", "", x),
                ),
                "expiration_date": DocumentField(
                    name="expiration_date",
                    patterns=[
                        r"EXPIRES?:?\s*(\d{2}-\d{2}-\d{4})",
                        r"EXP\.?\s*(\d{2}/\d{2}/\d{4})",
                        r"VALID THRU\s*(\d{2}/\d{2}/\d{4})",
                    ],
                    validation_func=lambda x: datetime.strptime(x, "%m-%d-%Y")
                    > datetime.now(),
                ),
                "dob": DocumentField(
                    name="dob",
                    patterns=[
                        r"DOB:?\s*(\d{2}-\d{2}-\d{4})",
                        r"BIRTH\s*DATE:?\s*(\d{2}/\d{2}/\d{4})",
                    ],
                    required=False,
                ),
            },
        )

    @staticmethod
    def get_passport_template() -> DocumentTemplate:
        return DocumentTemplate(
            DocumentType.PASSPORT,
            {
                "name": DocumentField(
                    name="name",
                    patterns=[
                        r"^([A-Z][a-z]+)\s+([A-Z][a-z]+)",
                        r"Surname:\s*([A-Z][a-z]+)\s+Given Names:\s*([A-Z][a-z]+)",
                    ],
                    preprocessing_func=lambda x: x.strip().upper(),
                ),
                "passport_number": DocumentField(
                    name="passport_number",
                    patterns=[
                        r"Passport No\.?\s*([A-Z0-9]{8,9})",
                        r"^([A-Z0-9]{9})<<",
                    ],
                ),
                "expiration_date": DocumentField(
                    name="expiration_date",
                    patterns=[
                        r"Date of expiry:?\s*(\d{2}\s*[A-Z]{3}\s*\d{4})",
                        r"EXPIRY:?\s*(\d{2}-\d{2}-\d{4})",
                    ],
                    validation_func=lambda x: datetime.strptime(x, "%d %b %Y")
                    > datetime.now(),
                ),
                "nationality": DocumentField(
                    name="nationality",
                    patterns=[
                        r"Nationality:?\s*([A-Z]{3})",
                        r"^[A-Z]{3}",
                    ],
                    required=False,
                ),
            },
        )
