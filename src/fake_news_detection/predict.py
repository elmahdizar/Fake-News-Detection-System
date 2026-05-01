from pathlib import Path

import joblib


MODEL_FILE = "fake_news_modelsvm.pkl"
VECTORIZER_FILE = "tfidf_vectorizer.pkl"


def _find_artifact_dir(search_roots: list[Path]) -> Path:
    for root in search_roots:
        model_path = root / MODEL_FILE
        vectorizer_path = root / VECTORIZER_FILE
        if model_path.exists() and vectorizer_path.exists():
            return root

    searched = ", ".join(str(path) for path in search_roots)
    raise FileNotFoundError(
        "Could not find both model files. Searched in: "
        f"{searched}"
    )


def load_artifacts(search_roots: list[Path]):
    artifact_dir = _find_artifact_dir(search_roots)
    model = joblib.load(artifact_dir / MODEL_FILE)
    vectorizer = joblib.load(artifact_dir / VECTORIZER_FILE)
    return model, vectorizer, artifact_dir


def predict_news(text: str, model, vectorizer) -> int:
    transformed_text = vectorizer.transform([text])
    prediction = model.predict(transformed_text)
    return int(prediction[0])
