# ──────────────────────────────────────────────
#  SOREPCO Automation – full Streamlit app
#  (2025-10-05 centred uploader edition - FIXED v2)
# ──────────────────────────────────────────────
import streamlit as st
import requests
import pandas as pd
import time
from io import BytesIO

# ───── PAGE CONFIG
st.set_page_config(page_title="SOREPCO Automation",
                   layout="wide",
                   page_icon="📄",
                   initial_sidebar_state="collapsed")

# ───── GLOBAL STYLE (incl. centred uploader)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
.stApp { background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%) !important; }
#MainMenu, footer, header { visibility: hidden; }
* { font-family: 'Inter', sans-serif !important; }

/* ─── Hero card */
.hero-container { margin: 2rem auto 2.5rem; max-width: 900px; padding: 0 1.5rem; }
.hero-card {
    background: rgba(255, 255, 255, .1);
    border-radius: 24px;
    padding: 3rem;
    text-align: center;
    border: 1px solid rgba(255, 255, 255, .2);
    backdrop-filter: blur(20px);
    box-shadow: 0 8px 32px rgba(31, 38, 135, .37);
    animation: float 3s ease-in-out infinite;
}
@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}
.hero-title {
    font-size: clamp(2.5rem, 5vw, 4rem);
    font-weight: 800;
    margin: 0 0 1rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    color: transparent;
}
.hero-subtitle { font-size: 1.25rem; color: #b8c6db; margin: 0; line-height: 1.6; }

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

/* MODIFICATION: Enhanced centering and spacing for inner drop-zone flex */
div[data-testid="stFileUploadDropzone"] > div {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important; /* Ensure content is centered horizontally */
    justify-content: center !important; /* Ensure content is centered vertically if space allows */
    gap: 1rem !important; /* Increased gap for better spacing */
    min-height: unset !important;
    width: 100% !important; /* Ensure it takes full width to center effectively */
    text-align: center !important; /* Center text within its own container */
}


/* Cloud icon */
[data-testid="stFileUploader"] section svg {
    width: 68px !important;
    height: 68px !important;
    color: #8b5cf6 !important;
    margin: 0 !important;
}

/* Helper text */
[data-testid="stFileUploader"] section span,
[data-testid="stFileUploader"] section p {
    font-size: 1.05rem !important;
    color: #d1d5db !important;
    margin: 0 !important; /* Keep margin 0 to let gap handle spacing */
    text-align: center !important; /* Ensure text is centered */
    line-height: 1.4 !important; /* Improve readability */
}

/* MODIFICATION: Correctly rebuilt "OR" divider */
/* The 'OR' text itself is a <p> tag within the section */
[data-testid="stFileUploader"] section > p {
    font-size: 1rem !important;
    font-weight: 600;
    color: #bb83ff !important;
    margin: 0.5rem 0 !important; /* Adjust vertical margin for OR text */
    width: 80%; /* Control width of the OR line segment */
    display: flex;
    align-items: center;
    gap: 1rem;
    text-align: center;
}
/* Pseudo-elements for the lines on either side of "OR" */
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

/* ─── Spinner loader */
.loader {
    border: 6px solid rgba(255, 255, 255, .1);
    border-top: 6px solid #a855f7;
    border-radius: 50%;
    width: 80px;
    height: 80px;
    animation: spin 1s linear infinite;
    margin: 0 auto;
}
@keyframes spin {
    0% { transform: rotate(0); }
    100% { transform: rotate(360deg); }
}
.spinner-text { font-size: 1.3rem; color: #a855f7; font-weight: 600; margin-top: 1rem; text-align: center; }

.big-time {
    text-align: center;
    font-size: 1.8rem;
    font-weight: 700;
    color: #a855f7;
    margin: 2rem auto;
    padding: 1.4rem;
    background: rgba(139, 92, 246, .1);
    border-radius: 16px;
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 20px rgba(139, 92, 246, .2);
    max-width: 600px;
}

.table-wrap { max-width: 1200px; margin: 0 auto; padding: 0 1.5rem; }
.big-table {
    width: 100%;
    border-collapse: collapse;
    margin: 2rem 0;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0, 0, 0, .3);
}
.big-table th, .big-table td {
    font-size: 1rem;
    padding: 1.4rem;
    text-align: center;
    border: 1px solid rgba(255, 255, 255, .1);
}
.big-table th { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #fff; font-weight: 600; }
.big-table td { background: rgba(255, 255, 255, .05); color: #fff; }
.big-table tr:hover td { background: rgba(255, 255, 255, .1); }

/* ─── Footer */
.footer {
    margin-top: 3rem;
    padding: 2rem;
    text-align: center;
    color: #b8c6db;
    font-size: .9rem;
    border-top: 1px solid rgba(255, 255, 255, .1);
}
.footer strong {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    color: transparent;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ───── HERO SECTION
st.markdown("""
<div class="hero-container">
  <div class="hero-card">
    <div class="hero-title">SOREPCO AUTOMATION</div>
    <p class="hero-subtitle">Interface nouvelle génération pour l'extraction automatique et l'attribution des codes NGP</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ───── CENTRED UPLOADER
# The centering is now handled purely by the CSS targeting `[data-testid="stFileUploader"] section`
if 'uploader_key' not in st.session_state:
    st.session_state.uploader_key = 0
uploaded_files = st.file_uploader("Déposez vos PDF",
                                  type=["pdf"],
                                  accept_multiple_files=True,
                                  label_visibility="collapsed",
                                  key=f"uploader_{st.session_state.uploader_key}")

# ───── BACKEND ENDPOINTS
SUBMIT_URL = "https://sorepco-automation.app.n8n.cloud/webhook/Zautomation"
STATUS_URL = "https://sorepco-automation.app.n8n.cloud/webhook/status"

# ───── HELPER FUNCTIONS
def submit_job(file_list):
    try:
        r = requests.post(SUBMIT_URL,
                          files=[("files", (f.name, f.getvalue(), "application/pdf"))
                                 for f in file_list],
                          timeout=60)
        r.raise_for_status()
        return r.json().get("job_id")
    except Exception as e:
        st.error(f"❌ Erreur d'envoi : {e}")
        return None

def poll_status(job_id, timeout=900, interval=10):
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(STATUS_URL, params={"job_id": job_id})
            if r.status_code == 200:
                data = r.json()
                if data.get("status") in ["completed", "error"]:
                    return data
            elif r.status_code == 404:
                st.warning("⚠️ Job introuvable.")
                return None
        except Exception as e:
            st.error(f"Erreur statut : {e}")
            return None
        time.sleep(interval)
    st.warning("⏰ Délai dépassé.")
    return None

# ───── PROCESSING
if uploaded_files:
    start_clicked = st.button("🚀 START", use_container_width=True)
    if start_clicked:
        st.session_state.start_time = time.time()
        with st.spinner("📤 Envoi des fichiers…"):
            job_id = submit_job(uploaded_files)
        if not job_id:
            st.stop()
        st.info(f"✅ Job créé : `{job_id}` – traitement en cours…")
        spin = st.empty()
        with spin.container():
            st.markdown('<div class="loader"></div><div class="spinner-text">Traitement…</div>',
                        unsafe_allow_html=True)
        result = poll_status(job_id)
        spin.empty()
        if result:
            st.session_state.processing_time = round(time.time() - st.session_state.start_time, 1)
            st.session_state.results = result
            st.success(f"🎯 Terminé – statut : **{result.get('status', '?')}**")
        else:
            st.error("❌ Aucun résultat reçu.")

# ───── RESULTS
if st.session_state.get("results"):
    res = st.session_state.results
    if isinstance(res.get("results"), list):
        df = pd.DataFrame(res["results"])
    elif isinstance(res.get("results"), dict):
        df = pd.DataFrame([res["results"]])
    else:
        df = pd.DataFrame([res])

    # time display
    t = st.session_state.get("processing_time", 0)
    if t >= 60:
        st.markdown(f'<div class="big-time">⏱ Temps : {int(t // 60)}:{int(t % 60):02d}</div>',
                    unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="big-time">⏱ Temps : {t} s</div>', unsafe_allow_html=True)

    if not df.empty:
        st.markdown('<div class="table-wrap"><table class="big-table"><thead><tr>' +
                    ''.join([f'<th>{c}</th>' for c in df.columns]) +
                    '</tr></thead><tbody>' +
                    ''.join(['<tr>' + ''.join([f'<td>{row[col]}</td>' for col in df.columns]) +
                             '</tr>' for _, row in df.iterrows()]) +
                    '</tbody></table></div>', unsafe_allow_html=True)

        # Excel export
        out = BytesIO()
        df.to_excel(out, index=False, engine="openpyxl")
        out.seek(0)
        col_l, col_r = st.columns(2)
        with col_l:
            st.download_button("📥 Exporter vers Excel",
                               data=out.getvalue(),
                               file_name=f"sorepco_{int(time.time())}.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        with col_r:
            if st.button("🔄 Nouveau traitement"):
                for k in list(st.session_state.keys()):
                    if k.startswith(('results', 'processing_time', 'start_time')):
                        del st.session_state[k]
                st.session_state.uploader_key += 1
                st.rerun()
    else:
        st.warning("⚠️ Aucune donnée à afficher.")

# ───── FOOTER
st.markdown("""
<div class="footer">
✨ Conçu avec passion par <strong>Firas Zouaghi</strong> • Propulsé par l'IA nouvelle génération
</div>
""", unsafe_allow_html=True)
