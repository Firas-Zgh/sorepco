import streamlit as st
import requests
import json
import pandas as pd
import time
from io import BytesIO

# ================================
# PAGE CONFIG
# ================================
st.set_page_config(
    page_title="SOREPCO Automation",
    layout="wide",
    page_icon="📄",
    initial_sidebar_state="collapsed",
)

# ================================
# STYLES (unchanged)
# ================================
# — your entire CSS block goes here, unchanged —

# ================================
# BACKEND ENDPOINTS
# ================================
SUBMIT_URL = "https://sorepco-automation.app.n8n.cloud/webhook/Zautomation"
STATUS_URL = "https://sorepco-automation.app.n8n.cloud/webhook/status"

# ================================
# HELPERS
# ================================
def submit_job(files):
    """Submit PDF(s) to WF1 and return job_id"""
    try:
        r = requests.post(SUBMIT_URL,
                          files=[("files", (f.name, f.getvalue(), "application/pdf")) for f in files],
                          timeout=60)
        r.raise_for_status()
        data = r.json()
        return data.get("job_id")
    except Exception as e:
        st.error(f"❌ Erreur d’envoi : {e}")
        return None


def poll_status(job_id, timeout=900, interval=10):
    """Poll WF3 every few seconds until job is done or timeout"""
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(STATUS_URL, params={"job_id": job_id})
            if r.status_code == 200:
                data = r.json()
                if data.get("status") in ["completed", "error"]:
                    return data
            elif r.status_code == 404:
                st.warning("⚠️ Job introuvable dans la base.")
                return None
        except Exception as e:
            st.error(f"Erreur lors de la vérification du statut : {e}")
            return None
        time.sleep(interval)
    st.warning("⏰ Délai dépassé (15 min).")
    return None

# ================================
# HERO SECTION
# ================================
st.markdown("""
<div class="hero-container">
    <div class="hero-card">
        <div class="hero-title">SOREPCO AUTOMATION</div>
        <p class="hero-subtitle">Interface nouvelle génération pour l'extraction automatique et l'attribution des codes NGP</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ================================
# UPLOAD SECTION
# ================================
st.markdown('<div class="upload-container">', unsafe_allow_html=True)
if 'uploader_key' not in st.session_state:
    st.session_state.uploader_key = 0

uploaded_files = st.file_uploader(
    "Déposez ici vos fichiers PDF",
    type=["pdf"],
    accept_multiple_files=True,
    label_visibility="collapsed",
    key=f"uploader_{st.session_state.uploader_key}"
)
st.markdown('</div>', unsafe_allow_html=True)

# ================================
# MAIN ACTION
# ================================
if uploaded_files:
    _, col2, _ = st.columns([1, 1, 1])
    with col2:
        start_clicked = st.button("🚀 START", key="start_button", use_container_width=True)

    if start_clicked:
        st.session_state.start_time = time.time()

        # 1. Submit files to WF1
        with st.spinner("📤 Envoi des fichiers..."):
            job_id = submit_job(uploaded_files)

        if not job_id:
            st.error("Impossible de démarrer le traitement.")
            st.stop()

        st.info(f"✅ Job créé : `{job_id}`. Le traitement s’exécute en arrière-plan...")

        # 2. Poll WF3
        spinner_placeholder = st.empty()
        with spinner_placeholder.container():
            st.markdown("""
            <div class="custom-spinner">
                <div class="loader"></div>
                <div class="spinner-text">⚙️ Traitement en cours...</div>
                <div style="color: #b8c6db; font-size: 1rem; margin-top: 1rem;">
                    🔍 Analyse des documents<br>
                    🧠 Extraction des données<br>
                    🏷️ Attribution des codes NGP
                </div>
            </div>
            """, unsafe_allow_html=True)

        result = poll_status(job_id)
        spinner_placeholder.empty()

        if result:
            st.session_state.processing_time = round(time.time() - st.session_state.start_time, 1)
            st.session_state.results = result
            st.success(f"🎯 Traitement terminé – statut : **{result.get('status','?')}**")
        else:
            st.error("❌ Aucun résultat reçu depuis le backend.")

# ================================
# RESULTS DISPLAY
# ================================
if st.session_state.get("results"):
    data = st.session_state.results
    if isinstance(data.get("results"), list):
        df = pd.DataFrame(data["results"])
    elif isinstance(data.get("results"), dict):
        df = pd.DataFrame([data["results"]])
    else:
        df = pd.DataFrame([data])

    processing_time = round(st.session_state.get("processing_time", 0), 1)
    time_text = f"⏱ Temps total : {int(processing_time//60)}m {int(processing_time%60)}s" if processing_time > 60 else f"⏱ {processing_time}s"
    st.markdown(f'<div class="big-time">{time_text}</div>', unsafe_allow_html=True)

    if not df.empty:
        st.markdown(
            '<div class="table-wrap">'
            '<table class="big-table"><thead><tr>'
            + ''.join([f'<th>{col}</th>' for col in df.columns])
            + '</tr></thead><tbody>'
            + ''.join(['<tr>' + ''.join([f'<td>{row[col]}</td>' for col in df.columns]) + '</tr>' for _, row in df.iterrows()])
            + '</tbody></table></div>',
            unsafe_allow_html=True
        )

        excel_io = BytesIO()
        df.to_excel(excel_io, index=False, engine="openpyxl")
        excel_io.seek(0)

        left_col, _, right_col = st.columns([1.8, 4.4, 1.4], gap="medium")
        with left_col:
            st.download_button(
                label="📥 Exporter vers Excel",
                data=excel_io.getvalue(),
                file_name=f"sorepco_export_{int(time.time())}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="excel_download"
            )
        with right_col:
            if st.button("🔄 Nouveau traitement"):
                for k in list(st.session_state.keys()):
                    if k.startswith(('results', 'processing_time', 'start_time')):
                        del st.session_state[k]
                st.session_state.uploader_key += 1
                st.rerun()
    else:
        st.warning("Aucune donnée affichable.")

# ================================
# FOOTER
# ================================
st.markdown("""
<div class="footer">
    ✨ Conçu avec passion par <strong>Firas Zouaghi</strong> • Propulsé par l'IA nouvelle génération
</div>
""", unsafe_allow_html=True)
