from pathlib import Path
from functools import lru_cache
import re
import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# =========================================================
# Konfigurasi dasar
# =========================================================
DEFAULT_THRESHOLD = 0.31

INDONESIAN_STOPWORDS = [
    "apa", "itu", "yang", "di", "ke", "dari", "dan", "atau", "pada",
    "untuk", "dengan", "dalam", "adalah", "saya", "ingin", "mau",
    "bisa", "kah", "ya", "dong", "tolong", "jelaskan", "sebutkan"
]


# =========================================================
# Path resolver
# =========================================================
def get_project_root() -> Path:
    """
    Mencari root project secara otomatis berdasarkan keberadaan folder data.
    Aman digunakan baik dari Streamlit, terminal, maupun notebook.
    """
    current = Path(__file__).resolve()

    candidates = [
        current.parent.parent,
        Path.cwd(),
        Path.cwd().parent,
    ]

    for candidate in candidates:
        if (candidate / "data" / "faq_mti_unpam.csv").exists():
            return candidate.resolve()

    for parent in current.parents:
        if (parent / "data" / "faq_mti_unpam.csv").exists():
            return parent.resolve()

    return current.parent.parent.resolve()


def get_faq_path() -> Path:
    return get_project_root() / "data" / "faq_mti_unpam.csv"


# =========================================================
# Text preprocessing
# =========================================================
def preprocess_text(text: str) -> str:
    """
    Preprocessing ringan:
    - lowercase
    - hapus karakter non-alfanumerik
    - rapikan spasi
    """
    text = str(text).lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def detect_column(df: pd.DataFrame, candidates: list[str]) -> str:
    """
    Mendeteksi nama kolom secara fleksibel.
    """
    lower_map = {col.lower().strip(): col for col in df.columns}

    for candidate in candidates:
        if candidate.lower() in lower_map:
            return lower_map[candidate.lower()]

    raise ValueError(
        f"Kolom tidak ditemukan. Kandidat yang dicari: {candidates}. "
        f"Kolom tersedia: {list(df.columns)}"
    )


def detect_faq_columns(df: pd.DataFrame):
    question_col = detect_column(
        df,
        ["question", "pertanyaan", "user_question", "faq_question"]
    )

    answer_col = detect_column(
        df,
        ["answer", "jawaban", "response", "bot_answer", "faq_answer"]
    )

    try:
        category_col = detect_column(
            df,
            ["category", "kategori", "label", "intent"]
        )
    except ValueError:
        category_col = None

    return question_col, answer_col, category_col


# =========================================================
# Keyword guard untuk mencegah false positive
# =========================================================
def keyword_guard_response(user_question: str):
    """
    Keyword guard digunakan untuk istilah akademik penting agar chatbot
    tidak salah mengambil jawaban dari kategori lain.
    """
    q = preprocess_text(user_question)

    # -----------------------------------------------------
    # Guard: kurikulum / semester
    # -----------------------------------------------------
    kurikulum_keywords = [
        "kurikulum",
        "semester 1 sampai 4",
        "semester satu sampai empat",
        "mata kuliah semester 1",
        "mata kuliah semester 2",
        "mata kuliah semester 3",
        "mata kuliah semester 4",
        "semester satu",
        "semester dua",
        "semester tiga",
        "semester empat",
    ]

    if any(keyword in q for keyword in kurikulum_keywords):
        return {
            "answer": (
                "Secara umum, kurikulum Program Magister Teknik Informatika terdiri dari mata kuliah dasar, "
                "mata kuliah keahlian, peminatan, metodologi penelitian, seminar/proposal, dan tesis. "
                "Pada dataset chatbot ini, contoh struktur akademik yang dikenali adalah:\n\n"
                "**Semester 1**: Algoritma Analisis, Data Mining, Modelling and Optimization, "
                "serta Sistem Komputer dan Jaringan.\n\n"
                "**Semester 2**: mata kuliah lanjutan yang mendukung penguatan teori, praktik komputasi, "
                "pengembangan sistem, dan metodologi penelitian.\n\n"
                "**Semester 3**: mata kuliah peminatan, pendalaman topik riset, serta persiapan proposal tesis.\n\n"
                "**Semester 4**: penyusunan dan penyelesaian tesis.\n\n"
                "Catatan: rincian resmi kurikulum tetap perlu mengacu pada dokumen akademik terbaru dari program studi."
            ),
            "category": "kurikulum",
            "similarity_score": 1.0,
            "matched_question": "keyword_guard:kurikulum",
            "is_fallback": False,
        }

    # -----------------------------------------------------
    # Guard: peminatan
    # -----------------------------------------------------
    peminatan_keywords = [
        "peminatan",
        "konsentrasi",
        "data science",
        "pilihan peminatan",
        "minat di mti",
        "peminatan di mti",
        "peminatan mti unpam",
    ]

    if any(keyword in q for keyword in peminatan_keywords):
        return {
            "answer": (
                "Peminatan pada Program Magister Teknik Informatika umumnya digunakan untuk membantu mahasiswa "
                "memperdalam bidang tertentu sesuai minat akademik dan rencana riset. "
                "Dalam konteks chatbot ini, peminatan yang relevan antara lain **Data Science**, "
                "pengembangan sistem informasi, jaringan dan infrastruktur, serta bidang informatika lain "
                "yang mendukung penelitian tesis.\n\n"
                "Untuk mahasiswa yang tertarik pada **Data Science**, topik yang dapat dipelajari mencakup "
                "Data Mining, Machine Learning, Natural Language Processing, analisis data, sistem rekomendasi, "
                "dan visualisasi data."
            ),
            "category": "peminatan",
            "similarity_score": 1.0,
            "matched_question": "keyword_guard:peminatan",
            "is_fallback": False,
        }

    # -----------------------------------------------------
    # Guard: tesis
    # -----------------------------------------------------
    tesis_keywords = [
        "tesis",
        "thesis",
        "penelitian akhir",
        "proposal tesis",
        "topik tesis",
        "dibahas pada tesis",
    ]

    if any(keyword in q for keyword in tesis_keywords):
        return {
            "answer": (
                "Tesis pada Program Magister Teknik Informatika merupakan penelitian akhir mahasiswa "
                "yang dilakukan secara sistematis untuk menyelesaikan masalah berbasis teknologi, data, "
                "atau sistem informasi. Topiknya dapat berkaitan dengan Data Mining, Data Science, "
                "Machine Learning, Natural Language Processing, sistem rekomendasi, jaringan komputer, "
                "keamanan informasi, atau bidang informatika lain sesuai peminatan dan arahan dosen pembimbing."
            ),
            "category": "tesis",
            "similarity_score": 1.0,
            "matched_question": "keyword_guard:tesis",
            "is_fallback": False,
        }

    # -----------------------------------------------------
    # Guard: out-of-scope umum
    # -----------------------------------------------------
    out_scope_keywords = [
        "nasi goreng",
        "masak",
        "resep",
        "bitcoin",
        "saham",
        "cuaca",
        "password wifi",
        "harga emas",
        "prediksi togel",
        "film terbaru",
    ]

    if any(keyword in q for keyword in out_scope_keywords):
        return {
            "answer": (
                "Maaf, pertanyaan tersebut berada di luar cakupan MTI Assistant UNPAM. "
                "Chatbot ini difokuskan untuk menjawab informasi akademik seputar Program Magister Teknik Informatika, "
                "mata kuliah, peminatan, tesis, Data Mining, Data Science, dan topik pembelajaran terkait."
            ),
            "category": "fallback",
            "similarity_score": 0.0,
            "matched_question": "keyword_guard:out_of_scope",
            "is_fallback": True,
        }

    return None


# =========================================================
# Load dataset dan bangun TF-IDF
# =========================================================
@lru_cache(maxsize=1)
def load_chatbot_resources():
    """
    Memuat dataset FAQ dan membangun TF-IDF matrix.
    Fungsi ini di-cache agar Streamlit lebih ringan.
    """
    faq_path = get_faq_path()

    if not faq_path.exists():
        raise FileNotFoundError(f"Dataset FAQ tidak ditemukan: {faq_path}")

    df = pd.read_csv(faq_path).fillna("")

    question_col, answer_col, category_col = detect_faq_columns(df)

    df["_processed_question"] = df[question_col].apply(preprocess_text)

    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=3000,
        stop_words=INDONESIAN_STOPWORDS,
    )

    tfidf_matrix = vectorizer.fit_transform(df["_processed_question"])

    return df, vectorizer, tfidf_matrix, question_col, answer_col, category_col


def build_tfidf_matrix(df: pd.DataFrame):
    """
    Fungsi tambahan untuk kompatibilitas notebook lama.
    """
    question_col, _, _ = detect_faq_columns(df)
    processed_questions = df[question_col].fillna("").apply(preprocess_text)

    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=3000,
        stop_words=INDONESIAN_STOPWORDS,
    )

    tfidf_matrix = vectorizer.fit_transform(processed_questions)

    return vectorizer, tfidf_matrix


# =========================================================
# Core retrieval function
# =========================================================
def retrieve_answer(
    user_question: str,
    df: pd.DataFrame,
    vectorizer: TfidfVectorizer,
    tfidf_matrix,
    threshold: float = DEFAULT_THRESHOLD,
):
    """
    Fungsi inti pencarian jawaban berbasis TF-IDF dan cosine similarity.
    """
    question_col, answer_col, category_col = detect_faq_columns(df)

    processed_question = preprocess_text(user_question)
    question_vector = vectorizer.transform([processed_question])

    similarity_scores = cosine_similarity(question_vector, tfidf_matrix).flatten()

    best_index = int(np.argmax(similarity_scores))
    best_score = float(similarity_scores[best_index])

    matched_question = str(df.iloc[best_index][question_col])
    category = str(df.iloc[best_index][category_col]) if category_col else ""

    if best_score < threshold:
        return {
            "answer": (
                "Maaf, saya belum menemukan jawaban yang cukup sesuai pada dataset FAQ. "
                "Silakan ajukan pertanyaan lain yang masih berkaitan dengan Program Magister Teknik Informatika, "
                "mata kuliah, peminatan, tesis, Data Mining, Data Science, atau topik akademik terkait."
            ),
            "category": "fallback",
            "similarity_score": best_score,
            "matched_question": matched_question,
            "is_fallback": True,
        }

    return {
        "answer": str(df.iloc[best_index][answer_col]),
        "category": category,
        "similarity_score": best_score,
        "matched_question": matched_question,
        "is_fallback": False,
    }


# =========================================================
# Public function untuk Streamlit
# =========================================================
def chatbot_response(user_question: str, threshold: float = DEFAULT_THRESHOLD):
    """
    Fungsi utama yang dipakai oleh app.py.
    Cukup dipanggil dengan:
        chatbot_response("Apa itu Data Mining?")
    """
    guard_result = keyword_guard_response(user_question)
    if guard_result is not None:
        return guard_result

    df, vectorizer, tfidf_matrix, _, _, _ = load_chatbot_resources()

    return retrieve_answer(
        user_question=user_question,
        df=df,
        vectorizer=vectorizer,
        tfidf_matrix=tfidf_matrix,
        threshold=threshold,
    )


# =========================================================
# Backward compatibility untuk notebook/script lama
# =========================================================
def get_chatbot_response(
    user_question: str,
    df: pd.DataFrame | None = None,
    vectorizer: TfidfVectorizer | None = None,
    tfidf_matrix=None,
    threshold: float = DEFAULT_THRESHOLD,
    return_details: bool = True,
):
    """
    Fungsi kompatibilitas agar kode lama tetap berjalan.

    Bisa dipanggil dengan format lama:
        get_chatbot_response(question, df, vectorizer, tfidf_matrix)

    Bisa juga dipanggil dengan format baru:
        get_chatbot_response(question)
    """
    guard_result = keyword_guard_response(user_question)
    if guard_result is not None:
        return guard_result if return_details else guard_result["answer"]

    if df is None or vectorizer is None or tfidf_matrix is None:
        result = chatbot_response(user_question, threshold=threshold)
        return result if return_details else result["answer"]

    result = retrieve_answer(
        user_question=user_question,
        df=df,
        vectorizer=vectorizer,
        tfidf_matrix=tfidf_matrix,
        threshold=threshold,
    )

    return result if return_details else result["answer"]


# =========================================================
# Utility untuk debugging cepat
# =========================================================
def debug_chatbot(user_question: str, threshold: float = DEFAULT_THRESHOLD):
    """
    Menampilkan hasil lengkap untuk debugging.
    """
    result = chatbot_response(user_question, threshold=threshold)
    return {
        "question": user_question,
        "answer": result.get("answer"),
        "category": result.get("category"),
        "similarity_score": result.get("similarity_score"),
        "matched_question": result.get("matched_question"),
        "is_fallback": result.get("is_fallback"),
    }