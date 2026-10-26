import datetime
from typing import List, Dict
from src.schemas import MultimodalReportRequest, RadiologicalFinding, StructuredRadiologyReport

class MultimodalReportEngine:
    """
    Motor multimodal de síntese de laudos radiológicos (Visão + Linguagem).
    """

    @staticmethod
    def generate_report(request: MultimodalReportRequest) -> StructuredRadiologyReport:
        features = request.visual_features_intensity
        findings_list: List[RadiologicalFinding] = []
        radlex_codes: List[str] = []
        findings_sentences: List[str] = []
        impression_points: List[str] = []

        # 1. Avaliação de Opacidades / Consolidação (Pneumonia)
        consolidation_score = features.get("consolidation", 0.05)
        if consolidation_score >= 0.70:
            findings_list.append(RadiologicalFinding(
                finding_name="Consolidação Pulmonar",
                confidence=round(consolidation_score, 3),
                anatomical_location="Lobo inferior direito",
                severity="SEVERE"
            ))
            radlex_codes.append("RID4326") # Lung consolidation
            findings_sentences.append("Consolidação pulmonar com opacidade alveolar confluente e broncogramas aéreos evidente no lobo inferior direito, compatível com processo infeccioso bacteriano/pneumonia lobar.")
            impression_points.append("Consolidação no lobo inferior direito sugestiva de pneumonia.")
        elif consolidation_score >= 0.35:
            findings_list.append(RadiologicalFinding(
                finding_name="Infiltrado Pulmonar Leve",
                confidence=round(consolidation_score, 3),
                anatomical_location="Bases pulmonares",
                severity="MILD"
            ))
            findings_sentences.append("Tênues opacidades reticulares bibasais sem caracterizar franca consolidação.")
        else:
            findings_sentences.append("Campos pleuropulmonares transparentes, sem evidência de opacidades focais ou consolidativas.")

        # 2. Avaliação de Derrame Pleural
        effusion_score = features.get("pleural_effusion", 0.05)
        if effusion_score >= 0.60:
            findings_list.append(RadiologicalFinding(
                finding_name="Derrame Pleural",
                confidence=round(effusion_score, 3),
                anatomical_location="Seio costofrênico direito",
                severity="MODERATE"
            ))
            radlex_codes.append("RID4896")
            findings_sentences.append("Velamento do seio costofrênico direito indicativo de derrame pleural laminar a moderado.")
            impression_points.append("Derrame pleural à direita associado.")
        else:
            findings_sentences.append("Seios costofrênicos e cardiofrênicos livres.")

        # 3. Avaliação de Cardiomegalia / Silhueta Cardíaca
        cardiomegaly_score = features.get("cardiomegaly", 0.10)
        if cardiomegaly_score >= 0.65:
            findings_list.append(RadiologicalFinding(
                finding_name="Cardiomegalia",
                confidence=round(cardiomegaly_score, 3),
                anatomical_location="Silhueta cardíaca",
                severity="MODERATE"
            ))
            radlex_codes.append("RID3457")
            findings_sentences.append("Aumento global da área cardíaca com índice cardiotorácico superior a 0.55.")
            impression_points.append("Cardiomegalia de grau moderado.")
        else:
            findings_sentences.append("Área cardíaca com dimensões e contornos dentro dos limites da normalidade.")

        findings_sentences.append("Estruturas ósseas da caixa torácica íntegras.")

        findings_text = " ".join(findings_sentences)
        
        if impression_points:
            impression_text = "; ".join(impression_points) + f". Correlação clínica recomendada com indicação: '{request.clinical_indication}'."
        else:
            impression_text = "Exame radiológico do tórax dentro dos padrões de normalidade para a faixa etária."

        # Triagem de urgência
        if consolidation_score >= 0.85 or effusion_score >= 0.80:
            urgency = "CRITICAL_STAT"
        elif consolidation_score >= 0.60 or cardiomegaly_score >= 0.70:
            urgency = "PRIORITY"
        else:
            urgency = "ROUTINE"

        return StructuredRadiologyReport(
            exam_id=f"EXAM-XR-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
            patient_id=request.patient_id,
            timestamp=datetime.datetime.now().isoformat(),
            technique=f"Radiografia digital de tórax ({request.exam_type})",
            findings_text=findings_text,
            impression_text=impression_text,
            key_findings=findings_list,
            radlex_codes=radlex_codes,
            urgency_triage=urgency
        )
