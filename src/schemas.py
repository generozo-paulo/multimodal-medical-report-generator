from pydantic import BaseModel, Field
from typing import List, Dict, Literal

class MultimodalReportRequest(BaseModel):
    patient_id: str
    exam_type: Literal["CHEST_XRAY_PA", "CHEST_XRAY_LATERAL", "CT_CHEST"]
    clinical_indication: str = Field(min_length=5)
    visual_features_intensity: Dict[str, float]

class RadiologicalFinding(BaseModel):
    finding_name: str
    confidence: float
    anatomical_location: str
    severity: Literal["NORMAL", "MILD", "MODERATE", "SEVERE"]

class StructuredRadiologyReport(BaseModel):
    exam_id: str
    patient_id: str
    timestamp: str
    technique: str
    findings_text: str
    impression_text: str
    key_findings: List[RadiologicalFinding]
    radlex_codes: List[str]
    urgency_triage: Literal["ROUTINE", "PRIORITY", "CRITICAL_STAT"]
