# OpenMLE-fast task

Task ID: `computer-price-prediction@1`

Native metric: `DesktopComputerPriceMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (867 bytes)
- `data/sample_submission.csv` (6711 bytes); columns: ["id", "Fiyat"]
- `data/test.csv` (96490 bytes); columns: ["id", "Marka", "İşlemci Tipi", "SSD Kapasitesi", "Ram (Sistem Belleği)", "Ekran Kartı", "Kapasite", "İşletim Sistemi", "Ekran Kartı Bellek Tipi", "Ekran Kartı Tipi", "Garanti Tipi", "Ram (Sistem Belleği) Tipi", "İşlemci Çekirdek Sayısı", "İşlemci Nesli", "İşlemci Modeli", "Çözünürlük", "Power Supply", "Kullanım Amacı", "Ekran Kartı Hafızası", "Temel İşlemci Hızı (GHz)", "Bağlantılar", "Cihaz Ağırlığı", "Ekran Boyutu", "İşlemci Frekansı", "Ekran Yenileme Hızı", "Panel Tipi", "Menşei", "Arttırılabilir Azami Bellek"]
- `data/train.csv` (405149 bytes); columns: ["id", "Marka", "Fiyat", "İşlemci Tipi", "SSD Kapasitesi", "Ram (Sistem Belleği)", "Ekran Kartı", "Kapasite", "İşletim Sistemi", "Ekran Kartı Bellek Tipi", "Ekran Kartı Tipi", "Garanti Tipi", "Ram (Sistem Belleği) Tipi", "İşlemci Çekirdek Sayısı", "İşlemci Nesli", "İşlemci Modeli", "Çözünürlük", "Power Supply", "Kullanım Amacı", "Ekran Kartı Hafızası", "Temel İşlemci Hızı (GHz)", "Bağlantılar", "Cihaz Ağırlığı", "Ekran Boyutu", "İşlemci Frekansı", "Ekran Yenileme Hızı", "Panel Tipi", "Menşei", "Arttırılabilir Azami Bellek"]

## Public description

```
description.txt (52 lines)
sample_submission.csv (495 lines)
test.csv (495 lines)
train.csv (1974 lines)```

-> sample_submission.csv has 494 rows and 2 columns.
The columns are: id, Fiyat

-> test.csv has 494 rows and 28 columns.
The columns are: id, Marka, İşlemci Tipi, SSD Kapasitesi, Ram (Sistem Belleği), Ekran Kartı, Kapasite, İşletim Sistemi, Ekran Kartı Bellek Tipi, Ekran Kartı Tipi, Garanti Tipi, Ram (Sistem Belleği) Tipi, İşlemci Çekirdek Sayısı, İşlemci Nesli, İşlemci Modeli... and 13 more columns

-> train.csv has 1973 rows and 29 columns.
The columns are: id, Marka, Fiyat, İşlemci Tipi, SSD Kapasitesi, Ram (Sistem Belleği), Ekran Kartı, Kapasite, İşletim Sistemi, Ekran Kartı Bellek Tipi, Ekran Kartı Tipi, Garanti Tipi, Ram (Sistem Belleği) Tipi, İşlemci Çekirdek Sayısı, İşlemci Nesli... and 14 more columns
