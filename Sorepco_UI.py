# -------------------------
# SOREPCO Automation • UI + backend
# -------------------------
import streamlit as st
import requests, pandas as pd, time, json
from io import BytesIO

# ──────────────────────────────────────────────
#  PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="SOREPCO Automation",
    layout="wide",
    page_icon="📄",
    initial_sidebar_state="collapsed",
)

# ──────────────────────────────────────────────
#  GLOBAL CSS  (hero, buttons, tables …)
# ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* === DARK GRADIENT THEME === */
.stApp{
  background:linear-gradient(135deg,#0c0c0c 0%,#1a1a2e 50%,#16213e 100%)!important;
  min-height:100vh;
}
#MainMenu, footer, header{visibility:hidden;}
*{font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif!important;}

/* === FLOATING HERO CARD === */
.hero-container{margin:2rem auto 3rem;max-width:900px;padding:0 1.5rem;z-index:1;}
.hero-card{
  background:rgba(255,255,255,.1);backdrop-filter:blur(20px);
  border:1px solid rgba(255,255,255,.2);border-radius:24px;padding:3rem;text-align:center;
  box-shadow:0 8px 32px rgba(31,38,135,.37);animation:float 3s ease-in-out infinite;
}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-10px)}}
.hero-title{
  font-size:clamp(2.5rem,5vw,4rem);font-weight:800;margin:0 0 1rem;
  background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);
  -webkit-background-clip:text;color:transparent;animation:titleGlow 3s ease-in-out infinite alternate;
}
@keyframes titleGlow{
  from{filter:drop-shadow(0 0 20px rgba(102,126,234,.5))}
  to  {filter:drop-shadow(0 0 30px rgba(118,75,162,.8))}
}
.hero-subtitle{font-size:1.25rem;color:#b8c6db;margin:0;line-height:1.6}

/* ───── FILE-UPLOADER (COMPACT, CENTRED) ───── */
.upload-container{max-width:450px;margin:3rem auto;padding:0 1rem;}

[data-testid="stFileUploader"] section{
  max-width:420px;width:100%;
  background:rgba(255,255,255,.08)!important;backdrop-filter:blur(20px)!important;
  border:3px dashed rgba(139,92,246,.45)!important;border-radius:24px!important;
  box-shadow:0 8px 32px rgba(0,0,0,.25)!important;padding:2rem 1.8rem!important;
  display:flex!important;flex-direction:column!important;align-items:center!important;gap:1.2rem!important;
  transition:.3s all!important;
}
[data-testid="stFileUploader"] section:hover{
  border-color:rgba(139,92,246,.75)!important;background:rgba(139,92,246,.12)!important;
  transform:translateY(-2px)!important;box-shadow:0 12px 38px rgba(139,92,246,.35)!important;
}

/* — inner drop-zone flex-wrapper — */
div[data-testid="stFileUploadDropzone"]>div{
  display:flex!important;flex-direction:column!important;align-items:center!important;justify-content:center!important;
  min-height:unset!important;gap:.75rem!important;
}
/* icon */
[data-testid="stFileUploader"] section svg{
  width:68px!important;height:68px!important;color:#8b5cf6!important;margin:0!important;
}
/* helper text */
[data-testid="stFileUploader"] section span,
[data-testid="stFileUploader"] section p{
  font-size:1.05rem!important;color:#d1d5db!important;margin:0!important;text-align:center!important;line-height:1.35;
}
/* browse button */
[data-testid="stFileUploader"] section button{
  background:linear-gradient(135deg,#8b5cf6 0%,#a855f7 100%)!important;color:#fff!important;
  border:none!important;border-radius:14px!important;padding:.85rem 2.4rem!important;
  font-weight:600!important;font-size:1.05rem!important;box-shadow:0 4px 20px rgba(139,92,246,.4)!important;
  transition:.3s all!important;margin-top:.4rem!important;
}
[data-testid="stFileUploader"] section button:hover{
  transform:translateY(-2px)!important;box-shadow:0 6px 28px rgba(139,92,246,.6)!important;
}

/* — OR divider — */
[data-testid="stFileUploader"] section::before,
[data-testid="stFileUploader"] section::after{
  content:"";width:60%;height:1px;background:linear-gradient(90deg,transparent 0%,#8b5cf6 50%,transparent 100%);
}
[data-testid="stFileUploader"] section::before{margin-top:.6rem;}
[data-testid="stFileUploader"] section::after{
  content:"OR";height:auto;background:none;margin:.25rem 0 .4rem;
  font-weight:600;font-size:1rem;color:#bb83ff;text-align:center;width:100%;
}

/* === PRIMARY BUTTONS & TABLE/STYLES trimmed for brevity === */
/* (retain from your previous file – nothing changed there) */
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
#  BACKEND ENDPOINTS
# ──────────────────────────────────────────────
SUBMIT_URL = "https://sorepco-automation.app.n8n.cloud/webhook/Zautomation"
STATUS_URL = "https://sorepco-automation.app.n8n.cloud/webhook/status"

# ──────────────────────────────────────────────
#  UTILS
# ──────────────────────────────────────────────
def submit_job(files):
    try:
        r = requests.post(
            SUBMIT_URL,
            files=[("files",(f.name,f.getvalue(),"application/pdf")) for f in files],
            timeout=60,
        ); r.raise_for_status()
        return r.json().get("job_id")
    except Exception as e:
        st.error(f"❌ Erreur d'envoi : {e}"); return None

def poll_status(job_id, timeout=900, interval=10):
    start=time.time()
    while time.time()-start < timeout:
        try:
            r=requests.get(STATUS_URL,params={"job_id":job_id})
            if r.status_code==200:
                data=r.json()
                if data.get("status") in ["completed","error"]: return data
            elif r.status_code==404:
                st.warning("⚠️ Job introuvable."); return None
        except Exception as e:
            st.error(f"Erreur statut : {e}"); return None
        time.sleep(interval)
    st.warning("⏰ Délai dépassé (15 min)."); return None

# ──────────────────────────────────────────────
#  HERO SECTION
# ──────────────────────────────────────────────
st.markdown("""
<div class="hero-container">
  <div class="hero-card">
    <div class="hero-title">SOREPCO AUTOMATION</div>
    <p class="hero-subtitle">Interface nouvelle génération pour l'extraction automatique et l'attribution des codes NGP</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
#  UPLOAD SECTION
# ──────────────────────────────────────────────
st.markdown('<div class="upload-container">', unsafe_allow_html=True)
if 'uploader_key' not in st.session_state: st.session_state.uploader_key = 0
uploaded_files = st.file_uploader(
    "Déposez ici vos fichiers PDF",
    type=["pdf"], accept_multiple_files=True, label_visibility="collapsed",
    key=f"uploader_{st.session_state.uploader_key}"
)
st.markdown('</div>', unsafe_allow_html=True)

# ──────────────────────────────────────────────
#  PROCESSING + RESULTS (unchanged from your code)
# ──────────────────────────────────────────────
if uploaded_files:
    start_clicked = st.button("🚀 START", type="primary", use_container_width=True)
    if start_clicked:
        st.session_state.start_time = time.time()
        with st.spinner("📤 Envoi des fichiers…"): job_id = submit_job(uploaded_files)
        if not job_id: st.stop()
        st.info(f"✅ Job créé : `{job_id}` – traitement en cours…")
        spinner = st.empty()
        with spinner.container():
            st.markdown('<div style="text-align:center;padding:2rem;">'
                        '<div class="loader"></div>'
                        '<div class="spinner-text">⚙️ Traitement en cours…</div>'
                        '</div>', unsafe_allow_html=True)
        result = poll_status(job_id); spinner.empty()
        if result:
            st.session_state.processing_time = round(time.time()-st.session_state.start_time,1)
            st.session_state.results = result
            st.success(f"🎯 Terminé – statut : **{result.get('status','?')}**")
        else: st.error("❌ Aucun résultat du backend.")

# (… keep your DataFrame/table/export code exactly as before …)

# ──────────────────────────────────────────────
#  FOOTER
# ──────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-top:3rem;padding:2rem;color:#b8c6db;font-size:.9rem;
            border-top:1px solid rgba(255,255,255,.1);">
✨ Conçu avec passion par <strong style="
background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);
-webkit-background-clip:text;color:transparent;">Firas Zouaghi</strong> • Propulsé par l'IA nouvelle génération
</div>
""", unsafe_allow_html=True)
