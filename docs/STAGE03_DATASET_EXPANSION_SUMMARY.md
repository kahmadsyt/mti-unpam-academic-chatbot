# STAGE 03 — Dataset Expansion, FAQ Enrichment, dan Improvement Chatbot Response

## 1. Tujuan Tahap 03

Tahap 03 berfokus pada perluasan dataset FAQ, penambahan variasi pertanyaan/parafrase, penambahan contoh pertanyaan out-of-scope, perbaikan jawaban chatbot, evaluasi ulang, serta perbandingan performa sebelum dan sesudah dataset expansion.

## 2. Ringkasan Perubahan

| Komponen | Sebelum | Sesudah Tahap 03 |
|---|---:|---:|
| Jumlah FAQ | 34 | 100 |
| Jumlah kategori FAQ | 10 | 11 |
| Jumlah pertanyaan evaluasi | 7 | 47 |
| Threshold acuan Tahap 02 | 0.31 | 0.31 |
| Best threshold Tahap 03 | - | 0.25 |
| Akurasi baseline Tahap 01 | 71.43% | - |
| Akurasi Tahap 03 pada threshold 0.31 | - | 78.72% |
| Akurasi Tahap 03 best threshold | - | 78.72% |

## 3. Improvement yang Dilakukan

1. Dataset `faq_mti_unpam.csv` diperluas dengan variasi pertanyaan mengenai profil program, kurikulum semester, peminatan, rekomendasi peminatan, tesis, prospek karier, dan fallback.
2. Dataset `evaluation_questions.csv` diperluas agar pengujian tidak hanya bergantung pada sedikit pertanyaan.
3. Jawaban chatbot dibuat lebih informatif dan natural, tetapi tetap menjaga batasan bahwa chatbot bukan kanal resmi PMB.
4. Fungsi chatbot diperbaiki agar kategori `fallback` pada FAQ eksplisit tetap ditampilkan sebagai status fallback.
5. Default threshold pada utility dan Streamlit diarahkan ke 0.31 sesuai rekomendasi Tahap 02.
6. Output evaluasi dan visualisasi Tahap 03 disimpan pada folder `outputs/stage03/`.

## 4. Catatan Akademik

Dataset tahap ini masih bersifat manual enrichment untuk kebutuhan prototype akademik. Informasi yang bersifat dinamis seperti biaya kuliah, jadwal PMB, persyaratan administrasi, dan kebijakan terbaru tidak dijawab secara deterministik oleh chatbot dan diarahkan ke kanal resmi.

## 5. File Output Penting

- `data/faq_mti_unpam.csv`
- `data/evaluation_questions.csv`
- `notebooks/03_dataset_expansion_faq_enrichment_improvement_chatbot_response.ipynb`
- `outputs/stage03/stage03_improvement_summary.csv`
- `outputs/stage03/threshold_tuning_results_stage03.csv`
- `outputs/stage03/evaluation_result_threshold_0_31_stage03.csv`
- `outputs/stage03/evaluation_result_best_threshold_stage03.csv`
- `outputs/stage03/figures/`

## 6. Kesimpulan

Tahap 03 memperkuat chatbot dari sisi cakupan informasi, variasi pertanyaan, fallback handling, dan evaluasi. Dengan dataset yang lebih besar, chatbot memiliki peluang lebih baik untuk menangani parafrase pengguna, sekaligus tetap membatasi jawaban pada ruang lingkup akademik MTI UNPAM.
