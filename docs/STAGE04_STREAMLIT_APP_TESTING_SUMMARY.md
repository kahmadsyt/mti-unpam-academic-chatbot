# STAGE 04 — Streamlit App Finalization, Scenario Testing, and Deployment Readiness

## Ringkasan

Tahap 04 berfokus pada finalisasi aplikasi chatbot Streamlit, pengujian skenario, dan kesiapan project untuk demo/deployment sederhana.

## Konfigurasi Utama

- Metode chatbot: TF-IDF Vectorizer + Cosine Similarity
- Threshold final sementara: `0.31`
- Total FAQ: `100`
- Total kategori FAQ: `11`
- Total scenario testing: `24`

## Hasil Scenario Testing

| Metrik | Nilai |
|---|---:|
| Total pertanyaan uji | 24 |
| Accuracy | 91.67% |
| Answered count | 18 |
| Fallback count | 6 |
| Average similarity | 0.6069 |

## Output File

- `outputs/stage04/scenario_questions_stage04.csv`
- `outputs/stage04/scenario_testing_results.csv`
- `outputs/stage04/stage04_app_readiness_summary.csv`
- `outputs/stage04/scenario_testing_summary_by_type.csv`
- `outputs/stage04/scenario_testing_error_analysis.csv`
- `outputs/stage04/figures/01_scenario_type_distribution.png`
- `outputs/stage04/figures/02_predicted_status_distribution.png`
- `outputs/stage04/figures/03_predicted_category_distribution.png`

## Interpretasi

Hasil pengujian digunakan untuk melihat apakah chatbot mampu menjawab pertanyaan yang masih berada dalam cakupan akademik MTI UNPAM dan menolak secara aman pertanyaan yang berada di luar cakupan. Kategori `fallback` tetap dipertahankan sebagai kontrol agar chatbot tidak memaksakan jawaban ketika similarity score rendah atau pertanyaan tidak relevan.

## Deployment Readiness Checklist

- [x] Dataset FAQ tersedia di `data/faq_mti_unpam.csv`
- [x] Evaluation questions tersedia di `data/evaluation_questions.csv`
- [x] Utility chatbot terpisah di `utils/chatbot_utils.py`
- [x] Aplikasi Streamlit tersedia di `app.py`
- [x] Scenario testing tersedia di `run_stage04_scenario_testing.py`
- [x] Output scenario testing tersedia di `outputs/stage04/`
- [x] Dokumentasi tersedia di `docs/STAGE04_STREAMLIT_APP_TESTING_SUMMARY.md`

## Catatan Batasan

Project ini masih merupakan prototype akademik. Informasi administratif terbaru seperti biaya kuliah, jadwal PMB, kebijakan akademik, dan struktur kurikulum resmi tetap perlu diverifikasi ke kanal resmi kampus.
