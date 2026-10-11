import streamlit as st
import yt_dlp
import os, re, tempfile
from pathlib import Path

st.set_page_config(page_title="YT Video Downloader", page_icon="⬇️", layout="centered")
st.title("⬇️ YouTube Video Downloader")
st.caption("Unduh video yang kamu miliki atau yang izin unduhnya sudah kamu dapatkan.")

url = st.text_input("URL video YouTube", placeholder="https://www.youtube.com/watch?v=...")
quality = st.selectbox("Kualitas video", ["720p", "480p", "360p", "Audio saja (MP3)"], index=0)
st.warning("Gunakan hanya untuk video milik sendiri, berlisensi terbuka, atau yang pemiliknya mengizinkan pengunduhan. Hormati hak cipta dan ketentuan YouTube.")

def safe_name(name):
    name = re.sub(r'[\\\\/:*?"<>|]+', "_", name).strip(" ._")
    return (name[:100] or "youtube_video")

if st.button("Cari info video", use_container_width=True):
    if not url.strip():
        st.error("Masukkan URL video terlebih dahulu.")
    else:
        try:
            opts = {"quiet": True, "no_warnings": True, "noplaylist": True}
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url.strip(), download=False)
            st.session_state["video_info"] = {
                "url": url.strip(), "title": info.get("title", "youtube_video"),
                "duration": info.get("duration"), "uploader": info.get("uploader"),
                "thumbnail": info.get("thumbnail")
            }
        except Exception as e:
            st.error("Tidak dapat membaca video. Periksa URL atau coba lagi nanti.")
            st.caption(str(e)[:400])

info = st.session_state.get("video_info")
if info and info.get("url") == url.strip():
    st.subheader(info["title"])
    if info.get("thumbnail"):
        st.image(info["thumbnail"], use_container_width=True)
    meta=[]
    if info.get("uploader"): meta.append("Channel: "+str(info["uploader"]))
    if info.get("duration") is not None: meta.append(f"Durasi: {int(info['duration'])//60}:{int(info['duration'])%60:02d}")
    st.caption(" • ".join(meta))

if st.button("⬇️ Download", type="primary", use_container_width=True):
    if not url.strip():
        st.error("Masukkan URL video terlebih dahulu.")
    else:
        with st.spinner("Memproses video..."):
            try:
                outdir = Path(tempfile.mkdtemp(prefix="yt_download_"))
                audio_only = quality.startswith("Audio")
                if audio_only:
                    fmt = "bestaudio/best"
                    opts = {
                        "format": fmt, "outtmpl": str(outdir / "%(title).100s.%(ext)s"),
                        "noplaylist": True, "quiet": True,
                        "postprocessors": [{"key":"FFmpegExtractAudio","preferredcodec":"mp3","preferredquality":"192"}]
                    }
                else:
                    height = int(quality.replace("p",""))
                    opts = {
                        "format": f"bestvideo[height<={height}]+bestaudio/best[height<={height}]/best[height<={height}]",
                        "outtmpl": str(outdir / "%(title).100s.%(ext)s"),
                        "merge_output_format": "mp4", "noplaylist": True, "quiet": True
                    }
                with yt_dlp.YoutubeDL(opts) as ydl:
                    ydl.download([url.strip()])
                outputs = [p for p in outdir.iterdir() if p.is_file()]
                if not outputs:
                    st.error("File tidak ditemukan setelah proses download.")
                else:
                    path = outputs[0]
                    data = path.read_bytes()
                    mime = "audio/mpeg" if path.suffix.lower()==".mp3" else "video/mp4"
                    st.success("Selesai.")
                    st.download_button("Simpan "+path.name, data=data, file_name=safe_name(path.name), mime=mime, use_container_width=True)
                    if mime == "video/mp4":
                        st.video(data)
            except Exception as e:
                st.error("Download gagal. Bisa jadi video dibatasi, memerlukan login, atau formatnya tidak tersedia.")
                st.caption(str(e)[:600])

st.divider()
st.caption("Untuk deploy Streamlit Community Cloud, ukuran file dan batas waktu server dapat membatasi video panjang. Aplikasi ini tidak mengakali paywall, login, DRM, atau pembatasan akses.")
