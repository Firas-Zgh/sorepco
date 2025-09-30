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
    page_title="SOREPCO Automation ✨",
    layout="wide",
    page_icon="📄",
    initial_sidebar_state="collapsed",
)

# ================================
# HYBRID DESIGN SYSTEM WITH SPINNER
# ================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* === 💜 UNIFIED VIOLET PALETTE === */
:root {
    --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%); /* 💜 Main violet gradient */
    --secondary-gradient: linear-gradient(135deg, #8b5cf6 0%, #a855f7 100%); /* 💜 Secondary violet */
    --accent-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%); /* 💜 Accent violet */
    --dark-gradient: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
    --success-gradient: linear-gradient(135deg, #8b5cf6 0%, #a855f7 100%); /* 💜 Success violet */
    --warning-gradient: linear-gradient(135deg, #9333ea 0%, #8b5cf6 100%); /* 💜 Warning violet */

    --glass-bg: rgba(255, 255, 255, 0.1);
    --glass-border: rgba(255, 255, 255, 0.2);
    --glass-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);

    --text-primary: #ffffff;
    --text-secondary: #b8c6db;
    --text-accent: #a855f7; /* 💜 Violet accent text */

    --success: #10dc60;
    --warning: #ffce00;
    --error: #f04141;

    --border-radius: 16px;
    --border-radius-lg: 24px;
    --spacing-xs: 0.5rem;
    --spacing-sm: 1rem;
    --spacing-md: 1.5rem;
    --spacing-lg: 2rem;
    --spacing-xl: 3rem;
}

/* === GLOBAL RESET === */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background: var(--dark-gradient);
    color: var(--text-primary);
    margin: 0;
    padding: 0;
    overflow-x: hidden;
}

.stApp {
    background: var(--dark-gradient);
    min-height: 100vh;
}

.stApp > header {
    visibility: hidden;
}

/* === ANIMATED BACKGROUND === */
.main::before {
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
    z-index: -1;
    animation: backgroundShift 20s ease-in-out infinite;
}

@keyframes backgroundShift {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.8; }
}

/* === UI3 HERO SECTION === */
.hero-container {
    position: relative;
    margin: var(--spacing-lg) auto var(--spacing-xl) auto;
    max-width: 900px;
    padding: 0 var(--spacing-md);
}

.hero-card {
    background: var(--glass-bg);
    backdrop-filter: blur(20px);
    border: 1px solid var(--glass-border);
    border-radius: var(--border-radius-lg);
    padding: var(--spacing-xl);
    text-align: center;
    box-shadow: var(--glass-shadow);
    position: relative;
    overflow: hidden;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.hero-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
    transition: left 0.5s;
}

.hero-card:hover::before {
    left: 100%;
}

.hero-title {
    font-size: clamp(2.5rem, 5vw, 4rem);
    font-weight: 800;
    margin: 0 0 var(--spacing-sm) 0;
    background: var(--primary-gradient);
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
    color: var(--text-secondary);
    margin: 0;
    line-height: 1.6;
}

/* === UI3 UPLOAD SECTION === */
.upload-container {
    max-width: 800px;
    margin: var(--spacing-xl) auto;
    padding: 0 var(--spacing-md);
}

/* Style the file uploader properly */
.stFileUploader > div {
    border: none !important;
    background: transparent !important;
    padding: 0 !important;
}

.stFileUploader [data-testid="stFileUploaderDropzone"] {
    border: 2px dashed var(--glass-border) !important;
    background: var(--glass-bg) !important;
    backdrop-filter: blur(20px) !important;
    border-radius: var(--border-radius-lg) !important;
    padding: var(--spacing-xl) !important;
    text-align: center !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    min-height: 300px !important;
    max-width: 600px !important;
    margin: 0 auto !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    gap: var(--spacing-md) !important;
}

.stFileUploader [data-testid="stFileUploaderDropzone"]:hover {
    border-color: var(--text-accent) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 20px 40px rgba(139, 92, 246, 0.2) !important; /* 💜 Violet hover glow */
    background: rgba(139, 92, 246, 0.05) !important; /* 💜 Violet hover background */
}

/* 💜 Dynamic violet effect when dragging */
.stFileUploader [data-testid="stFileUploaderDropzone"][data-drag-over="true"] {
    border-color: #a855f7 !important; /* 💜 Violet drag border */
    background: rgba(168, 85, 247, 0.1) !important; /* 💜 Violet drag background */
    box-shadow: 0 0 30px rgba(168, 85, 247, 0.5) !important; /* 💜 Violet drag glow */
    transform: scale(1.02) !important;
}

/* Hide the default upload text and show custom */
.stFileUploader [data-testid="stFileUploaderDropzone"] > div {
    display: none !important;
}

.stFileUploader [data-testid="stFileUploaderDropzone"]::before {
    content: '☁️' !important;
    font-size: 3rem !important;
    color: var(--text-accent) !important;
    margin-bottom: var(--spacing-sm) !important;
    opacity: 0.8 !important;
    transition: all 0.3s ease !important;
}

.stFileUploader [data-testid="stFileUploaderDropzone"]:hover::before {
    opacity: 1 !important;
    transform: scale(1.1) !important;
}

.stFileUploader [data-testid="stFileUploaderDropzone"]::after {
    content: 'Glissez-déposez vos fichiers PDF\\Aou cliquez pour sélectionner' !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    color: var(--text-primary) !important;
    white-space: pre-line !important;
    text-align: center !important;
    line-height: 1.5 !important;
    margin-top: var(--spacing-sm) !important;
}

/* 🎨 START BUTTON STYLING - UI3 Enhanced */
.stButton > button {
    background: var(--success-gradient) !important; /* 🌈 Main button gradient color */
    color: white !important;
    border: none !important;
    border-radius: var(--border-radius) !important; /* 📐 Button corner radius */
    padding: var(--spacing-md) var(--spacing-xl) !important;
    font-size: 1.2rem !important; /* 📝 Button text size */
    font-weight: 700 !important; /* 💪 Button text weight */
    font-family: 'Inter', sans-serif !important;
    cursor: pointer !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 20px rgba(139, 92, 246, 0.3) !important; /* 💜 Violet button shadow */
    position: relative !important;
    overflow: hidden !important;
    min-width: 250px !important; /* 📏 Button minimum width */
    height: 56px !important; /* 📏 Button height */
}

.stButton > button:hover {
    transform: translateY(-2px) !important; /* 🚀 Hover lift effect */
    box-shadow: 0 8px 30px rgba(139, 92, 246, 0.5) !important; /* 💜 Violet hover shadow */
}

/* 📥 DOWNLOAD BUTTON STYLING - UI3 Enhanced */
.stDownloadButton > button {
    background: var(--secondary-gradient) !important; /* 🎨 Download button gradient */
    color: white !important;
    border: none !important;
    border-radius: var(--border-radius) !important;
    padding: var(--spacing-md) var(--spacing-lg) !important;
    font-size: 1rem !important; /* 📝 Download button text size */
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 20px rgba(168, 85, 247, 0.3) !important; /* 💜 Violet download shadow */
    height: 48px !important;
    min-width: 200px !important;
}

.stDownloadButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(168, 85, 247, 0.5) !important; /* 💜 Violet download hover */
}

/* 🌀 SPINNER STYLING - UI3 Enhanced */
.custom-spinner {
    text-align: center;
    padding: var(--spacing-xl);
    background: var(--glass-bg);
    backdrop-filter: blur(20px);
    border-radius: var(--border-radius-lg);
    border: 1px solid var(--glass-border);
    margin: var(--spacing-lg) auto;
    max-width: 500px;
    box-shadow: var(--glass-shadow);
}

.loader {
    border: 6px solid rgba(255, 255, 255, 0.1);
    border-top: 6px solid #a855f7; /* 💜 Violet spinner */
    border-radius: 50%;
    width: 80px;
    height: 80px;
    animation: spin 1s linear infinite;
    margin: 40px auto;
    box-shadow: 0 0 30px rgba(168, 85, 247, 0.3); /* 💜 Violet glow */
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.spinner-text {
    text-align: center;
    font-size: 1.3rem;
    color: var(--text-accent); /* 💜 Violet text */
    font-weight: 600;
    margin-top: var(--spacing-md);
    animation: textPulse 2s ease-in-out infinite;
}

@keyframes textPulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}

/* ⏱️ TIME DISPLAY STYLING - UI3 Enhanced */
.big-time {
    text-align: center;
    font-size: 1.8rem; /* 📝 Time display text size */
    font-weight: 700; /* 💪 Time display text weight */
    color: var(--text-accent); /* 🎨 Time display color */
    margin: var(--spacing-lg) 0;
    padding: var(--spacing-md); /* 📦 Time display padding */
    background: rgba(139, 92, 246, 0.1); /* 💜 Violet time display background */
    border-radius: var(--border-radius); /* 📐 Time display corner radius */
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 20px rgba(139, 92, 246, 0.2); /* 💜 Violet time display shadow */
    max-width: 600px; /* 📏 Time display max width */
    margin-left: auto;
    margin-right: auto;
}

/* 📋 TABLE WRAPPER - UI3 Enhanced */
.table-wrap {
    max-width: 1200px; /* 📏 Table container max width */
    margin: 0 auto;
    padding: 0 var(--spacing-md);
}

/* 📊 TABLE STYLING - UI3 Enhanced */
.big-table {
    width: 100%;
    border-collapse: collapse;
    margin: var(--spacing-lg) 0;
    border-radius: var(--border-radius); /* 📐 Table corner radius */
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3); /* ✨ Table shadow */
}

.big-table th, .big-table td {
    font-size: 1rem; /* 📝 Table text size */
    padding: var(--spacing-md); /* 📦 Table cell padding */
    text-align: center;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.big-table th {
    background: var(--primary-gradient); /* 🎨 Table header background */
    color: white;
    font-weight: 600; /* 💪 Header text weight */
}

.big-table th:first-child {
    text-align: left; /* 📍 First column alignment */
}

.big-table td {
    background: rgba(255, 255, 255, 0.05); /* 🌟 Table cell background */
    color: var(--text-primary); /* 🎨 Table text color */
    transition: background-color 0.2s ease;
}

.big-table td:first-child {
    text-align: left; /* 📍 First column data alignment */
}

.big-table tr:hover td {
    background: rgba(255, 255, 255, 0.1); /* ✨ Hover effect */
}

/* === SUCCESS MESSAGE STYLING === */
.stSuccess {
    background: rgba(139, 92, 246, 0.1) !important;
    border: 1px solid rgba(139, 92, 246, 0.3) !important;
    border-radius: var(--border-radius) !important;
    backdrop-filter: blur(10px) !important;
    text-align: center !important;
    margin: 0 auto !important;
    max-width: 600px !important;
}

/* === UI3 FOOTER === */
.footer {
    text-align: center;
    margin-top: var(--spacing-xl);
    padding: var(--spacing-lg);
    color: var(--text-secondary);
    font-size: 0.9rem;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.footer strong {
    background: var(--accent-gradient);
    background-clip: text;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 600;
}

/* === RESPONSIVE DESIGN === */
@media screen and (max-width: 768px) {
    .hero-title {
        font-size: 2.5rem;
    }

    .stDownloadButton button, .stButton button {
        width: 100% !important;
    }
}

/* === LOADING ANIMATIONS === */
@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}

.floating {
    animation: float 3s ease-in-out infinite;
}

/* === SCROLL IMPROVEMENTS === */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb {
    background: var(--accent-gradient);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--primary-gradient);
}
</style>

<script>
// Add dynamic drag and drop effects
document.addEventListener('DOMContentLoaded', function() {
    const dropzone = document.querySelector('[data-testid="stFileUploaderDropzone"]');
    if (dropzone) {
        dropzone.addEventListener('dragover', function(e) {
            e.preventDefault();
            this.setAttribute('data-drag-over', 'true');
        });

        dropzone.addEventListener('dragleave', function(e) {
            e.preventDefault();
            this.removeAttribute('data-drag-over');
        });

        dropzone.addEventListener('drop', function(e) {
            e.preventDefault();
            this.removeAttribute('data-drag-over');
        });
    }
});
</script>
""", unsafe_allow_html=True)

# ================================
# HELPER FUNCTIONS
# ================================

def test_n8n_connection():
    """Test n8n cloud webhook connection"""
    try:
        # Test if the cloud n8n endpoint is reachable
        response = requests.get(
            "https://sorepco-automation.app.n8n.cloud",
            timeout=5
        )
        return response.status_code in [200, 404], f"n8n cloud server status: {response.status_code}"
    except Exception as e:
        return False, f"Cannot reach n8n cloud server: {str(e)}"

def run_workflow_webhook(files):
    """Use cloud webhook approach - production URL"""
    try:
        # Production webhook URL for n8n cloud
        webhook_url = "https://sorepco-automation.app.n8n.cloud/webhook/Zautomation"

        response = requests.post(
            webhook_url,
            files=files,
            timeout=1000,  # 2 minutes timeout
            stream=True   # Enable streaming
        )

        if response.status_code == 200:
            try:
                return True, response.json()
            except:
                # If JSON parsing fails, return raw text
                return True, {"message": "Processing completed", "raw_response": response.text}
        else:
            return False, f"Webhook returned status {response.status_code}: {response.text}"

    except requests.exceptions.Timeout:
        return False, "Request timed out (2 minutes). The workflow might still be running."
    except Exception as e:
        return False, f"Error calling webhook: {str(e)}"

# ================================
# UI3 HERO SECTION
# ================================
st.markdown("""
<div class="hero-container">
    <div class="hero-card floating">
        <h1 class="hero-title">SOREPCO AUTOMATION</h1>
        <p class="hero-subtitle">Interface nouvelle génération pour l'extraction automatique et l'attribution des codes NGP</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ================================
# UI3 UPLOAD SECTION
# ================================
st.markdown('<div class="upload-container">', unsafe_allow_html=True)

# Use session state to manage uploader key for proper reset
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
# PROCESSING SECTION WITH SPINNER
# ================================
if uploaded_files:
    # Center the START button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        start_clicked = st.button("🚀 START", key="start_button", use_container_width=True)

    if start_clicked:
        # Initialize session state
        st.session_state.start_time = time.time()

        # Prepare files for upload
        files = [("files", (f.name, f, "application/pdf")) for f in uploaded_files]

        # Create a placeholder for the spinner
        spinner_placeholder = st.empty()
        
        # Show custom spinner
        with spinner_placeholder.container():
            st.markdown("""
            <div class="custom-spinner">
                <div class="loader"></div>
                <div class="spinner-text">⚙️ Workflow en cours d'exécution...</div>
                <div style="color: var(--text-secondary); font-size: 1rem; margin-top: 1rem;">
                    🔍 Analyse des documents PDF<br>
                    🧠 Extraction des données<br>
                    🏷️ Attribution des codes NGP
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Call the webhook
        success, result = run_workflow_webhook(files)
        
        # Clear the spinner after processing
        spinner_placeholder.empty()

        if success:
            # Store results
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
        # Handle different result formats
        results_data = st.session_state.results

        # If results is a list, use it directly
        if isinstance(results_data, list):
            df = pd.DataFrame(results_data)
        # If results is a dict with data key
        elif isinstance(results_data, dict) and 'data' in results_data:
            df = pd.DataFrame(results_data['data'])
        # If results is a dict, try to convert to DataFrame
        elif isinstance(results_data, dict):
            df = pd.DataFrame([results_data])
        else:
            df = pd.DataFrame(results_data)

        processing_time = round(st.session_state.get("processing_time", 0), 1)

        # Format processing time
        if processing_time >= 60:
            minutes = int(processing_time // 60)
            seconds = int(processing_time % 60)
            time_display = f"{minutes}:{seconds:02d}"
            time_text = f"⏱ Temps de traitement : {time_display}"
        else:
            time_text = f"⏱ Temps de traitement : {processing_time} secondes"

        st.markdown(f'<div class="big-time">{time_text}</div>', unsafe_allow_html=True)

        # Render table
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

            # Excel export
            excel_io = BytesIO()
            try:
                df.to_excel(excel_io, index=False, engine="openpyxl")
            except:
                df.to_excel(excel_io, index=False)
            excel_io.seek(0)

            # Button layout
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
                    # Clear all session state data
                    for key in list(st.session_state.keys()):
                        if key.startswith(('results', 'processing_time', 'start_time')):
                            del st.session_state[key]
                    
                    # Reset the uploader by changing its key
                    st.session_state.uploader_key += 1
                    
                    # Rerun to refresh the UI
                    st.rerun()
        else:
            st.warning("⚠️ Aucune donnée à afficher dans le tableau.")

    except Exception as e:
        st.error(f"❌ Erreur lors de l'affichage des résultats: {str(e)}")
        st.write("Debug - Raw results:", st.session_state.results)

# ================================
# UI3 FOOTER
# ================================
st.markdown("""
<div class="footer">
    ✨ Conçu avec passion par <strong>Firas Zouaghi</strong> • Propulsé par l'IA nouvelle génération
</div>
""", unsafe_allow_html=True)