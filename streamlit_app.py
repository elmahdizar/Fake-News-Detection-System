<<<<<<< HEAD
import streamlit as st
import joblib
import requests
import os
import base64
from sklearn.exceptions import NotFittedError

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

# ── Load background image as base64 ──────────────────────────────────────────
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return None

# Look for the background image next to the script
base_dir = os.path.dirname(os.path.abspath(__file__))
bg_candidates = [
    os.path.join(base_dir, "fake_news_bg.png"),
    os.path.join(base_dir, "background.png"),
    os.path.join(base_dir, "1780939038556_image.png"),
]
bg_b64 = None
for path in bg_candidates:
    bg_b64 = get_base64_image(path)
    if bg_b64:
        break

# Build the background CSS: use image if available, else fallback to dark concrete look
if bg_b64:
    bg_css = f"""
    .stApp {{
        background-image: url("data:image/png;base64,{bg_b64}");
        background-size: cover;
        background-position: center center;
        background-attachment: fixed;
        background-repeat: no-repeat;
        min-height: 100vh;
    }}
    """
else:
    # Fallback: dark concrete/grunge gradient
    bg_css = """
    .stApp {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 50%, #1a1a1a 100%);
        min-height: 100vh;
    }
    """

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Tajawal', sans-serif !important;
}}

{bg_css}

/* Dark overlay so UI elements stay readable over the image */
.stApp::before {{
    content: '';
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.55);
    pointer-events: none;
    z-index: 0;
}}

/* Ensure all Streamlit content sits above the overlay */
.stApp > * {{
    position: relative;
    z-index: 1;
}}

/* Title */
h1 {{
    font-family: 'Tajawal', sans-serif !important;
    color: #ffffff !important;
    text-align: center;
    font-size: 2rem !important;
    padding: 1rem 0 0.5rem 0;
    letter-spacing: 1px;
    text-shadow: 0 2px 12px rgba(0,0,0,0.8);
}}

/* Left column (buttons side) */
[data-testid="column"]:first-child {{
    background: transparent;
    padding: 1rem;
}}

/* Right column (text area side) */
[data-testid="column"]:last-child {{
    background: transparent;
    padding: 1rem;
}}

/* Text area */
.stTextArea textarea {{
    background: rgba(0, 0, 0, 0.55) !important;
    border: 2px solid rgba(255,255,255,0.25) !important;
    border-radius: 12px !important;
    color: #f0f0f0 !important;
    font-family: 'Tajawal', sans-serif !important;
    font-size: 1rem !important;
    min-height: 320px !important;
}}

.stTextArea textarea:focus {{
    border-color: rgba(255,255,255,0.6) !important;
}}

/* Text input (URL) */
.stTextInput input {{
    background: rgba(0,0,0,0.55) !important;
    border: 2px solid rgba(255,255,255,0.25) !important;
    border-radius: 10px !important;
    color: #f0f0f0 !important;
    font-family: 'Tajawal', sans-serif !important;
}}

/* File uploader */
[data-testid="stFileUploader"] {{
    background: rgba(0,0,0,0.4) !important;
    border: 2px dashed rgba(255,255,255,0.3) !important;
    border-radius: 10px !important;
}}

/* All buttons */
.stButton > button {{
    width: 100% !important;
    background: rgba(0,0,0,0.45) !important;
    color: #ffffff !important;
    border: 2px solid rgba(255,255,255,0.4) !important;
    border-radius: 10px !important;
    font-family: 'Tajawal', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    padding: 0.6rem 1rem !important;
    transition: all 0.2s ease !important;
    margin-bottom: 0.5rem !important;
    backdrop-filter: blur(4px) !important;
}}

.stButton > button:hover {{
    background: rgba(255,255,255,0.18) !important;
    border-color: #ffffff !important;
    transform: translateY(-2px) !important;
}}

/* Labels */
label, .stTextInput label, .stTextArea label, .stFileUploader label {{
    color: #e0e0e0 !important;
    font-family: 'Tajawal', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    text-shadow: 0 1px 4px rgba(0,0,0,0.8) !important;
}}

/* Result banners */
.stSuccess, .stError, .stWarning, .stInfo {{
    border-radius: 10px !important;
    font-family: 'Tajawal', sans-serif !important;
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    backdrop-filter: blur(6px) !important;
}}

/* Divider */
hr {{
    border-color: rgba(255,255,255,0.2) !important;
}}

/* Caption */
.stCaption {{
    color: #cccccc !important;
    font-family: 'Tajawal', sans-serif !important;
    text-shadow: 0 1px 3px rgba(0,0,0,0.8) !important;
}}

/* Markdown text */
p, .stMarkdown p {{
    color: #e8e8e8 !important;
    text-shadow: 0 1px 4px rgba(0,0,0,0.7) !important;
}}
</style>
""", unsafe_allow_html=True)

# ── Title ─────────────────────────────────────────────────────────────────────
st.markdown("<h1>Fake News Detection System </h1>", unsafe_allow_html=True)

# ── Load model ────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [base_dir, os.path.join(base_dir, "Fake-News-Detection-System")]
    for folder in candidates:
        mp = os.path.join(folder, "fake_news_modelsvm.pkl")
        vp = os.path.join(folder, "tfidf_vectorizer.pkl")
        if os.path.exists(mp) and os.path.exists(vp):
            try:
                return joblib.load(mp), joblib.load(vp), None
            except Exception as e:
                return None, None, str(e)
    return None, None, "Fichiers .pkl introuvables."

model, vectorizer, load_error = load_model()
if load_error:
    st.error(f"Erreur modèle : {load_error}")

# ── Layout: left buttons | right text area ────────────────────────────────────
col_left, col_right = st.columns([1, 2])

with col_left:
    st.markdown("**📁 Importer un fichier .txt**")
    uploaded_file = st.file_uploader("", type=["txt"], label_visibility="collapsed")

    st.markdown("**🔗 Lien URL**")
    url_input = st.text_input("", placeholder="https://...", label_visibility="collapsed")

    st.markdown("** Contenus importés**")
    if uploaded_file:
        st.info(f" {uploaded_file.name}")
    elif url_input.strip():
        st.info(f"🔗 URL prête")
    else:
        st.caption("Aucun fichier ou URL")

with col_right:
    st.markdown("** Coller le texte**")
    pasted_text = st.text_area("", height=320, placeholder="Collez ici votre article ou titre...", label_visibility="collapsed")

# ── Analyser button (full width) ──────────────────────────────────────────────
st.markdown("---")
if st.button("🔍 Analyser", use_container_width=True):
    content = ""
    source = ""

    if uploaded_file:
        content = uploaded_file.read().decode("utf-8", errors="ignore")
        source = f"Fichier : {uploaded_file.name}"

    elif url_input.strip():
        with st.spinner("Récupération du texte..."):
            try:
                resp = requests.get(url_input.strip(), timeout=10, headers={"User-Agent": "Mozilla/5.0"})
                resp.raise_for_status()
                if BS4_AVAILABLE and "text/html" in resp.headers.get("Content-Type", ""):
                    soup = BeautifulSoup(resp.text, "html.parser")
                    for tag in soup(["script", "style", "nav", "footer"]):
                        tag.decompose()
                    paragraphs = [p.get_text(" ", strip=True) for p in soup.find_all("p") if len(p.get_text()) > 40]
                    content = "\n".join(paragraphs) or soup.get_text(" ", strip=True)
                else:
                    content = resp.text
                source = f"URL : {url_input.strip()}"
            except Exception as e:
                st.error(f"Impossible de récupérer l'URL : {e}")

    elif pasted_text.strip():
        content = pasted_text.strip()
        source = "Texte collé"

    if not content.strip():
        st.warning("Veuillez fournir un texte, un fichier ou une URL.")
    elif model is None:
        st.error("Modèle non disponible.")
    else:
        try:
            prediction = model.predict(vectorizer.transform([content]))[0]
            if prediction == 1:
                st.success(" TRUE NEWS")
            else:
                st.error("FAKE NEWS")
            st.caption(f"Source : {source} · {len(content.split())} mots")
        except NotFittedError:
            st.error("Le modèle n'est pas entraîné.")
        except Exception as e:
            st.error(f"Erreur : {e}")
=======
from pathlib import Path

import streamlit as st

from src.fake_news_detection.predict import load_artifacts, predict_news


st.set_page_config(page_title="Detection des fake news", page_icon="N", layout="centered")

st.title("Systeme de detection des fake news")
st.write("Collez un article de presse ou un titre pour le classer comme vrai ou faux.")


def artifact_candidates() -> list[Path]:
    project_root = Path(__file__).resolve().parent
    parent_root = project_root.parent
    return [
        project_root / "artifacts",
        parent_root,
    ]


@st.cache_resource
def get_pipeline():
    return load_artifacts(artifact_candidates())


text = st.text_area(
    "Texte de l'actualite",
    placeholder="Saisissez un titre ou le contenu d'un article ici...",
    height=220,
)

if st.button("Verifier l'information", type="primary"):
    if not text.strip():
        st.warning("Veuillez saisir un texte avant de lancer la prediction.")
    else:
        try:
            model, vectorizer, source_dir = get_pipeline()
            label = predict_news(text, model, vectorizer)

            st.caption(f"Artefacts du modele charges depuis : {source_dir}")
            if label == 1:
                st.success("Prediction : information vraie")
            else:
                st.error("Prediction : fausse information")
        except FileNotFoundError as exc:
            st.error(str(exc))
            st.info(
                "Ajoutez `fake_news_modelsvm.pkl` et `tfidf_vectorizer.pkl` dans le "
                "dossier `artifacts/`, ou laissez-les dans le dossier parent."
            )
>>>>>>> 25412cc (Initial starter project)
