# Fake News Detection System

Starter project for a Streamlit-based fake news detection app.

## Project Structure

```text
Fake-News-Detection-System/
|-- streamlit_app.py
|-- requirements.txt
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
2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the app:

```powershell
streamlit run streamlit_app.py
```

## Model Files

The app looks for these files in `artifacts/` first:

- `fake_news_modelsvm.pkl`
- `tfidf_vectorizer.pkl`

If they are not found there, it also checks the parent workspace so you can reuse existing local files during setup.

## Next Steps

- Add your trained model files to `artifacts/`
- Add datasets to `data/`
- Extend `src/fake_news_detection/predict.py` with preprocessing or retraining helpers
