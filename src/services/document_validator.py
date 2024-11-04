import re
from typing import Dict, Any, List, Optional
import logging

from utils.document_templates import DocumentTemplates
from utils.document_types import DocumentField, DocumentType

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DocumentValidator:
    def __init__(self):
        self.templates = [
            DocumentTemplates.get_drivers_license_template(),
            DocumentTemplates.get_passport_template(),
        ]

    def _preprocess_text(self, text: str) -> str:

        text = text.upper()
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def _extract_field(self, text: str, field: DocumentField) -> Optional[str]:

        for pattern in field.patterns:
            match = re.search(pattern, text, re.MULTILINE | re.IGNORECASE)
            if match:
                value = match.group(1)
                if field.preprocessing_func:
                    value = field.preprocessing_func(value)
                if field.validation_func and not field.validation_func(value):
                    continue
                return value
        return None

    def _identify_document_type(self, text: str) -> DocumentType:

        text = text.upper()

        dl_indicators = ["DRIVER", "LICENSE", "DL", "OPERATOR"]
        passport_indicators = ["PASSPORT", "NATIONALITY", "ISSUING COUNTRY"]

        dl_score = sum(1 for indicator in dl_indicators if indicator in text)
        passport_score = sum(
            1 for indicator in passport_indicators if indicator in text
        )

        if dl_score > passport_score:
            return DocumentType.DRIVERS_LICENSE
        elif passport_score > dl_score:
            return DocumentType.PASSPORT
        return DocumentType.UNKNOWN

    def validate_document_details(self, extracted_text: str) -> Dict[str, Any]:

        try:
            cleaned_text = self._preprocess_text(extracted_text)
            doc_type = self._identify_document_type(cleaned_text)

            if doc_type == DocumentType.UNKNOWN:
                raise ValueError("Unable to determine document type")

            template = next(t for t in self.templates if t.doc_type == doc_type)

            results = {"document_type": doc_type.value, "fields": {}}

            missing_required_fields = []

            for field_name, field in template.fields.items():
                value = self._extract_field(cleaned_text, field)
                if value:
                    results["fields"][field_name] = value
                elif field.required:
                    missing_required_fields.append(field_name)

            if missing_required_fields:
                raise ValueError(
                    f"Missing required fields: {', '.join(missing_required_fields)}"
                )

            return results

        except Exception as e:
            logger.error(f"Document validation failed: {str(e)}")
            raise ValueError(f"Document validation failed: {str(e)}")
