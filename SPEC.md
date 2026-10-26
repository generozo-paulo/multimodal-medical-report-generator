# Especificação Contratual (SDD) - Multimodal Medical Report Generator

## 1. Escopo & Objetivos
Pipeline Multimodal que integra visão computacional (processamento de radiografia de tórax / exames de imagem) com geração de laudos radiológicos estruturados (**Findings** e **Impression**).
O modelo correlaciona achados visuais (consolidação pulmonar, cardiomegalia, derrame pleural) com o histórico clínico do paciente para gerar um laudo padronizado pré-preenchido para revisão médica.

## 2. Contratos de Entrada (Pydantic)

### 2.1 Requisição Multimodal (`MultimodalReportRequest`)
- `patient_id`: str
- `exam_type`: Literal["CHEST_XRAY_PA", "CHEST_XRAY_LATERAL", "CT_CHEST"]
- `clinical_indication`: str = Field(min_length=5)
- `visual_features_intensity`: Dict[str, float] # escores simulados de visão computacional (0.0 a 1.0)

## 3. Contratos de Saída (Pydantic)

### 3.1 Achado Radiológico Identificado (`RadiologicalFinding`)
- `finding_name`: str
- `confidence`: float
- `anatomical_location`: str
- `severity`: Literal["NORMAL", "MILD", "MODERATE", "SEVERE"]

### 3.2 Laudo Multimodal Estruturado (`StructuredRadiologyReport`)
- `exam_id`: str
- `timestamp`: str
- `technique`: str
- `findings_text`: str
- `impression_text`: str
- `key_findings`: List[RadiologicalFinding]
- `radlex_codes`: List[str]
- `urgency_triage`: Literal["ROUTINE", "PRIORITY", "CRITICAL_STAT"]
