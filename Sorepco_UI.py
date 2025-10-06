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
# ENHANCED CSS FOR CLOUD COMPATIBILITY
# ================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* === Footer Linkedin icon === */
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

/* === FORCE DARK THEME === */
.stApp {
    background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%) !important;
    min-height: 100vh;
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* === GLOBAL STYLES === */
* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* === ANIMATED BACKGROUND === */
.stApp::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background:
        radial-gradient(circle at 20% 50%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
        radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
        radial-gradient(circle at 40% 80%, rgba(120, 219, 255, 0.3) 0%, transparent 50%);
    z-index: 0;
    pointer-events: none;
    animation: backgroundShift 20s ease-in-out infinite;
}

@keyframes backgroundShift {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.8; }
}

/* === HERO SECTION === */
.hero-container {
    position: relative;
    margin: 2rem auto 1rem auto;
    max-width: 900px;
    padding: 0 1.5rem;
    z-index: 1;
}

.hero-card {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 24px;
    padding: 3rem;
    text-align: center;
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    position: relative;
    overflow: hidden;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    animation: float 3s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}

.hero-title {
    font-size: clamp(2.5rem, 5vw, 4rem);
    font-weight: 800;
    margin: 0 0 1rem 0;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    background-clip: text;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.2;
    animation: titleGlow 3s ease-in-out infinite alternate;
}

@keyframes titleGlow {
    from { filter: drop-shadow(0 0 20px rgba(102, 126, 234, 0.5)); }
    to { filter: drop-shadow(0 0 30px rgba(118, 75, 162, 0.8)); }
}

.hero-subtitle {
    font-size: 1.25rem;
    font-weight: 400;
    color: #b8c6db;
    margin: 0;
    line-height: 1.6;
}

/* === FILE UPLOADER STYLING === */
.upload-container {
    max-width: 800px;
    margin: 1rem auto;
    padding: 0 1.5rem;
    z-index: 1;
    position: relative;
}

/* ─── Uploader card */
[data-testid="stFileUploader"] section {
    margin: 3rem auto !important;
    max-width: 420px;
    width: 100%;
    padding: 2.2rem 1.8rem;
    border-radius: 24px;
    background: rgba(255, 255, 255, .08) !important;
    backdrop-filter: blur(20px) !important;
    border: 3px dashed rgba(139, 92, 246, .45) !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, .25) !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    gap: 1.15rem !important;
    transition: .3s all;
}

[data-testid="stFileUploader"] section:hover {
    border-color: rgba(139, 92, 246, .75) !important;
    background: rgba(139, 92, 246, .12) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 38px rgba(139, 92, 246, .35) !important;
}

/* inner drop-zone flex */
div[data-testid="stFileUploadDropzone"] > div {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    width: 100% !important;
}

/* Icon spacing */
[data-testid="stFileUploader"] section svg {
    width: 68px !important;
    height: 68px !important;
    color: #8b5cf6 !important;
    margin: 0 auto 1rem auto !important;
}

/* Helper text */
[data-testid="stFileUploader"] section span {
    font-size: 1.05rem !important;
    color: #d1d5db !important;
    text-align: center !important;
    line-height: 1.4 !important;
}

/* "OR" Divider */
[data-testid="stFileUploader"] section > p {
    font-size: 1rem !important;
    font-weight: 600;
    color: #bb83ff !important;
    margin: 0.5rem 0 !important;
    width: 80%;
    display: flex;
    align-items: center;
    gap: 1rem;
}

[data-testid="stFileUploader"] section > p::before,
[data-testid="stFileUploader"] section > p::after {
    content: '';
    flex-grow: 1;
    height: 1px;
    background: linear-gradient(90deg, transparent 0%, #8b5cf6 50%, transparent 100%);
}

/* Browse button */
[data-testid="stFileUploader"] section button {
    background: linear-gradient(135deg, #8b5cf6 0%, #a855f7 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 14px !important;
    padding: .9rem 2.6rem !important;
    font-weight: 600 !important;
    font-size: 1.05rem !important;
    box-shadow: 0 4px 20px rgba(139, 92, 246, .4) !important;
    transition: .3s all;
}

[data-testid="stFileUploader"] section button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 28px rgba(139, 92, 246, .6) !important;
}

/* === UPLOADED FILES DISPLAY === */
[data-testid="stFileUploader"] ul {
    background: rgba(255, 255, 255, 0.08) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(139, 92, 246, 0.3) !important;
    border-radius: 16px !important;
    padding: 1rem !important;
    margin: 1rem auto !important;
    max-width: 600px !important;
    width: auto !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2) !important;
}

[data-testid="stFileUploader"] ul li {
    background: rgba(139, 92, 246, 0.1) !important;
    border: 1px solid rgba(139, 92, 246, 0.25) !important;
    border-radius: 12px !important;
    padding: 0.8rem 1rem !important;
    margin: 0.5rem 0 !important;
    color: #ffffff !important;
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    transition: all 0.2s ease !important;
    min-width: 0 !important;
}

[data-testid="stFileUploader"] ul li:hover {
    background: rgba(139, 92, 246, 0.15) !important;
    border-color: rgba(139, 92, 246, 0.4) !important;
}

/* Filename container - allows wrapping and vertical stacking */
[data-testid="stFileUploader"] ul li > div:first-child {
    order: 1 !important;
    flex-grow: 1 !important;
    overflow-wrap: break-word !important;
    word-break: break-word !important;
    min-width: 0 !important;
    padding-right: 1rem !important;
    display: flex !important;
    flex-direction: column !important;
    gap: 0.3rem !important;
}

/* Filename styling */
[data-testid="stFileUploader"] ul li > div:first-child > span:first-child {
    font-weight: 500 !important;
    font-size: 0.95rem !important;
}

/* File size styling - displayed below filename */
[data-testid="stFileUploader"] ul li > div:first-child > small,
[data-testid="stFileUploader"] ul li > div:first-child > span:last-child {
    font-size: 0.8rem !important;
    color: #b8c6db !important;
    opacity: 0.8 !important;
    display: block !important;
}

/* X button alignment */
[data-testid="stFileUploader"] ul li button {
    background: rgba(255, 255, 255, 0.1) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    color: #ffffff !important;
    border-radius: 8px !important;
    padding: 0.3rem 0.6rem !important;
    transition: all 0.2s ease !important;
    margin-left: auto !important;
    order: 2 !important;
    flex-shrink: 0 !important;
    align-self: flex-start !important;
}

[data-testid="stFileUploader"] ul li button:hover {
    background: rgba(255, 77, 77, 0.3) !important;
    border-color: rgba(255, 77, 77, 0.5) !important;
}
/* === BUTTON STYLING === */
.stButton > button {
    background: linear-gradient(135deg, #8b5cf6 0%, #a855f7 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 16px !important;
    padding: 1.5rem 3rem !important;
    font-size: 1.2rem !important;
    font-weight: 700 !important;
    cursor: pointer !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 20px rgba(139, 92, 246, 0.3) !important;
    min-width: 250px !important;
    height: 56px !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(139, 92, 246, 0.5) !important;
}

.stDownloadButton > button {
    background: linear-gradient(135deg, #8b5cf6 0%, #a855f7 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 16px !important;
    padding: 1rem 2rem !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 20px rgba(168, 85, 247, 0.3) !important;
    height: 48px !important;
    min-width: 200px !important;
}

.stDownloadButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(168, 85, 247, 0.5) !important;
}

/* === SPINNER === */
.custom-spinner {
    text-align: center;
    padding: 3rem;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(20px);
    border-radius: 24px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    margin: 2rem auto;
    max-width: 500px;
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
}

.loader {
    border: 6px solid rgba(255, 255, 255, 0.1);
    border-top: 6px solid #a855f7;
    border-radius: 50%;
    width: 80px;
    height: 80px;
    animation: spin 1s linear infinite;
    margin: 40px auto;
    box-shadow: 0 0 30px rgba(168, 85, 247, 0.3);
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.spinner-text {
    text-align: center;
    font-size: 1.3rem;
    color: #a855f7;
    font-weight: 600;
    margin-top: 1.5rem;
    animation: textPulse 2s ease-in-out infinite;
}

@keyframes textPulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}

/* === TIME DISPLAY === */
.big-time {
    text-align: center;
    font-size: 1.8rem;
    font-weight: 700;
    color: #a855f7;
    margin: 2rem 0;
    padding: 1.5rem;
    background: rgba(139, 92, 246, 0.1);
    border-radius: 16px;
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 20px rgba(139, 92, 246, 0.2);
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
}

/* === TABLE === */
.table-wrap {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1.5rem;
}

.big-table {
    width: 100%;
    border-collapse: collapse;
    margin: 2rem 0;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.big-table th, .big-table td {
    font-size: 1rem;
    padding: 1.5rem;
    text-align: center;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.big-table th {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    font-weight: 600;
}

.big-table th:first-child {
    text-align: left;
}

.big-table td {
    background: rgba(255, 255, 255, 0.05);
    color: #ffffff;
    transition: background-color 0.2s ease;
}

.big-table td:first-child {
    text-align: left;
}

.big-table tr:hover td {
    background: rgba(255, 255, 255, 0.1);
}

/* === SUCCESS MESSAGE - CUSTOM STYLING === */
.custom-success {
    background: rgba(139, 92, 246, 0.1) !important;
    border: 1px solid rgba(139, 92, 246, 0.3) !important;
    border-radius: 16px !important;
    backdrop-filter: blur(20px) !important;
    padding: 1.5rem !important;
    text-align: center !important;
    margin: 2rem auto !important;
    max-width: 600px !important;
    box-shadow: 0 8px 32px rgba(139, 92, 246, 0.25) !important;
    color: #a855f7 !important;
    font-size: 1.2rem !important;
    font-weight: 600 !important;
}

/* === FOOTER === */
.footer {
    text-align: center;
    margin-top: 3rem;
    padding: 2rem;
    color: #b8c6db;
    font-size: 0.9rem;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.footer strong {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    background-clip: text;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 600;
}

/* === RESPONSIVE === */
@media screen and (max-width: 768px) {
    .hero-title {
        font-size: 2.5rem;
    }
    .stDownloadButton button, .stButton button {
        width: 100% !important;
    }
}

/* === SCROLLBAR === */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #8b5cf6 0%, #a855f7 100%);
}
</style>
""", unsafe_allow_html=True)

# ================================
# BACKEND ENDPOINTS
# ================================
SUBMIT_URL = "https://sorepco-automation.app.n8n.cloud/webhook/Zautomation"
STATUS_URL = "https://sorepco-automation.app.n8n.cloud/webhook/status"

# ================================
# HELPER FUNCTIONS
# ================================
def submit_job(files):
    """Submit PDF(s) to WF1 and return job_id"""
    try:
        r = requests.post(
            SUBMIT_URL,
            files=[("files", (f.name, f.getvalue(), "application/pdf")) for f in files],
            timeout=60
        )
        r.raise_for_status()
        data = r.json()
        return data.get("job_id")
    except Exception as e:
        st.error(f"❌ Erreur d'envoi : {e}")
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
# PROCESSING SECTION
# ================================
if uploaded_files:
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        start_clicked = st.button("START", key="start_button", use_container_width=True)

    if start_clicked:
        st.session_state.start_time = time.time()

        # 1. Submit files to WF1
        with st.spinner("Envoi des fichiers..."):
            job_id = submit_job(uploaded_files)

        if not job_id:
            st.error("Impossible de démarrer le traitement.")
            st.stop()

        # COMMENTED OUT - Job creation message
        # st.info(f"✅ Job créé : `{job_id}`. Le traitement s'exécute en arrière-plan...")

        # 2. Poll WF3
        spinner_placeholder = st.empty()
        
        with spinner_placeholder.container():
            st.markdown("""
            <div class="custom-spinner">
                <div class="loader"></div>
                <div class="spinner-text">⚙️ Traitement en cours...</div>
                <div style="color: #b8c6db; font-size: 1rem; margin-top: 1rem;">
                    Extraction OCR multi-pages<br>
                    Analyse sémantique par agents IA<br>
                    Classification intelligente des données<br>
                    Attribution automatique des codes NGP<br>
                    Validation et structuration finale
                </div>
            </div>
            """, unsafe_allow_html=True)

        result = poll_status(job_id)
        spinner_placeholder.empty()

        if result:
            st.session_state.processing_time = round(time.time() - st.session_state.start_time, 1)
            st.session_state.results = result
            
            # Custom styled success message
            status = result.get('status', '?')
            status_text = "Complété" if status == "completed" else status
            st.markdown(f"""
            <div class="custom-success">
                ✅ Traitement terminé – statut : <strong>{status_text}</strong>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("❌ Aucun résultat reçu depuis le backend.")

# ================================
# RESULTS SECTION
# ================================
if st.session_state.get("results"):
    try:
        data = st.session_state.results
        
        # Handle different result structures
        if isinstance(data.get("results"), list):
            df = pd.DataFrame(data["results"])
        elif isinstance(data.get("results"), dict):
            df = pd.DataFrame([data["results"]])
        else:
            df = pd.DataFrame([data])

        #processing_time = round(st.session_state.get("processing_time", 0), 1)

        #if processing_time >= 60:
        #    minutes = int(processing_time // 60)
        #    seconds = int(processing_time % 60)
        #    time_text = f"⏱ Temps de traitement : {minutes}:{seconds:02d}"
        #else:
         #   time_text = f"⏱ Temps de traitement : {processing_time} secondes"

        #st.markdown(f'<div class="big-time">{time_text}</div>', unsafe_allow_html=True)

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
            try:
                df.to_excel(excel_io, index=False, engine="openpyxl")
            except:
                df.to_excel(excel_io, index=False)
            excel_io.seek(0)

            left_col, spacer, right_col = st.columns([1.8, 4.4, 1.4], gap="medium")

            with left_col:
                st.download_button(
                    label="Exporter vers Excel",
                    data=excel_io.getvalue(),
                    file_name=f"sorepco_export_{int(time.time())}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="excel_download_fixed"
                )

            with right_col:
                if st.button("Nouveau traitement", key="new_treatment_fixed"):
                    for key in list(st.session_state.keys()):
                        if key.startswith(('results', 'processing_time', 'start_time')):
                            del st.session_state[key]
                    st.session_state.uploader_key += 1
                    st.rerun()
        else:
            st.warning("⚠️ Aucune donnée à afficher dans le tableau.")

    except Exception as e:
        st.error(f"❌ Erreur lors de l'affichage des résultats: {str(e)}")
        st.write("Debug - Raw results:", st.session_state.results)

# ================================
# FOOTER
# ================================
st.markdown("""
<div class="footer">
    Création par <strong>Firas Zouaghi</strong> • Propulsé par l'IA nouvelle génération<br>
    Contact 📧 <a href="mailto:zgh.firas@gmail.com" style="color: inherit; text-decoration: none;">zgh.firas@gmail.com</a> • 
    <a href="https://www.linkedin.com/in/firas-zouaghi-309884164/" target="_blank" style="color: inherit; text-decoration: none;">
        <i class="fab fa-linkedin"></i> LinkedIn
    </a>
</div>
""", unsafe_allow_html=True)
