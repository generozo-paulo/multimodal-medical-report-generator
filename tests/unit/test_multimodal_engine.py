import pytest
from src.schemas import MultimodalReportRequest
from src.multimodal_engine import MultimodalReportEngine

def test_multimodal_report_consolidation_and_effusion():
    req = MultimodalReportRequest(
        patient_id="PAC-TEST-PNEUMO",
        exam_type="CHEST_XRAY_PA",
        clinical_indication="Febre alta e estertores creptantes em base direita",
        visual_features_intensity={
            "consolidation": 0.88,
            "pleural_effusion": 0.70,
            "cardiomegaly": 0.10
        }
    )
    report = MultimodalReportEngine.generate_report(req)
    assert len(report.key_findings) >= 2
    assert "Consolidação" in report.findings_text
    assert "derrame pleural" in report.findings_text.lower()
    assert report.urgency_triage in ["PRIORITY", "CRITICAL_STAT"]
    assert len(report.radlex_codes) >= 2

def test_multimodal_report_normal_study():
    req = MultimodalReportRequest(
        patient_id="PAC-NORMAL",
        exam_type="CHEST_XRAY_PA",
        clinical_indication="Check-up de rotina admissional",
        visual_features_intensity={
            "consolidation": 0.05,
            "pleural_effusion": 0.02,
            "cardiomegaly": 0.10
        }
    )
    report = MultimodalReportEngine.generate_report(req)
    assert len(report.key_findings) == 0
    assert "normalidade" in report.impression_text.lower()
    assert report.urgency_triage == "ROUTINE"
