# Ringkasan TAHAP 02 — Dataset Validation, Error Analysis, Threshold Tuning, dan Evaluasi Kinerja Chatbot

## 1. Status Dataset

- Dataset FAQ: 34 baris.
- Jumlah kategori FAQ: 10 kategori.
- Shape TF-IDF matrix: (34, 208).
- Dataset evaluasi: 7 pertanyaan uji.
- Coverage kategori evaluasi: 5 dari 11 kategori termasuk fallback.

## 2. Hasil Evaluasi Baseline

- Threshold awal: 0.25.
- Akurasi baseline: 71.43% (5/7 benar).
- Jumlah error baseline: 2.
- Error utama baseline berasal dari pertanyaan out-of-scope yang masih dianggap mirip dengan pertanyaan FAQ.

## 3. Threshold Tuning

- Threshold terbaik pada data evaluasi saat ini berada pada rentang 0.305–0.325.
- Threshold rekomendasi sementara: 0.310.
- Akurasi pada threshold rekomendasi: 100.00% (7/7 benar).

## 4. Catatan Akademik

Peningkatan akurasi setelah threshold tuning belum boleh diklaim sebagai performa final karena jumlah pertanyaan evaluasi masih sangat kecil. Hasil ini lebih tepat disebut sebagai evaluasi awal dan dasar untuk memperbaiki dataset FAQ, pertanyaan uji, serta strategi fallback.

## 5. Rekomendasi Perbaikan

1. Tambahkan variasi pertanyaan untuk setiap kategori, minimal 3–5 variasi per FAQ penting.
2. Perluas evaluation_questions.csv dari 7 pertanyaan menjadi minimal 30–50 pertanyaan uji.
3. Tambahkan lebih banyak pertanyaan out-of-scope seperti biaya kuliah, pendaftaran, resep makanan, jadwal kampus, atau topik non-MTI.
4. Tambahkan stopwords Bahasa Indonesia sederhana agar kata umum seperti saya, apa, dan suka tidak terlalu memengaruhi similarity.
5. Pisahkan kategori resmi akademik, rekomendasi peminatan, prospek karier, dan fallback agar evaluasi lebih jelas.
6. Validasi jawaban berbasis sumber resmi jika chatbot akan dipakai sebagai kanal informasi publik.
