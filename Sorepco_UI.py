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
    margin: 2rem auto 3rem auto;
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
    margin: 3rem auto;
    padding: 0 1.5rem;
    z-index: 1;
    position: relative;
}

/* Target all file uploader elements */
[data-testid="stFileUploader"] {
    z-index: 1 !important;
}

[data-testid="stFileUploader"] > div {
    border: none !important;
    background: transparent !important;
    padding: 0 !important;
}

[data-testid="stFileUploaderDropzone"] {
    border: 2px dashed rgba(255, 255, 255, 0.2) !important;
    background: rgba(255, 255, 255, 0.1) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border-radius: 24px !important;
    padding: 3rem !important;
    text-align: center !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    min-height: 300px !important;
    max-width: 600px !important;
    margin: 0 auto !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
}

[data-testid="stFileUploaderDropzone"]:hover {
    border-color: #a855f7 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 20px 40px rgba(139, 92, 246, 0.2) !important;
    background: rgba(139, 92, 246, 0.05) !important;
}

/* Custom upload zone content */
[data-testid="stFileUploaderDropzone"] > div > div {
    display: none !important;
}

[data-testid="stFileUploaderDropzone"]::before {
    content: '☁️';
    font-size: 3rem;
    display: block;
    margin-bottom: 1rem;
    opacity: 0.8;
    transition: all 0.3s ease;
}

[data-testid="stFileUploaderDropzone"]:hover::before {
    opacity: 1;
    transform: scale(1.1);
}

[data-testid="stFileUploaderDropzone"]::after {
    content: 'Glissez-déposez vos fichiers PDF\\Aou cliquez pour sélectionner';
    font-size: 1.1rem;
    font-weight: 600;
    color: #ffffff;
    white-space: pre-line;
    text-align: center;
    line-height: 1.5;
    margin-top: 1rem;
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

/* === SUCCESS MESSAGE === */
.stSuccess {
    background: rgba(139, 92, 246, 0.1) !important;
    border: 1px solid rgba(139, 92, 246, 0.3) !important;
    border-radius: 16px !important;
    backdrop-filter: blur(10px) !important;
    text-align: center !important;
    margin: 0 auto !important;
    max-width: 600px !important;
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
# HELPER FUNCTIONS
# ================================

def run_workflow_webhook(files):
    """Use cloud webhook approach - production URL"""
    try:
        webhook_url = "https://sorepco-automation.app.n8n.cloud/webhook/Zautomation"

        response = requests.post(
            webhook_url,
            files=files,
            timeout=1000,
            stream=True
        )

        if response.status_code == 200:
            try:
                return True, response.json()
            except:
                return True, {"message": "Processing completed", "raw_response": response.text}
        else:
            return False, f"Webhook returned status {response.status_code}: {response.text}"

    except requests.exceptions.Timeout:
        return False, "Request timed out (2 minutes). The workflow might still be running."
    except Exception as e:
        return False, f"Error calling webhook: {str(e)}"

# ================================
# HERO SECTION
# ================================
st.markdown("""
<div class="hero-container">
    <div class="hero-card">
        <div style="
            font-size: clamp(2.5rem, 5vw, 4rem);
            font-weight: 800;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            text-align: center;
            line-height: 1.2;
            animation: titleGlow 3s ease-in-out infinite alternate;
        ">
            SOREPCO AUTOMATION
        </div>
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
        start_clicked = st.button("🚀 START", key="start_button", use_container_width=True)

    if start_clicked:
        st.session_state.start_time = time.time()
        files = [("files", (f.name, f, "application/pdf")) for f in uploaded_files]

        spinner_placeholder = st.empty()
        
        with spinner_placeholder.container():
            st.markdown("""
            <div class="custom-spinner">
                <div class="loader"></div>
                <div class="spinner-text">⚙️ Workflow en cours d'exécution...</div>
                <div style="color: #b8c6db; font-size: 1rem; margin-top: 1rem;">
                    🔍 Analyse des documents PDF<br>
                    🧠 Extraction des données<br>
                    🏷️ Attribution des codes NGP
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        success, result = run_workflow_webhook(files)
        spinner_placeholder.empty()

        if success:
            st.session_state.processing_time = round(time.time() - st.session_state.start_time, 1)
            st.session_state.results = result
            st.success("🎊 Résultats extraits avec succès ! Données prêtes pour l'analyse.")
        else:
            st.error(f"❌ Erreur lors du traitement: {result}")
            st.info("💡 Vérifiez que le workflow n8n cloud est activé et accessible.")

# ================================
# RESULTS SECTION
# ================================
if st.session_state.get("results"):
    try:
        results_data = st.session_state.results

        if isinstance(results_data, list):
            df = pd.DataFrame(results_data)
        elif isinstance(results_data, dict) and 'data' in results_data:
            df = pd.DataFrame(results_data['data'])
        elif isinstance(results_data, dict):
            df = pd.DataFrame([results_data])
        else:
            df = pd.DataFrame(results_data)

        processing_time = round(st.session_state.get("processing_time", 0), 1)

        if processing_time >= 60:
            minutes = int(processing_time // 60)
            seconds = int(processing_time % 60)
            time_text = f"⏱ Temps de traitement : {minutes}:{seconds:02d}"
        else:
            time_text = f"⏱ Temps de traitement : {processing_time} secondes"

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
            try:
                df.to_excel(excel_io, index=False, engine="openpyxl")
            except:
                df.to_excel(excel_io, index=False)
            excel_io.seek(0)

            left_col, spacer, right_col = st.columns([1.8, 4.4, 1.4], gap="medium")

            with left_col:
                st.download_button(
                    label="📥 Exporter vers Excel",
                    data=excel_io.getvalue(),
                    file_name=f"sorepco_export_{int(time.time())}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="excel_download_fixed"
                )

            with right_col:
                if st.button("🔄 Nouveau traitement", key="new_treatment_fixed"):
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
    ✨ Conçu avec passion par <strong>Firas Zouaghi</strong> • Propulsé par l'IA nouvelle génération
</div>
""", unsafe_allow_html=True)
