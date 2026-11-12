# OpenMLE-fast task

Task ID: `prediksi-status-akademik-mahasiswa@1`

Native metric: `StudentAcademicStatusMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2761 bytes)
- `data/sample_submission.csv` (1841 bytes); columns: ["id", "prob_Lulus"]
- `data/test.csv` (7127 bytes); columns: ["id", "Jenis Kelamin", "Umur", "Status Menikah", "Kehadiran (%)", "Partisipasi Diskusi (skor)", "Nilai Tugas (rata-rata)", "Aktivitas E-Learning (skor)", "IPK"]
- `data/train.csv` (17412 bytes); columns: ["Jenis Kelamin", "Umur", "Status Menikah", "Kehadiran (%)", "Partisipasi Diskusi (skor)", "Nilai Tugas (rata-rata)", "Aktivitas E-Learning (skor)", "IPK", "Status Akademik"]

## Public description

Prediksi Status Akademik Mahasiswa (Binary Probabilistic Classification)

Problem statement
Anda diminta membangun model yang memprediksi probabilitas seorang mahasiswa berstatus Lulus. Input adalah data tabular per mahasiswa berisi demografi, keterlibatan/aktivitas, dan performa akademik. Output yang diharapkan adalah probabilitas p(Lulus) untuk setiap baris pada test.csv. Peringkat di leaderboard ditentukan oleh ROC AUC terhadap kelas positif Lulus.

Data files
- train.csv: fitur terstruktur + kolom label Status Akademik.
- test.csv: fitur terstruktur tanpa label, ditambah kolom id untuk penyelarasan pengiriman (submission).
- sample_submission.csv: contoh format pengiriman berisi kolom id dan prob_Lulus.

Fitur yang tersedia
Gunakan seluruh fitur berikut (semua berasal dari sheet yang sama) dan label:
- Jenis Kelamin (kategori)
- Umur (integer)
- Status Menikah (kategori)
- Kehadiran (%) (integer, 40–100)
- Partisipasi Diskusi (skor) (integer, 40–100)
- Nilai Tugas (rata-rata) (integer, 40–100)
- Aktivitas E-Learning (skor) (integer, 40–100)
- IPK (float, ~1.50–3.99)
- Label: Status Akademik (nilai: Lulus atau Tidak) — hanya ada di train.csv
Catatan: Kolom Nama (PII) telah dihilangkan dari berkas akhir. Kolom id pada test.csv semata untuk penyelarasan baris dan tidak relevan sebagai fitur prediktif.

Tugas dan pengiriman
- Latih model pada train.csv untuk memetakan fitur ke probabilitas Lulus.
- Buat prediksi probabilitas untuk setiap baris pada test.csv dan simpan sebagai berkas CSV dengan tepat dua kolom: id, prob_Lulus.
- Nilai prob_Lulus harus berada pada [0, 1]. Urutan baris bebas, tetapi id harus cocok satu-per-satu dengan id pada test.csv tanpa duplikasi atau baris hilang.

Evaluasi
- Metrik: ROC AUC pada kelas positif Lulus menggunakan kolom prob_Lulus.
- Alasan pemilihan metrik: ROC AUC bersifat threshold-free dan adil pada ketidakseimbangan kelas sedang. Metrik ini menilai kemampuan model meranking mahasiswa Lulus lebih tinggi daripada Tidak di seluruh ambang keputusan.
- Validasi format submission: file submission akan diverifikasi ketat (kolom, rentang nilai, duplikasi id, dan kesesuaian set id dengan test.csv).

Catatan penting
- Disarankan melakukan praktek ML yang baik: encoding kategori (misal one-hot), penanganan skala numerik bila perlu, regularisasi/kalibrasi, dan evaluasi internal yang hati-hati untuk menghindari overfitting.

Ringkasan target
- Tujuan: prediksi probabilitas Lulus untuk setiap baris test.csv.
- File yang harus dikirim: CSV dengan kolom [id, prob_Lulus].
- Penilaian: ROC AUC pada kelas positif Lulus.
