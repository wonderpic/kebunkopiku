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
    return f"data:image/png;base64,{format_base64}"

# --- AMBIL DATA LOGO JIKA ADA ---
NAMA_LOGO = "logo.png"
html_src_logo = ""
if os.path.exists(NAMA_LOGO):
    try:
        html_src_logo = konversi_gambar_ke_html(NAMA_LOGO)
    except:
        pass

# --- KODE DESAIN TEMA (MEMAKSA PENYUSUTAN TOTAL MARGIN & TEKS) ---
st.markdown("""
    <style>
    /* 1. Paksa hapus margin putih paling atas dari server Streamlit */
    .stAppHeader {
        display: none !important;
    }
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0.5rem !important;
        max-width: 100% !important;
    }
    div[data-testid="stDecoration"] {
        display: none !important;
    }
    div[data-testid="stVerticalBlock"] > div {
        padding-top: 0px !important;
        padding-bottom: 0px !important;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f4f7f4 0%, #e6ebe6 100%);
    }
    
    /* 2. Desain Kotak Kartu Informasi */
    .block-container .element-container div.stAlert {
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: none;
    }
    
    /* Kartu Peringatan Tugas Belum Selesai */
    div[data-testid="stNotification"] {
        border-left: 5px solid #d9534f !important;
        background-color: #ffffff !important;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(217, 83, 79, 0.08);
    }
    
    /* Percantik Tombol Menu Navigasi */
    div[data-testid="stRadio"] > div {
        background-color: #ffffff;
        padding: 8px;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.03);
    }
    
    /* Kotak Kontainer Custom untuk Data Kebun */
    .kartu-kebun {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 15px;
        border-left: 6px solid #4e3629;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 🛠️ BLOK HEADER KUSTOM MANDIRI (MENGUNCI MARGIN & TEKS PERINGATAN TIPIS) ---
# Di sini kita menyatukan Logo, Judul, dan Teks Peringatan Kecil dalam satu baris HTML terpadu agar hemat tempat
html_logo_tag = f'<img src="{html_src_logo}" style="width: 90px; height: auto; margin-bottom: 5px; image-rendering: -webkit-optimize-contrast; image-rendering: crisp-edges;">' if html_src_logo else ''

st.markdown(f"""
    <div style="text-align: center; width: 100%; margin-top: 0px; padding-top: 0px;">
        {html_logo_tag}
        <h1 style="color: #1e3f20 !important; font-family: 'Helvetica Neue', sans-serif; font-weight: 800; text-align: center; margin: 2px 0 !important; font-size: 22px; padding: 0;">Talaga Hangsa KopiPlanPro</h1>
        <p style="color: #4a6b4c; font-weight: 500; text-align: center; margin: 0 0 10px 0 !important; font-size: 12px; padding: 0;">Asisten Digital Manajemen Perawatan Kebun Kopi</p>
        
        <!-- HASIL KOREKSI: Kotak Peringatan Sangat Tipis, Hemat Tempat, Huruf Kecil -->
        <div style="background-color: #fff3cd; color: #856404; padding: 6px 10px; border-radius: 6px; font-size: 10.5px; line-height: 1.3; text-align: left; margin-bottom: 12px; border: 1px solid #ffeeba;">
            <b>⚠️ PENTING PETANI:</b> Data tersimpan di HP ini. <b>JANGAN</b> hapus riwayat internet (Cache/Cookies) HP agar data tidak hilang. Unduh cadangan berkala di menu Data Kebun.
        </div>
    </div>
""", unsafe_allow_html=True)


# --- SISTEM PENYIMPANAN DATA MANDIRI ---
if 'kebun_data' not in st.session_state:
    st.session_state.kebun_data = pd.DataFrame(columns=['Blok', 'Varietas', 'Jenis_Pupuk', 'Tanggal_Tanam', 'Jumlah_Pohon', 'Status_Musim'])

# --- NAVIGASI MENU UTAMA ---
menu = st.radio("Pilih Menu:", ["📊 Data Kebun", "📅 Jadwal Kerja", "🧮 Kalkulator Pupuk", "🌱 Tambah Blok"], horizontal=True)
st.write("---")

# 1. MENU: TAMBAH BLOK
if menu == "🌱 Tambah Blok":
    st.markdown("<h3 style='color: #1e3f20; margin-top:0;'>🌱 Tambah Blok Kebun Baru</h3>", unsafe_allow_html=True)
    with st.form("form_kebun_baru"):
        nama_blok = st.text_input("Nama Blok Baru", placeholder="Contoh: Blok A")
        varietas = st.selectbox("Varietas Kopi", ["Arabika", "Robusta"])
        jenis_pupuk = st.selectbox("Metode Pemupukan Utama", ["Organik (Kompos/Kohe)", "Non-Organik (Kimia/NPK)"])
        status_musim = st.selectbox("Kondisi Cuaca Saat Ini", ["Musim Kemarau", "Musim Hujan"])
        tgl_tanam = st.date_input("Tanggal Tanam", datetime.now().date())
        jml_pohon = st.number_input("Jumlah Pohon (Batang)", min_value=1, value=100)
        submit_button = st.form_submit_button(label="⚡ Simpan Blok Baru")

    if submit_button and nama_blok:
        if not st.session_state.kebun_data.empty and nama_blok in st.session_state.kebun_data['Blok'].values:
            st.error(f"Nama Blok '{nama_blok}' sudah terdaftar!")
        else:
            new_row = pd.DataFrame([[nama_blok, varietas, jenis_pupuk, tgl_tanam, jml_pohon, status_musim]], 
                                    columns=['Blok', 'Varietas', 'Jenis_Pupuk', 'Tanggal_Tanam', 'Jumlah_Pohon', 'Status_Musim'])
            st.session_state.kebun_data = pd.concat([st.session_state.kebun_data, new_row], ignore_index=True)
            st.success(f"🎉 Sukses menambahkan {nama_blok}.")
            st.rerun()

# 2. MENU: TAMPILAN DATA KEBUN
elif menu == "📊 Data Kebun":
    st.markdown("<h3 style='color: #1e3f20; margin-top:0;'>📊 Ringkasan Kebun</h3>", unsafe_allow_html=True)
    
    if st.session_state.kebun_data.empty:
        st.info("📲 Belum ada data kebun. Silakan tambah data di menu '🌱 Tambah Blok'.")
    else:
        total_pohon = st.session_state.kebun_data['Jumlah_Pohon'].sum()
        st.metric(label="Total Semua Pohon Kopi Dikelola", value=f"{total_pohon} Batang")
        
        data_csv = st.session_state.kebun_data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Unduh Cadangan Data Kebun (Excel/CSV)",
            data=data_csv,
            file_name=f"Cadangan_Kebun_{datetime.now().strftime('%d_%b_%Y')}.csv",
            mime='text/csv'
        )
        st.write("---")
        
        for idx, row in st.session_state.kebun_data.iterrows():
            st.markdown(f"""
                <div class="kartu-kebun">
                    <h4 style="margin-top:0; margin-bottom:5px; color:#4e3629;">📍 Blok: {row['Blok']}</h4>
                    <p style="margin:2px 0; font-size:13px;"><b>Varietas:</b> Kopi {row['Varietas']} | <b>Cuaca:</b> {row['Status_Musim']}</p>
                    <p style="margin:2px 0; font-size:13px;"><b>Sistem Pupuk:</b> {row['Jenis_Pupuk']}</p>
                    <p style="margin:2px 0; font-size:12px; color:#666;"><b>Populasi:</b> {row['Jumlah_Pohon']} Pohon | <b>Tanam:</b> {row['Tanggal_Tanam']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"🗑️ Hapus {row['Blok']}", key=f"hapus_{row['Blok']}_{idx}"):
                st.session_state.kebun_data = st.session_state.kebun_data.drop(idx).reset_index(drop=True)
                st.rerun()

# 3. MENU: TAMPILAN JADWAL
elif menu == "📅 Jadwal Kerja":
    st.markdown("<h3 style='color: #1e3f20; margin-top:0;'>📅 Daftar Tugas Pemeliharaan</h3>", unsafe_allow_html=True)
    
    if st.session_state.kebun_data.empty:
        st.info("Belum ada jadwal. Tambahkan data kebun terlebih dahulu.")
    else:
        for idx, row in st.session_state.kebun_data.iterrows():
            blok_id = row['Blok']
            tgl = pd.to_datetime(row['Tanggal_Tanam'])
            musim = row['Status_Musim']
            
            st.markdown(f"##### 📍 Blok Kerja: **{blok_id}** ({row['Varietas']})")
            
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
                st.error(f"⚠️ **TUGAS** | **{nama_tugas}** | 📆 Target: {tgl_indo}")
            st.markdown("---")

# 4. MENU: TAMPILAN KALKULATOR
elif menu == "🧮 Kalkulator Pupuk":
    st.markdown("<h3 style='color: #1e3f20; margin-top:0;'>🧮 Kalkulator Kebutuhan Pupuk</h3>", unsafe_allow_html=True)
    
    if st.session_state.kebun_data.empty:
        st.info("Masukkan data kebun terlebih dahulu untuk mengaktifkan kalkulator.")
    else:
        pilihan_blok = st.selectbox("Pilih Blok Kebun:", st.session_state.kebun_data['Blok'].unique())
