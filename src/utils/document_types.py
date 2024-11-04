from enum import Enum
from typing import Callable, List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
import re


class DocumentType(Enum):
    DRIVERS_LICENSE = "drivers_license"
    PASSPORT = "passport"
    UNKNOWN = "unknown"


@dataclass
class DocumentField:
    name: str
    patterns: List[str]
    preprocessing_func: Optional[Callable] = None
    validation_func: Optional[Callable] = None
    required: bool = True


class DocumentTemplate:
    def __init__(self, doc_type: DocumentType, fields: Dict[str, DocumentField]):
        self.doc_type = doc_type
        self.fields = fields
