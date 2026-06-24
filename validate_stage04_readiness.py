from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent

required_files = [
    "app.py",
    "requirements.txt",
    "README.md",
    "data/faq_mti_unpam.csv",
    "data/evaluation_questions.csv",
    "utils/chatbot_utils.py",
    "notebooks/03_dataset_expansion_faq_enrichment_improvement_chatbot_response.ipynb",
    "docs/STAGE03_DATASET_EXPANSION_SUMMARY.md",
]

print("=" * 70)
print("VALIDASI KESIAPAN TAHAP 04")
print("=" * 70)
print(f"Project root: {PROJECT_ROOT}")
print("-" * 70)

all_pass = True

for file_path in required_files:
    full_path = PROJECT_ROOT / file_path
    if full_path.exists():
        print(f"[PASS] {file_path}")
    else:
        print(f"[FAIL] {file_path} tidak ditemukan")
        all_pass = False

print("-" * 70)

faq_path = PROJECT_ROOT / "data" / "faq_mti_unpam.csv"
eval_path = PROJECT_ROOT / "data" / "evaluation_questions.csv"

if faq_path.exists():
    faq_df = pd.read_csv(faq_path).fillna("")
    print(f"FAQ dataset shape        : {faq_df.shape}")
    print(f"Jumlah kategori FAQ      : {faq_df['category'].nunique() if 'category' in faq_df.columns else 'Kolom category tidak ada'}")
else:
    all_pass = False

if eval_path.exists():
    eval_df = pd.read_csv(eval_path).fillna("")
    print(f"Evaluation dataset shape : {eval_df.shape}")
else:
    all_pass = False

print("-" * 70)

if all_pass:
    print("STATUS: PASS - Project siap masuk Tahap 04.")
else:
    print("STATUS: FAIL - Masih ada file yang perlu diperbaiki.")

print("=" * 70)