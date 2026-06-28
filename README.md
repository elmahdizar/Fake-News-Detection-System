# Fake News Detection System

Streamlit app for detecting fake news using a trained SVM model and a TF-IDF vectorizer.

## Project Structure

```text
Fake-News-Detection-System/
|-- streamlit_app.py
|-- requirements.txt
|-- runtime.txt
|-- COMMANDES_STREAMLIT.md
|-- fake_news_modelsvm.pkl
|-- tfidf_vectorizer.pkl
|-- .gitignore
|-- src/
|   `-- fake_news_detection/
|       |-- __init__.py
|       `-- predict.py
|-- artifacts/
|   `-- README.md
`-- data/
    `-- README.md
```

## Quick Start

1. Create or activate a virtual environment.

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the app:

```powershell
streamlit run streamlit_app.py
```

If `streamlit` is not recognized:

```powershell
python -m streamlit run streamlit_app.py
```

## Model Files

The app needs these files:

- `fake_news_modelsvm.pkl`
- `tfidf_vectorizer.pkl`

Place them in the project root, next to `streamlit_app.py`.

## Streamlit Cloud Deployment

This project includes:

- `requirements.txt` for Python dependencies
- `runtime.txt` to use Python 3.11 on Streamlit Cloud

After editing files, push updates to GitHub:

```bash
git status
git add -A
git commit -m "Update Streamlit deployment files"
git push origin main
```

## Next Steps

- Add datasets to `data/`
- Extend `src/fake_news_detection/predict.py` with preprocessing or retraining helpers
