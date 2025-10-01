import streamlit as st
import requests
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
# CLOUD-SAFE CSS
# ================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* --- base + dark gradient --- */
.stApp{
    background:linear-gradient(135deg,#0c0c0c 0%,#1a1a2e 50%,#16213e 100%)!important;
    min-height:100vh;
}
#MainMenu,footer,header{visibility:hidden;}
*{font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif!important;}

/* --- fancy background orbs --- */
.stApp::before{
    content:'';position:fixed;top:0;left:0;width:100%;height:100%;
    background:
      radial-gradient(circle at 20% 50%,rgba(120,119,198,.3)0%,transparent 50%),
      radial-gradient(circle at 80% 20%,rgba(255,119,198,.3)0%,transparent 50%),
      radial-gradient(circle at 40% 80%,rgba(120,219,255,.3)0%,transparent 50%);
    z-index:0;pointer-events:none;
    animation:bgShift 20s ease-in-out infinite;
}
@keyframes bgShift{0%,100%{opacity:1;}50%{opacity:.8;}}

/* --- hero --- */
.hero-container{position:relative;margin:2rem auto 3rem;max-width:900px;padding:0 1.5rem;z-index:1;}
.hero-card{
    background:rgba(255,255,255,.1);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);
    border:1px solid rgba(255,255,255,.2);border-radius:24px;padding:3rem;text-align:center;
    box-shadow:0 8px 32px rgba(31,38,135,.37);animation:float 3s ease-in-out infinite;
}
@keyframes float{0%,100%{transform:translateY(0);}50%{transform:translateY(-10px);}}

/* gradient title text */
.title-gradient{
    font-size:clamp(2.5rem,5vw,4rem);font-weight:800;margin-bottom:1rem;line-height:1.2;
    background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);
    -webkit-background-clip:text;background-clip:text;color:transparent;
    animation:titleGlow 3s ease-in-out infinite alternate;
}
@keyframes titleGlow{from{filter:drop-shadow(0 0 20px rgba(102,126,234,.5));}
                      to{filter:drop-shadow(0 0 30px rgba(118,75,162,.8));}}
.hero-subtitle{font-size:1.25rem;font-weight:400;color:#b8c6db;margin:0;line-height:1.6;}

/* --- uploader --- */
section[data-testid="stFileUploader"] label{display:none!important;} /* kill default text */

[data-testid="stFileUploaderDropzone"]{
  border:2px dashed rgba(255,255,255,.25)!important;background:rgba(255,255,255,.08)!important;
  backdrop-filter:blur(20px)!important;-webkit-backdrop-filter:blur(20px)!important;
  border-radius:24px!important;padding:3rem!important;text-align:center!important;
  min-height:300px!important;max-width:600px!important;margin:0 auto!important;
  display:flex!important;flex-direction:column!important;align-items:center!important;justify-content:center!important;
  transition:all .3s cubic-bezier(.4,0,.2,1)!important;
}
[data-testid="stFileUploaderDropzone"]:hover{
  border-color:#a855f7!important;transform:translateY(-2px)!important;
  box-shadow:0 20px 40px rgba(139,92,246,.2)!important;background:rgba(139,92,246,.05)!important;
}

/* nuke inner default blob */
[data-testid="stFileUploaderDropzone"] > div > div{display:none!important;}

/* custom icon/text */
[data-testid="stFileUploaderDropzone"]::before{
  content:'☁️';font-size:3rem;display:block;margin-bottom:1rem;opacity:.8;transition:.3s;
}
[data-testid="stFileUploaderDropzone"]:hover::before{opacity:1;transform:scale(1.1);}
[data-testid="stFileUploaderDropzone"]::after{
  content:'Glissez-déposez vos fichiers PDF\\Aou cliquez pour sélectionner';
  font-size:1.1rem;font-weight:600;color:#fff;white-space:pre-line;text-align:center;line-height:1.5;margin-top:1rem;
}

/* buttons */
.stButton>button{
  background:linear-gradient(135deg,#8b5cf6 0%,#a855f7 100%)!important;color:#fff!important;border:none!important;
  border-radius:16px!important;padding:1.5rem 3rem!important;font-size:1.2rem!important;font-weight:700!important;
  box-shadow:0 4px 20px rgba(139,92,246,.3)!important;min-width:250px!important;height:56px!important;
  transition:all .3s cubic-bezier(.4,0,.2,1)!important;cursor:pointer!important;
}
.stButton>button:hover{transform:translateY(-2px)!important;box-shadow:0 8px 30px rgba(139,92,246,.5)!important;}
</style>
""", unsafe_allow_html=True)

# ================================
# HELPER
# ================================
def run_workflow_webhook(files):
    try:
        r = requests.post(
            "https://sorepco-automation.app.n8n.cloud/webhook/Zautomation",
            files=files, timeout=1000, stream=True
        )
        if r.status_code == 200:
            try:
                return True, r.json()
            except:
                return True, {"message": "Processing completed", "raw_response": r.text}
        return False, f"Webhook returned {r.status_code}: {r.text}"
    except requests.exceptions.Timeout:
        return False, "Request timed out (2 min). Workflow may still be running."
    except Exception as e:
        return False, f"Call failed: {e}"

# ================================
# HERO
# ================================
st.markdown("""
<div class="hero-container">
  <div class="hero-card">
    <div class="title-gradient">SOREPCO AUTOMATION</div>
    <p class="hero-subtitle">
      Interface nouvelle génération pour l'extraction automatique<br/>
      et l'attribution des codes NGP
    </p>
  </div>
</div>
""", unsafe_allow_html=True)

# ================================
# UPLOADER
# ================================
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0

uploaded_files = st.file_uploader(
    "PDFs", type=["pdf"], accept_multiple_files=True,
    label_visibility="collapsed", key=f"up_{st.session_state.uploader_key}"
)

# ================================
# PROCESS
# ================================
if uploaded_files:
    if st.button("🚀 START", use_container_width=True):
        files = [("files", (f.name, f, "application/pdf")) for f in uploaded_files]
        start = time.time()
        with st.spinner("⚙️ Workflow en cours…"):
            ok, result = run_workflow_webhook(files)

        if ok:
            st.success("🎊 Extraction terminée !")
            st.session_state.results = result
            st.session_state.proc_time = round(time.time() - start, 1)
        else:
            st.error(result)

# ================================
# RESULTS
# ================================
if res := st.session_state.get("results"):
    # Normalize
    if isinstance(res, list):
        df = pd.DataFrame(res)
    elif isinstance(res, dict) and "data" in res:
        df = pd.DataFrame(res["data"])
    else:
        df = pd.DataFrame([res])

    st.write(f"⏱ Temps : {st.session_state.get('proc_time',0)} s")

    st.dataframe(df, use_container_width=True)

    excel = BytesIO()
    df.to_excel(excel, index=False)
    excel.seek(0)
    st.download_button("📥 Exporter vers Excel", excel,
                       f"sorepco_export_{int(time.time())}.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    if st.button("🔄 Nouveau traitement"):
        for k in ("results", "proc_time"):
            st.session_state.pop(k, None)
        st.session_state.uploader_key += 1
        st.experimental_rerun()

# ================================
# FOOTER
# ================================
st.markdown("""
<div style="text-align:center;margin-top:3rem;padding:2rem 0;color:#b8c6db;font-size:.9rem">
✨ Conçu avec passion par <strong style="
background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);
-webkit-background-clip:text;background-clip:text;color:transparent;">Firas Zouaghi</strong>
 • Propulsé par l'IA nouvelle génération
</div>
""", unsafe_allow_html=True)
