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
        return f"data:image/png;base64,{format_base64}"
    except:
        return ""

NAMA_LOGO = "logo.png"
html_src_logo = konversi_gambar_ke_html(NAMA_LOGO)

# --- KODE DESAIN TEMA LUXURY (HEMAT SPACE) ---
st.markdown("""
    <style>
    header.stAppHeader { background-color: transparent !important; height: 0px !important; }
    section.stMain .block-container { padding-top: 1rem !important; max-width: 100% !important; }
    .stApp { background: linear-gradient(135deg, #f4f7f4 0%, #e6ebe6 100%); }
    .judul-utama { color: #1e3f20 !important; font-family: 'Helvetica Neue', sans-serif; font-weight: 800; text-align: center; margin-top: 5px !important; margin-bottom: 2px !important; font-size: 24px; }
    .sub-judul { color: #4a6b4c; font-weight: 500; text-align: center; margin-top: 0px; margin-bottom: 12px; font-size: 13px; }
    .kotak-warning-petani { background-color: #fff3cd; color: #856404; padding: 6px 12px; border-radius: 8px; font-size: 11px; line-height: 1.4; margin-bottom: 15px; border: 1px solid #ffeeba; text-align: left; }
    .kartu-kebun { background-color: #ffffff; padding: 15px; border-radius: 15px; border-left: 6px solid #4e3629; box-shadow: 0 4px 12px rgba(0,0,0,0.04); margin-bottom: 15px; }
    div[data-testid="stRadio"] > div { background-color: #ffffff; padding: 8px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.03); }
    </style>
    """, unsafe_allow_html=True)

# --- BLOK HEADER ---
if html_src_logo:
    st.markdown(f"""<div style="text-align: center; width: 100%; margin-bottom: 5px;"><img src="{html_src_logo}" style="width: 95px; height: auto;"></div>""", unsafe_allow_html=True)

st.markdown("<div class='judul-utama'>Talaga Hangsa KopiPlanPro</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-judul'>Asisten Digital Perawatan Kebun Kopi</div>", unsafe_allow_html=True)

st.markdown("""
    <div class="kotak-warning-petani">
        ⚠️ **INFORMASI KUNCI DATA:** Data kebun Anda dikunci langsung dari kode pusat GitHub agar permanen abadi dan tidak bisa hilang saat di-refresh.
    </div>
""", unsafe_allow_html=True)

# --- 🌟 PUSAT DATA KEBUN PERMANEN (ANTI-HILANG RESTART) 🌟 ---
# Silakan ketik dan sesuaikan data kebun asli Anda di bawah ini agar tersimpan abadi
Daftar_Kebun_Abadi = [
    {"Blok": "Blok Utama (Lereng)", "Varietas": "Arabika", "Jenis_Pupuk": "Organik (Kompos/Kohe)", "Tanggal_Tanam": "2025-01-01", "Jumlah_Pohon": 250, "Status_Musim": "Musim Kemarau"},
    {"Blok": "Blok B (Bawah)", "Varietas": "Robusta", "Jenis_Pupuk": "Non-Organik (Kimia/NPK)", "Tanggal_Tanam": "2025-06-15", "Jumlah_Pohon": 400, "Status_Musim": "Musim Hujan"}
]

# Mengunci tabel agar selalu membaca data di atas secara konstan
df_kebun = pd.DataFrame(Daftar_Kebun_Abadi)

# --- NAVIGASI MENU UTAMA ---
menu = st.radio("Pilih Menu:", ["📊 Data Kebun", "📅 Jadwal Kerja", "🧮 Kalkulator Pupuk"], horizontal=True)
st.write("---")

# 1. MENU: DATA KEBUN
if menu == "📊 Data Kebun":
    st.markdown("<h3 style='color: #1e3f20; margin-top:0;'>📊 Ringkasan Kebun</h3>", unsafe_allow_html=True)
    total_pohon = df_kebun['Jumlah_Pohon'].sum()
    st.metric(label="Total Semua Pohon Kopi Dikelola", value=f"{total_pohon} Batang")
    st.write("---")
    
    for idx, row in df_kebun.iterrows():
        st.markdown(f"""
            <div class="kartu-kebun">
                <h4 style="margin-top:0; margin-bottom:5px; color:#4e3629;">📍 Blok: {row['Blok']}</h4>
                <p style="margin:2px 0; font-size:13px;"><b>Varietas:</b> Kopi {row['Varietas']} | <b>Cuaca:</b> {row['Status_Musim']}</p>
                <p style="margin:2px 0; font-size:13px;"><b>Sistem Pupuk:</b> {row['Jenis_Pupuk']}</p>
                <p style="margin:2px 0; font-size:12px; color:#666;"><b>Populasi:</b> {row['Jumlah_Pohon']} Pohon | **Tanam:** {row['Tanggal_Tanam']}</p>
            </div>
        """, unsafe_allow_html=True)

# 2. MENU: JADWAL KERJA
elif menu == "📅 Jadwal Kerja":
    st.markdown("<h3 style='color: #1e3f20; margin-top:0;'>📅 Daftar Tugas Pemeliharaan</h3>", unsafe_allow_html=True)
    for idx, row in df_kebun.iterrows():
        st.markdown(f"##### 📍 Blok Kerja: **{row['Blok']}** ({row['Varietas']})")
        tgl = pd.to_datetime(row['Tanggal_Tanam'])
        tugas_list = []
        if "Organik" in row['Jenis_Pupuk']:
            tugas_list += [("🟫 Aplikasi Pupuk Dasar (Kompos)", 14), ("🟫 Pemupukan Organik Tahap 1", 120)]
        else:
            tugas_list += [("🧪 Aplikasi Pupuk Kimia Dasar", 30), ("🧪 Pemupukan NPK Vegetatif", 90)]
        if row['Varietas'] == "Arabika":
            tugas_list += [("✂️ Pangkas Bentuk Batang Tunggal", 365), ("🍒 Estimasi Panen Perdana Arabika", 730)]
        else:
            tugas_list += [("✂️ Pangkas Wiwilan Tunas Air", 60), ("🍒 Estimasi Panen Perdana Robusta", 900)]
        if row['Status_Musim'] == "Musim Kemarau":
            tugas_list += [("💧 Penyiraman Rutin Kemarau T1", 3), ("💧 Penyiraman Rutin Kemarau T2", 6)]
        else:
            tugas_list += [("🌧️ Cek Saluran Drainase Kebun", 5), ("🌧️ Pembersihan Gulma Hujan", 15)]
            
        tugas_list.sort(key=lambda x: x)
        for nama_tugas, jeda_hari in tugas_list:
            tgl_target = tgl + timedelta(days=jeda_hari)
            st.error(f"⚠️ **TUGAS** | **{nama_tugas}** | 📆 Target: {tgl_target.strftime('%d %b %Y')}")
        st.markdown("---")

# 3. MENU: KALKULATOR PUPUK & DROPDOWN WILAYAH (GARANSI MUNCUL 100%)
elif menu == "🧮 Kalkulator Pupuk":
    st.markdown("<h3 style='color: #1e3f20; margin-top:0;'>🧮 Kalkulator Kebutuhan Pupuk</h3>", unsafe_allow_html=True)
    pilihan_blok = st.selectbox("Pilih Blok Kebun:", df_kebun['Blok'].unique())
    df_filter = df_kebun[df_kebun['Blok'] == pilihan_blok]
    
    if not df_filter.empty:
        # Perbaikan total ekstraksi data menggunakan indeks skalar array
        jumlah_pohon = int(df_filter['Jumlah_Pohon'].values[0])
        sistem_pupuk = str(df_filter['Jenis_Pupuk'].values[0])
        st.info(f"**Blok Terpilih:** {pilihan_blok} | **Populasi:** {jumlah_pohon} Pohon")
        
        if "Organik" in sistem_pupuk:
            tonase = jumlah_pohon * 5.0
            st.metric(label="Total Pupuk Kompos/Kohe Dibutuhkan", value=f"{tonase:,.1f} Kg")
            jenis_barang = "Pupuk Organik Kompos"
        else:
            tonase = (jumlah_pohon * 100) / 1000
            st.metric(label="Total Pupuk NPK Kimia Dibutuhkan", value=f"{tonase:,.1f} Kg")
            jenis_barang = "Pupuk Kimia NPK"
        
        # --- 🛒 MENU PENAWARAN AFILIASI WA (PASTI MUNCUL) ---
        st.write("---")
        st.markdown("<h4 style='color: #1e3f20; margin-top:0;'>🛒 Pesan Pupuk Lewat Agen Terdekat</h4>", unsafe_allow_html=True)
        wilayah = st.selectbox("Pilih Lokasi Wilayah Kebun Anda:", ["Pilih Wilayah...", "Aceh Tengah (Gayo)", "Bandung Barat (Lembang)", "Temanggung (Jawa Tengah)", "Kintamani (Bali)"])
        
        kontak_toko = {
            "Aceh Tengah (Gayo)": {"nama": "Toko Tani Makmur Gayo", "wa": "628123456789"},
            "Bandung Barat (Lembang)": {"nama": "CV Kopi Subur Mandiri", "wa": "628555444333"},
            "Temanggung (Jawa Tengah)": {"nama": "Agen Pupuk Subur Temanggung", "wa": "628987654321"},
            "Kintamani (Bali)": {"nama": "Kios Tani Amadan Bali", "wa": "628111222333"}
        }
        
        if wilayah != "Pilih Wilayah...":
            toko = kontak_toko[wilayah]
            st.success(f"📍 Mitra Terdekat Ditemukan: **{toko['nama']}**")
            pesan_wa = f"Halo {toko['nama']}, saya ingin memesan {jenis_barang} sebanyak {tonase:,.1f} Kg untuk kebutuhan blok kebun kopi saya melalui sistem rekomendasi aplikasi Talaga Hangsa KopiPlanPro."
            link_wa = f"https://wa.me{toko['wa']}?text={pesan_wa.replace(' ', '%20')}"
            st.markdown(f"""<a href="{link_wa}" target="_blank" style="text-decoration: none;"><div style="background-color: #25d366; color: white; padding: 12px; text-align: center; border-radius: 8px; font-weight: bold; margin-top: 10px;">🟢 Hubungi Toko & Kirim Pesanan Otomatis</div></a>""", unsafe_allow_html=True)
