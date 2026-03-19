from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ProcessRule:
    rule_url: str


@dataclass
class ProcessCondition:
    condition_name: str


@dataclass
class ServiceData:
    process_id: str
    rules: List[ProcessRule] = field(default_factory=list)
    conditions: List[ProcessCondition] = field(default_factory=list)


@dataclass
class ExtractedPrecondition:
    text: str
    category: Optional[str] = None
    applicant_type: Optional[str] = None
    legal_reference: Optional[str] = None


@dataclass
class LLMExtractionResult:
    process_id: str
    preconditions: List[ExtractedPrecondition] = field(default_factory=list)