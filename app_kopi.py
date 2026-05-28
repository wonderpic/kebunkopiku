import streamlit as st
import pandas as pd
import os
import base64
from datetime import datetime, timedelta

# Konfigurasi Tampilan Utama Halaman HP
st.set_page_config(page_title="Talaga Hangsa KopiPlanPro", layout="centered")

# --- SISTEM PROSES GAMBAR BASE64 ---
def konversi_gambar_ke_html(jalur_gambar):
    with open(jalur_gambar, "rb") as file_gambar:
        data_binner = file_gambar.read()
        format_base64 = base64.b64encode(data_binner).decode()
    return f"""
    <div style="display: flex; justify-content: center; align-items: center; width: 100%; margin-bottom: -10px;">
        <img src="data:image/png;base64,{format_base64}" style="width: 140px; height: auto; image-rendering: -webkit-optimize-contrast; image-rendering: crisp-edges; object-fit: contain;">
    </div>
    """

# --- KODE DESAIN TEMA LUXURY ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f4f7f4 0%, #e6ebe6 100%);
    }
    .judul-utama {
        color: #1e3f20 !important;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 800;
        text-align: center;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        margin-top: 15px !important;
        margin-bottom: 5px !important;
        font-size: 28px;
    }
    .sub-judul {
        color: #4a6b4c; 
        font-weight: 500; 
        text-align: center; 
        margin-top: -5px;
        margin-bottom: 25px;
        font-size: 14px;
    }
    .block-container .element-container div.stAlert {
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: none;
    }
    div[data-testid="stNotification"] {
        border-left: 5px solid #d9534f !important;
        background-color: #ffffff !important;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(217, 83, 79, 0.08);
    }
    div[data-testid="stRadio"] > div {
        background-color: #ffffff;
        padding: 10px;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.03);
    }
    .kartu-kebun {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        border-left: 6px solid #4e3629;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- EKSEKUSI PENAMPILAN LOGO ---
NAMA_LOGO = "logo.png"
if os.path.exists(NAMA_LOGO):
    try:
        html_logo = konversi_gambar_ke_html(NAMA_LOGO)
        st.markdown(html_logo, unsafe_allow_html=True)
    except:
        st.markdown("<p style='text-align: center; color: #d9534f; font-style: italic; font-size: 12px;'>[ Gagal memproses ketajaman logo ]</p>", unsafe_allow_html=True)
else:
    st.markdown(f"<p style='text-align: center; color: #888; font-style: italic; font-size: 12px;'>[ File '{NAMA_LOGO}' tidak ditemukan ]</p>", unsafe_allow_html=True)

# --- JUDUL BRANDING ---
st.markdown("<div class='judul-utama'>Talaga Hangsa KopiPlanPro</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-judul'>Asisten Digital Manajemen Perawatan Kebun Kopi</div>", unsafe_allow_html=True)

# --- ⚠️ FITUR BARU: TEKS PERINGATAN PENGAMAN UNTUK PETANI ---
st.warning("""
    ⚠️ **PENTING UNTUK KAWAN PETANI:** 
    * Data kebun Anda tersimpan aman di HP ini. 
    * **JANGAN** bersihkan riwayat internet (*Clear Cache/Cookies*) HP Anda agar data kebun tidak terhapus.
    * Gunakan tombol **📥 Unduh Cadangan Excel** di menu **Data Kebun** untuk menyimpan data ke HP Anda secara berkala!
""")
st.write("")

# --- SISTEM PENYIMPANAN DATA MANDIRI ---
if 'kebun_data' not in st.session_state:
    st.session_state.kebun_data = pd.DataFrame(columns=['Blok', 'Varietas', 'Jenis_Pupuk', 'Tanggal_Tanam', 'Jumlah_Pohon', 'Status_Musim'])

# --- NAVIGASI MENU UTAMA ---
menu = st.radio("Pilih Menu:", ["📊 Data Kebun", "📅 Jadwal Kerja", "🧮 Kalkulator Pupuk", "🌱 Tambah Blok"], horizontal=True)
st.write("---")

# 1. MENU: TAMBAH BLOK
if menu == "🌱 Tambah Blok":
    st.markdown("<h3 style='color: #1e3f20;'>🌱 Tambah Blok Kebun Baru</h3>", unsafe_allow_html=True)
    with st.form("form_kebun_baru"):
        nama_blok = st.text_input("Nama Blok Baru", placeholder="Contoh: Blok A / Lereng Barat")
        varietas = st.selectbox("Varietas Kopi", ["Arabika", "Robusta"])
        jenis_pupuk = st.selectbox("Metode Pemupukan Utama", ["Organik (Kompos/Kohe)", "Non-Organik (Kimia/NPK)"])
        status_musim = st.selectbox("Kondisi Cuaca Saat Ini", ["Musim Kemarau", "Musim Hujan"])
        tgl_tanam = st.date_input("Tanggal Tanam", datetime.now().date())
        jml_pohon = st.number_input("Jumlah Pohon (Batang)", min_value=1, value=100)
        submit_button = st.form_submit_button(label="⚡ Simpan Blok Baru")

    if submit_button and nama_blok:
        if not st.session_state.kebun_data.empty and nama_blok in st.session_state.kebun_data['Blok'].values:
            st.error(f"Nama Blok '{nama_blok}' sudah terdaftar! Gunakan nama lain.")
        else:
            new_row = pd.DataFrame([[nama_blok, varietas, jenis_pupuk, tgl_tanam, jml_pohon, status_musim]], 
                                    columns=['Blok', 'Varietas', 'Jenis_Pupuk', 'Tanggal_Tanam', 'Jumlah_Pohon', 'Status_Musim'])
            st.session_state.kebun_data = pd.concat([st.session_state.kebun_data, new_row], ignore_index=True)
            st.success(f"🎉 Sukses! {nama_blok} berhasil ditambahkan.")
            st.rerun()

# 2. MENU: TAMPILAN DATA KEBUN (DENGAN TOMBOL UNDUH EXCEL)
elif menu == "📊 Data Kebun":
    st.markdown("<h3 style='color: #1e3f20;'>📊 Ringkasan Kebun</h3>", unsafe_allow_html=True)
    
    if st.session_state.kebun_data.empty:
        st.info("📲 Belum ada data kebun. Silakan masuk ke menu '🌱 Tambah Blok' terlebih doaulu.")
    else:
        total_pohon = st.session_state.kebun_data['Jumlah_Pohon'].sum()
        st.metric(label="Total Semua Pohon Kopi Dikelola", value=f"{total_pohon} Batang")
        
        # --- 📥 FITUR BARU: TOMBOL UNDUH CADANGAN EXCEL/CSV ---
        # Mengubah tabel data menjadi format teks CSV yang dipahami Excel HP
        data_csv = st.session_state.kebun_data.to_csv(index=False).encode('utf-8')
        
        st.write("")
        st.download_button(
            label="📥 Unduh Cadangan Data Kebun (Excel/CSV)",
            data=data_csv,
            file_name=f"Cadangan_Kebun_Kopi_{datetime.now().strftime('%d_%b_%Y')}.csv",
            mime='text/csv',
            help="Klik di sini untuk mengamankan data kebun ke dalam folder Download HP Anda."
        )
        st.write("---")
        
        for idx, row in st.session_state.kebun_data.iterrows():
            st.markdown(f"""
                <div class="kartu-kebun">
                    <h3 style="margin-top:0; color:#4e3629;">📍 Blok: {row['Blok']}</h3>
                    <p style="margin:5px 0;"><b>Varietas:</b> Kopi {row['Varietas']} | <b>Cuaca:</b> {row['Status_Musim']}</p>
                    <p style="margin:5px 0;"><b>Sistem Pupuk:</b> {row['Jenis_Pupuk']}</p>
                    <p style="margin:5px 0; color:#666;"><b>Populasi:</b> {row['Jumlah_Pohon']} Pohon | <b>Tanggal Tanam:</b> {row['Tanggal_Tanam']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"🗑️ Hapus {row['Blok']}", key=f"hapus_{row['Blok']}_{idx}"):
                st.session_state.kebun_data = st.session_state.kebun_data.drop(idx).reset_index(drop=True)
                st.success(f"Blok {row['Blok']} telah berhasil dihapus!")
                st.rerun()

# 3. MENU: TAMPILAN JADWAL & PERINGATAN PINTAR
elif menu == "📅 Jadwal Kerja":
    st.markdown("<h3 style='color: #1e3f20;'>📅 Daftar Tugas Pemeliharaan</h3>", unsafe_allow_html=True)
    
    if st.session_state.kebun_data.empty:
        st.info("Belum ada jadwal. Tambahkan data kebun terlebih dahulu di menu '🌱 Tambah Blok'.")
    else:
        for idx, row in st.session_state.kebun_data.iterrows():
            blok_id = row['Blok']
            tgl = pd.to_datetime(row['Tanggal_Tanam'])
            musim = row['Status_Musim']
            
            st.markdown(f"#### 📍 Blok Kerja: **{blok_id}** ({row['Varietas']})")
            
            tugas_list = []
            if "Organik" in row['Jenis_Pupuk']:
                tugas_list += [("🟫 Aplikasi Pupuk Dasar (Kompos)", 14), ("🟫 Pemupukan Organik Tahap 1", 120)]
            else:
                tugas_list += [("🧪 Aplikasi Pupuk Kimia Dasar", 30), ("🧪 Pemupukan NPK Vegetatif", 90)]
            
            if row['Varietas'] == "Arabika":
                tugas_list += [("✂️ Pangkas Bentuk Batang Tunggal", 365), ("🍒 Estimasi Panen Perdana Arabika", 730)]
            else:
                tugas_list += [("✂️ Pangkas Wiwilan Tunas Air", 60), ("🍒 Estimasi Panen Perdana Robusta", 900)]
            
            if musim == "Musim Kemarau":
                tugas_list += [("💧 Penyiraman Rutin Kemarau T1", 3), ("💧 Penyiraman Rutin Kemarau T2", 6)]
            else:
                tugas_list += [("🌧️ Cek Saluran Drainase Kebun", 5), ("🌧️ Pembersihan Gulma Hujan", 15)]
                
            tugas_list.sort(key=lambda x: x)
            
            for nama_tugas, jeda_hari in tugas_list:
                tgl_target = tgl + timedelta(days=jeda_hari)
                tgl_indo = tgl_target.strftime('%d %b %Y')
                st.error(f"⚠️ **TUGAS HARUS DILAKUKAN**\n\n**{nama_tugas}**\n\n📆 Target: {tgl_indo}")
            st.markdown("---")

# 4. MENU: TAMPILAN KALKULATOR PUPUK OTOMATIS
elif menu == "🧮 Kalkulator Pupuk":
    st.markdown("<h3 style='color: #1e3f20;'>🧮 Kalkulator Kebutuhan Pupuk Kebun</h3>", unsafe_allow_html=True)
    
    if st.session_state.kebun_data.empty:
        st.info("Masukkan data kebun terlebih dahulu untuk mengaktifkan kalkulator.")
    else:
        pilihan_blok = st.selectbox("Pilih Blok Kebun:", st.session_state.kebun_data['Blok'].unique())
