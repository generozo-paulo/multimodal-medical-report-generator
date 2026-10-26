import streamlit as st
import pandas as pd
from src.schemas import MultimodalReportRequest
from src.multimodal_engine import MultimodalReportEngine

st.set_page_config(
    page_title="Multimodal Medical Radiology Report Generator",
    page_icon="🩻",
    layout="wide"
)

st.title("🩻 Multimodal Medical Report Generator (Visão + LLM)")
st.markdown("""
Geração automatizada de laudos radiológicos estruturados (**Findings & Impression**) integrando extração de sinais de imagem médica e correlação com hipóteses clínicas.
""")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("⚙️ Dados do Exame & Features de Visão Computacional")
    patient_id = st.text_input("ID do Paciente", "PAC-71829")
    exam_type = st.selectbox("Incidência Radiológica", ["CHEST_XRAY_PA", "CHEST_XRAY_LATERAL", "CT_CHEST"])
    indication = st.text_input("Indicação Clínica", "Suspeita de pneumonia adquirida na comunidade com tosse produtiva e febre")

    st.markdown("### Escores de Visão Computacional (Deep Learning Heatmaps)")
    consolidation = st.slider("Confiança de Consolidação / Opacidade Pulmonar", 0.0, 1.0, 0.82, 0.02)
    effusion = st.slider("Confiança de Derrame Pleural", 0.0, 1.0, 0.65, 0.02)
    cardiomegaly = st.slider("Confiança de Cardiomegalia", 0.0, 1.0, 0.15, 0.02)

    req = MultimodalReportRequest(
        patient_id=patient_id,
        exam_type=exam_type,
        clinical_indication=indication,
        visual_features_intensity={
            "consolidation": consolidation,
            "pleural_effusion": effusion,
            "cardiomegaly": cardiomegaly
        }
    )

with col2:
    st.subheader("📑 Minuta do Laudo Radiológico Estruturado")
    report = MultimodalReportEngine.generate_report(req)

    urgency_badge = "🔴 STAT (Crítico)" if report.urgency_triage == "CRITICAL_STAT" else ("🟡 Prioritário" if report.urgency_triage == "PRIORITY" else "🟢 Rotina")
    st.metric("Triagem de Urgência", urgency_badge)

    st.markdown("#### Técnica:")
    st.write(report.technique)

    st.markdown("#### Achados Radiológicos (Findings):")
    st.info(report.findings_text)

    st.markdown("#### Conclusão / Impressão Diagnóstica (Impression):")
    st.warning(report.impression_text)

    st.markdown("#### 🎯 Tabela Estruturada de Achados:")
    findings_data = []
    for k in report.key_findings:
        findings_data.append({
            "Achado": k.finding_name,
            "Localização": k.anatomical_location,
            "Gravidade": k.severity,
            "Confiança do Modelo": f"{k.confidence:.1%}"
        })
    if findings_data:
        st.dataframe(pd.DataFrame(findings_data), use_container_width=True)
    else:
        st.success("Nenhuma alteração patológica significativa detectada nos parâmetros informados.")
