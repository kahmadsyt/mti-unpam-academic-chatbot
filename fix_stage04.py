from pathlib import Path
import re
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent
FAQ_PATH = PROJECT_ROOT / "data" / "faq_mti_unpam.csv"
EVAL_PATH = PROJECT_ROOT / "data" / "evaluation_questions.csv"

if not FAQ_PATH.exists():
    raise FileNotFoundError(f"FAQ file tidak ditemukan: {FAQ_PATH}")

faq_df = pd.read_csv(FAQ_PATH).fillna("")

new_faq_rows = [
    {
        "question": "Apa yang dibahas pada tesis?",
        "answer": (
            "Tesis pada program Magister Teknik Informatika membahas penelitian akhir mahasiswa "
            "yang dilakukan secara sistematis untuk menyelesaikan masalah berbasis teknologi, data, "
            "atau sistem informasi. Topiknya dapat berkaitan dengan Data Mining, Data Science, "
            "Machine Learning, NLP, sistem rekomendasi, jaringan komputer, keamanan informasi, "
            "atau bidang informatika lain sesuai peminatan dan arahan dosen pembimbing."
        ),
        "category": "tesis",
    },
    {
        "question": "Apa itu tesis di program Magister Teknik Informatika?",
        "answer": (
            "Tesis adalah karya ilmiah akhir pada jenjang magister yang menunjukkan kemampuan mahasiswa "
            "dalam merumuskan masalah, menelaah teori, memilih metode penelitian, mengolah data, "
            "menganalisis hasil, dan menarik kesimpulan secara akademik."
        ),
        "category": "tesis",
    },
    {
        "question": "Apakah tesis MTI harus berkaitan dengan Data Mining?",
        "answer": (
            "Tesis MTI tidak selalu harus berkaitan dengan Data Mining. Namun, bagi mahasiswa dengan "
            "peminatan Data Science, topik seperti Data Mining, Machine Learning, NLP, sistem rekomendasi, "
            "analisis sentimen, klasifikasi, clustering, atau predictive analytics sangat relevan untuk dikembangkan."
        ),
        "category": "tesis",
    },
    {
        "question": "Contoh topik tesis Data Science apa saja?",
        "answer": (
            "Contoh topik tesis Data Science antara lain analisis sentimen, klasifikasi teks, prediksi performa akademik, "
            "sistem rekomendasi, deteksi anomali, clustering perilaku pengguna, topic modeling, chatbot akademik, "
            "dan dashboard analitik berbasis data."
        ),
        "category": "tesis",
    },
    {
        "question": "Apa perbedaan tugas kuliah dan tesis?",
        "answer": (
            "Tugas kuliah biasanya digunakan untuk mengukur pemahaman materi pada satu mata kuliah tertentu, "
            "sedangkan tesis merupakan penelitian akhir yang lebih mendalam, terstruktur, menggunakan metodologi ilmiah, "
            "serta menghasilkan kontribusi akademik atau praktis."
        ),
        "category": "tesis",
    },
]

def normalize_text(text):
    text = str(text).lower().strip()
    text = re.sub(r"\s+", " ", text)
    return text

def align_row_to_columns(df, row):
    aligned = {col: "" for col in df.columns}

    column_map = {col.lower().strip(): col for col in df.columns}

    synonyms = {
        "question": ["question", "pertanyaan", "user_question"],
        "answer": ["answer", "jawaban", "response", "bot_answer"],
        "category": ["category", "kategori", "label"],
    }

    for key, value in row.items():
        for candidate in synonyms.get(key, [key]):
            if candidate in column_map:
                aligned[column_map[candidate]] = value
                break

    return aligned

question_col = None
for candidate in ["question", "pertanyaan", "user_question"]:
    for col in faq_df.columns:
        if col.lower().strip() == candidate:
            question_col = col
            break
    if question_col:
        break

if question_col is None:
    raise ValueError("Kolom pertanyaan tidak ditemukan. Pastikan ada kolom question/pertanyaan.")

existing_questions = set(faq_df[question_col].apply(normalize_text))

rows_to_add = []
for row in new_faq_rows:
    if normalize_text(row["question"]) not in existing_questions:
        rows_to_add.append(align_row_to_columns(faq_df, row))

if rows_to_add:
    faq_df = pd.concat([faq_df, pd.DataFrame(rows_to_add)], ignore_index=True)
    faq_df.to_csv(FAQ_PATH, index=False, encoding="utf-8")
    print(f"[OK] {len(rows_to_add)} FAQ tesis berhasil ditambahkan.")
else:
    print("[INFO] FAQ tesis sudah ada. Tidak ada data baru ditambahkan.")

print(f"[INFO] FAQ terbaru: {FAQ_PATH}")
print(f"[INFO] Shape FAQ: {faq_df.shape}")

# Tambahkan evaluation questions jika file tersedia
if EVAL_PATH.exists():
    eval_df = pd.read_csv(EVAL_PATH).fillna("")

    new_eval_rows = [
        {
            "question": "Apa yang dibahas pada tesis?",
            "expected_category": "tesis",
            "expected_answer_keyword": "penelitian akhir",
            "expected_is_fallback": False,
        },
        {
            "question": "Apa contoh topik tesis Data Science?",
            "expected_category": "tesis",
            "expected_answer_keyword": "Data Science",
            "expected_is_fallback": False,
        },
        {
            "question": "Apakah tesis harus menggunakan data?",
            "expected_category": "tesis",
            "expected_answer_keyword": "metodologi",
            "expected_is_fallback": False,
        },
    ]

    eval_question_col = None
    for candidate in ["question", "pertanyaan", "user_question"]:
        for col in eval_df.columns:
            if col.lower().strip() == candidate:
                eval_question_col = col
                break
        if eval_question_col:
            break

    if eval_question_col:
        existing_eval_questions = set(eval_df[eval_question_col].apply(normalize_text))

        aligned_eval_rows = []
        for row in new_eval_rows:
            if normalize_text(row["question"]) not in existing_eval_questions:
                aligned = {col: "" for col in eval_df.columns}
                lower_cols = {col.lower().strip(): col for col in eval_df.columns}

                for key, value in row.items():
                    if key in lower_cols:
                        aligned[lower_cols[key]] = value

                aligned_eval_rows.append(aligned)

        if aligned_eval_rows:
            eval_df = pd.concat([eval_df, pd.DataFrame(aligned_eval_rows)], ignore_index=True)
            eval_df.to_csv(EVAL_PATH, index=False, encoding="utf-8")
            print(f"[OK] {len(aligned_eval_rows)} evaluation questions tesis berhasil ditambahkan.")
        else:
            print("[INFO] Evaluation questions tesis sudah ada.")
    else:
        print("[WARN] Kolom question pada evaluation_questions.csv tidak ditemukan.")

print("[DONE] Perbaikan dataset tesis selesai.")