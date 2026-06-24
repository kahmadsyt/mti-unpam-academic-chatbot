"""
Utility functions for MTI UNPAM Academic Assistant.
This module contains reusable functions for loading FAQ data, preprocessing text,
building a TF-IDF engine, generating chatbot responses, and evaluating test questions.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, Tuple

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


REQUIRED_COLUMNS = ["question", "answer", "category", "semester", "peminatan", "source_type"]


def load_faq_data(csv_path: str | Path) -> pd.DataFrame:
    """Load FAQ dataset and validate required columns."""
    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"FAQ dataset not found: {csv_path}")

    df = pd.read_csv(csv_path).fillna("")
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    df["question"] = df["question"].astype(str)
    df["answer"] = df["answer"].astype(str)
    df["category"] = df["category"].astype(str)
    return df


def preprocess_text(text: str) -> str:
    """Simple Indonesian text preprocessing for FAQ matching."""
    text = str(text).lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def build_tfidf_engine(df: pd.DataFrame) -> Tuple[TfidfVectorizer, object]:
    """Build TF-IDF vectorizer and matrix from FAQ questions."""
    vectorizer = TfidfVectorizer(
        preprocessor=preprocess_text,
        ngram_range=(1, 2),
        min_df=1,
        token_pattern=r"(?u)\b\w+\b",
    )
    tfidf_matrix = vectorizer.fit_transform(df["question"])
    return vectorizer, tfidf_matrix


def get_chatbot_response(
    user_question: str,
    df: pd.DataFrame,
    vectorizer: TfidfVectorizer,
    tfidf_matrix,
    threshold: float = 0.25,
) -> Dict[str, object]:
    """Return chatbot response using TF-IDF and cosine similarity."""
    if not str(user_question).strip():
        return {
            "answer": "Silakan masukkan pertanyaan terlebih dahulu.",
            "category": "empty_input",
            "similarity_score": 0.0,
            "matched_question": "",
            "status": "empty",
        }

    user_vector = vectorizer.transform([user_question])
    similarity_scores = cosine_similarity(user_vector, tfidf_matrix).flatten()
    best_index = int(similarity_scores.argmax())
    best_score = float(similarity_scores[best_index])

    if best_score < threshold:
        return {
            "answer": (
                "Maaf, saya belum memiliki informasi yang cukup untuk menjawab pertanyaan tersebut. "
                "Silakan ajukan pertanyaan seputar Program MTI UNPAM, kurikulum, peminatan, tesis, atau prospek karier."
            ),
            "category": "fallback",
            "similarity_score": round(best_score, 4),
            "matched_question": df.iloc[best_index]["question"],
            "status": "fallback",
        }

    selected = df.iloc[best_index]
    return {
        "answer": selected["answer"],
        "category": selected["category"],
        "semester": selected.get("semester", ""),
        "peminatan": selected.get("peminatan", ""),
        "similarity_score": round(best_score, 4),
        "matched_question": selected["question"],
        "status": "answered",
    }


def evaluate_questions(
    eval_df: pd.DataFrame,
    faq_df: pd.DataFrame,
    vectorizer: TfidfVectorizer,
    tfidf_matrix,
    threshold: float = 0.25,
) -> pd.DataFrame:
    """Evaluate chatbot against a simple test question dataset."""
    records = []
    for _, row in eval_df.iterrows():
        result = get_chatbot_response(row["test_question"], faq_df, vectorizer, tfidf_matrix, threshold)
        predicted_category = result["category"]
        expected_category = row.get("expected_category", "")
        records.append(
            {
                "test_question": row["test_question"],
                "expected_category": expected_category,
                "predicted_category": predicted_category,
                "similarity_score": result["similarity_score"],
                "status": result["status"],
                "is_correct": expected_category == predicted_category,
                "matched_question": result["matched_question"],
            }
        )
    return pd.DataFrame(records)
