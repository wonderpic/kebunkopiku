import streamlit as st
import pandas as pd
import os
import base64
from datetime import datetime, timedelta

# Konfigurasi Tampilan Utama Halaman HP
st.set_page_config(page_title="Talaga Hangsa KopiPlanPro", layout="centered")

# --- SISTEM PROSES GAMBAR BASE64 ---
def konversi_gambar_ke_html(jalur_gambar):
    try:
        with open(jalur_gambar, "rb") as file_gambar:
            data_binner = file_gambar.read()
            format_base64 = base64.b64encode(data_binner).decode()
        return f"""
        <div style="display: flex; justify-content: center; align-items: center; width: 100%; margin-top: 0px; margin-bottom: -5px;">
            <img src="data:image/png;base64,{format_base64}" style="width: 130px; height: auto; image-rendering: -webkit-optimize-contrast; image-rendering: crisp-edges; object-fit: contain;">
        </div>
        """
    except:
        return ""

# --- KODE DESAIN TEMA LUXURY (HEMAT SPACE) ---
st.markdown("""
    <style>
    header.stAppHeader { background-color: transparent !important; height: 0px !important; }
    section.stMain .block-container { padding-top: 1.5rem !important; max-width: 100% !important; }
    .stApp { background: linear-gradient(135deg, #f4f7f4 0%, #e6ebe6 100%); }
    .judul-utama { color: #1e3f20 !important; font-family: 'Helvetica Neue', sans-serif; font-weight: 800; text-align: center; text-shadow: 1px 1px 2px rgba(0,0,0,0.1); margin-top: 5px !important; margin-bottom: 2px !important; font-size: 24px; }
    .sub-judul { color: #4a6b4c; font-weight: 500; text-align: center; margin-top: 0px; margin-bottom: 12px; font-size: 13px; }
    .kotak-warning-petani { background-color: #fff3cd; color: #856404; padding: 6px 12px; border-radius: 8px; font-size: 11px; line-height: 1.4; margin-bottom: 20px; border: 1px solid #ffeeba; text-align: left; }
    .kartu-kebun { background-color: #ffffff; padding: 20px; border-radius: 15px; border-left: 6px solid #4e3629; box-shadow: 0 4px 12px rgba(0,0,0,0.04); margin-bottom: 20px; }
    div[data-testid="stRadio"] > div { background-color: #ffffff; padding: 10px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.03); }
    </style>
    """, unsafe_allow_html=True)

# --- EKSEKUSI PENAMPILAN LOGO ---
NAMA_LOGO = "logo.png"
if os.path.exists(NAMA_LOGO):
    html_logo = konversi_gambar_ke_html(NAMA_LOGO)
    if html_logo:
        st.markdown(html_logo, unsafe_allow_html=True)

st.markdown("<div class='judul-utama'>Talaga Hangsa KopiPlanPro</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-judul'>Asisten Digital Perawatan Kebun Kopi</div>", unsafe_allow_html=True)

st.markdown("""
    <div class="kotak-warning-petani">
        ⚠️ **INFORMASI KUNCI DATA:** Data kebun Anda telah dikunci di dalam kode GitHub pusat agar permanen abadi dan tidak bisa hilang saat di-refresh.
    </div>
""", unsafe_allow_html=True)


# --- 🌟 PUSAT PENGUNCIAN DATA KEBUN ASLI MILIK ANDA (ANTI-HILANG TOTAL) 🌟 ---
# SAYA SUDAH MASUKKAN CONTOH ISI NYA. SILAKAN GANTI TEKS & ANGKA DI BAWAH INI SESUAI DATA KEBUN ASLI ANDA!
Daftar_Kebun_Abadi = [
    {"Blok": "Blok Utama Lereng", "Lokasi": "Cianjur", "Ketinggian": 1100, "Varietas": "Arabika", "Jenis_Pupuk": "Organik (Kompos/Kohe)", "Tanggal_Tanam": "2025-01-01", "Jumlah_Pohon": 250, "Status_Musim": "Musim Kemarau"},
    {"Blok": "Blok B Bawah", "Lokasi": "Garut", "Ketinggian": 850, "Varietas": "Robusta", "Jenis_Pupuk": "Non-Organik (Kimia/NPK)", "Tanggal_Tanam": "2025-03-15", "Jumlah_Pohon": 400, "Status_Musim": "Musim Hujan"}
]

# Memaksa tabel selalu terisi data di atas tanpa menggunakan st.session_state yang labil
df_kebun = pd.DataFrame(Daftar_Kebun_Abadi)


# --- NAVIGASI MENU UTAMA (2 MENU PALING STABIL & KOKOH) ---
menu = st.radio("Pilih Menu:", ["📊 Data Kebun", "📅 Jadwal Kerja"], horizontal=True)
st.write("---")

# 1. MENU: TAMPILAN DATA KEBUN
if menu == "📊 Data Kebun":
    st.markdown("<h3 style='color: #1e3f20; margin-top:0;'>📊 Ringkasan Kebun</h3>", unsafe_allow_html=True)
    total_pohon = df_kebun['Jumlah_Pohon'].sum()
    st.metric(label="Total Semua Pohon Kopi Dikelola", value=f"{total_pohon} Batang")
    st.write("---")
    
    for idx, row in df_kebun.iterrows():
        st.markdown(f"""
            <div class="kartu-kebun">
                <h3 style="margin-top:0; color:#4e3629;">📍 Blok: {row['Blok']}</h3>
                <p style="margin:3px 0; font-size:14px;">🗺️ <b>Lokasi:</b> {row['Lokasi']} | 🏔️ <b>Ketinggian:</b> {row['Ketinggian']} mdpl</p>
                <p style="margin:3px 0; font-size:14px;">🌱 <b>Varietas:</b> Kopi {row['Varietas']} | 🌦️ <b>Cuaca:</b> {row['Status_Musim']}</p>
                <p style="margin:3px 0; font-size:14px;">🟫 <b>Sistem Pupuk:</b> {row['Jenis_Pupuk']}</p>
                <p style="margin:5px 0 0 0; color:#666; font-size:13px;"><b>Populasi:</b> {row['Jumlah_Pohon']} Pohon | **Tanggal Tanam:** {row['Tanggal_Tanam']}</p>
            </div>
        """, unsafe_allow_html=True)

# 2. MENU: JADWAL KERJA (URUTAN GLOBAL WAKTU TERDEKAT LINTAS BLOK)
elif menu == "📅 Jadwal Kerja":
    st.markdown("<h3 style='color: #1e3f20; margin-top:0;'>📅 Daftar Tugas Pemeliharaan</h3>", unsafe_allow_html=True)
    
    # Wadah untuk mencampur semua tugas dari semua blok
    keranjang_tugas_global = []
    
    for idx, row in df_kebun.iterrows():
        blok_id = row['Blok']
        lokasi = row['Lokasi']
        musim = row['Status_Musim']
        h_mdpl = int(row['Ketinggian'])
        var_kopi = row['Varietas']
        tgl = pd.to_datetime(row['Tanggal_Tanam'])
            
        tugas_lokal = []
        if "Organik" in str(row['Jenis_Pupuk']):
            tugas_lokal += [("🟫 Aplikasi Pupuk Dasar (Kompos)", 14), ("🟫 Pemupukan Organik Tahap 1", 120)]
        else:
            tugas_lokal += [("🧪 Aplikasi Pupuk Kimia Dasar", 30), ("🧪 Pemupukan NPK Vegetatif", 90)]
        
        if var_kopi == "Arabika":
            tugas_lokal += [("✂️ Pangkas Bentuk Batang Tunggal", 365), ("🍒 Estimasi Panen Perdana Arabika", 730)]
        else:
            tugas_lokal += [("✂️ Pangkas Wiwilan Tunas Air", 60), ("🍒 Estimasi Panen Perdana Robusta", 900)]
        
        if musim == "Musim Kemarau":
            tugas_lokal += [("💧 Penyiraman Rutin Kemarau T1", 3), ("💧 Penyiraman Rutin Kemarau T2", 6)]
        else:
            tugas_lokal += [("🌧️ Cek Saluran Drainase Kebun", 5), ("🌧️ Pembersihan Gulma Hujan", 15)]
            
        for nama_tugas, jeda_hari in tugas_lokal:
            tgl_target = tgl + timedelta(days=jeda_hari)
            keranjang_tugas_global.append({
                "blok": blok_id,
                "lokasi": lokasi,
                "mdpl": h_mdpl,
                "varietas": var_kopi,
                "tugas": nama_tugas,
                "target_waktu": tgl_target
            })
    
    # Proses utama mengurutkan seluruh isi keranjang berdasarkan tanggal terdekat
    keranjang_tugas_global.sort(key=lambda x: x["target_waktu"])
    
    for tgs in keranjang_tugas_global:
        tgl_cetak = tgs["target_waktu"].strftime('%d %b %Y')
        
        with st.container():
            st.markdown(f"📍 **Blok:** {tgs['blok']} ({tgs['lokasi']} - {tgs['mdpl']} mdpl)")
            
            if tgs["varietas"] == "Arabika" and tgs["mdpl"] < 1000:
                st.caption("⚠️ *Arabika di lahan rendah rentan penyakit karat daun. Perketat pengawasan jamur daun!*")
            elif tgs["varietas"] == "Robusta" and tgs["mdpl"] > 900:
                st.caption("⚠️ *Robusta di dataran tinggi membutuhkan waktu pembungaan sedikit lebih lama.*")
            else:
                st.caption("✅ *Kondisi ketinggian lahan sangat ideal untuk varietas ini.*")
            
            st.error(f"⚠️ **TUGAS** | **{tgs['tugas']}** | 📆 Target: {tgl_cetak}")
        st.markdown("---")
