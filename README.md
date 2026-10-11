# YouTube Video Downloader — Streamlit

Aplikasi Streamlit sederhana untuk mengunduh video yang Anda miliki, berlisensi terbuka, atau yang pemiliknya mengizinkan pengunduhan.

## Deploy ke GitHub + Streamlit Community Cloud

1. Buat repository GitHub baru, misalnya `yt-video-downloader`.
2. Upload `app.py`, `requirements.txt`, `packages.txt`, `.gitignore`, dan `README.md`.
3. Buka https://share.streamlit.io/ dan masuk dengan GitHub.
4. Pilih **Create app**, repository, branch `main`, file utama `app.py`.
5. Klik **Deploy**.

## Jalankan lokal

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## Catatan

- Unduh hanya konten milik sendiri, berlisensi terbuka, atau dengan izin pemilik.
- Tidak mengakali DRM, paywall, login, atau pembatasan akses.
- Streamlit Community Cloud memiliki batas sumber daya dan waktu; video besar/panjang mungkin gagal.
