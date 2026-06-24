# MTI UNPAM Academic Assistant

Prototype chatbot informasi akademik Program Magister Teknik Informatika UNPAM berbasis **Text Mining**, **TF-IDF Vectorizer**, **Cosine Similarity**, visualisasi dashboard, dan deployment menggunakan **Streamlit**.

## 1. Tujuan Project

Project ini dibuat untuk membantu calon mahasiswa memahami informasi dasar Program Magister Teknik Informatika UNPAM, seperti struktur semester, mata kuliah, peminatan, rekomendasi peminatan, tesis, dan prospek karier.

## 2. Metode

Metode utama yang digunakan:

1. Text preprocessing sederhana
2. TF-IDF Vectorizer
3. Cosine Similarity
4. Threshold-based fallback response
5. Evaluasi sederhana menggunakan pertanyaan uji
6. Visualisasi dashboard menggunakan Plotly
7. Deployment aplikasi dengan Streamlit

## 3. Struktur Folder

```text
mti-unpam-academic-chatbot/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .streamlit/
│   └── config.toml
├── data/
│   ├── faq_mti_unpam.csv
│   └── evaluation_questions.csv
├── notebooks/
│   └── 01_mti_unpam_academic_chatbot_tfidf_cosine_similarity.ipynb
├── outputs/
│   └── model_artifacts/
├── assets/
├── docs/
│   └── project_notes.md
└── utils/
    ├── __init__.py
    └── chatbot_utils.py
```

## 4. Cara Menjalankan di Laptop

### Membuat environment Conda

```bash
conda create -n mti-chatbot python=3.11 -y
conda activate mti-chatbot
pip install -r requirements.txt
```

### Menjalankan Streamlit

```bash
streamlit run app.py
```

## 5. Cara Menjalankan Notebook

```bash
conda activate mti-chatbot
jupyter notebook
```

Lalu buka file:

```text
notebooks/01_mti_unpam_academic_chatbot_tfidf_cosine_similarity.ipynb
```

## 6. Push ke GitHub

```bash
git init -b main
git add .
git commit -m "Initial commit - MTI UNPAM academic chatbot"
git remote add origin https://github.com/USERNAME/mti-unpam-academic-chatbot.git
git push -u origin main
```

Ganti `USERNAME` dengan username GitHub Anda.

## 7. Deploy ke Streamlit Community Cloud

1. Push project ke GitHub.
2. Login ke Streamlit Community Cloud.
3. Pilih **Create app**.
4. Pilih repository `mti-unpam-academic-chatbot`.
5. Pilih branch `main`.
6. Main file path: `app.py`.
7. Deploy.

## 8. Catatan Akademik

Aplikasi ini adalah prototype untuk tugas Data Mining/Text Mining. Dataset FAQ masih perlu divalidasi kembali jika akan digunakan sebagai kanal informasi resmi.
