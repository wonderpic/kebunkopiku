import streamlit as st
import pandas as pd
import os
import base64
from datetime import datetime, timedelta

# Konfigurasi Tampilan Utama Halaman HP
st.set_page_config(page_title="Talaga Hangsa KopiPlanPro", layout="centered")

# --- SISTEM PROSES GAMBAR BASE64 (MENGUNCI KETAJAMAN & CENTER MUTLAK) ---
def konversi_gambar_ke_html(jalur_gambar):
    with open(jalur_gambar, "rb") as file_gambar:
        data_binner = file_gambar.read()
        format_base64 = base64.b64encode(data_binner).decode()
    return f"""
    <div style="display: flex; justify-content: center; align-items: center; width: 100%; margin-top: 0px; margin-bottom: -5px;">
        <img src="data:image/png;base64,{format_base64}" style="width: 130px; height: auto; image-rendering: -webkit-optimize-contrast; image-rendering: crisp-edges; object-fit: contain;">
    </div>
    """

# --- KODE DESAIN TEMA LUXURY (HEMAT SPACE) ---
st.markdown("""
    <style>
    header.stAppHeader { background-color: transparent !important; height: 0px !important; }
    section.stMain .block-container { padding-top: 1.5rem !important; max-width: 100% !important; }
    .stApp { background: linear-gradient(135deg, #f4f7f4 0%, #e6ebe6 100%); }
    
    .judul-utama {
        color: #1e3f20 !important;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 800;
        text-align: center;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        margin-top: 15px !important;
        margin-bottom: 5px !important;
        font-size: 24px;
    }
    
    .sub-judul {
        color: #4a6b4c; 
        font-weight: 500; 
        text-align: center; 
        margin-top: -5px;
        margin-bottom: 20px;
        font-size: 13px;
    }
    
    .kotak-warning-petani {
        background-color: #fff3cd;
        color: #856404;
        padding: 8px 12px;
        border-radius: 8px;
        font-size: 11px;
        line-height: 1.4;
        margin-bottom: 20px;
        border: 1px solid #ffeeba;
        text-align: left;
    }
    
    .kartu-kebun {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        border-left: 6px solid #4e3629;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
        margin-bottom: 20px;
    }
    
    div[data-testid="stRadio"] > div {
        background-color: #ffffff;
        padding: 10px;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.03);
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
        st.markdown("<p style='text-align: center; color: #888; font-style: italic; font-size: 12px;'>[ Memuat Logo... ]</p>", unsafe_allow_html=True)
else:
    st.markdown(f"<p style='text-align: center; color: #888; font-style: italic; font-size: 12px;'>[ File '{NAMA_LOGO}' tidak ditemukan ]</p>", unsafe_allow_html=True)

st.markdown("<div class='judul-utama'>Talaga Hangsa KopiPlanPro</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-judul'>Asisten Digital Perawatan Kebun Kopi</div>", unsafe_allow_html=True)

st.markdown("""
    <div class="kotak-warning-petani">
        ⚠️ **PENTING UNTUK PETANI:** Data kebun tersimpan aman di memori internet HP Anda. <b>JANGAN</b> hapus riwayat internet (Cache/Cookies) HP Anda agar data tidak hilang secara otomatis.
    </div>
""", unsafe_allow_html=True)

# --- SISTEM PENYIMPANAN DATA MANDIRI ---
if 'kebun_data' not in st.session_state:
    st.session_state.kebun_data = pd.DataFrame(columns=['Blok', 'Varietas', 'Jenis_Pupuk', 'Tanggal_Tanam', 'Jumlah_Pohon', 'Status_Musim'])

# --- NAVIGASI MENU UTAMA ---
menu = st.radio("Pilih Menu:", ["📊 Data Kebun", "📅 Jadwal Kerja", "🌱 Tambah Blok"], horizontal=True)
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
            st.success(f"🎉 Sukses! {nama_blok} berhasil ditambahkan ke sistem.")
            st.rerun()

# 2. MENU: TAMPILAN DATA KEBUN
elif menu == "📊 Data Kebun":
    st.markdown("<h3 style='color: #1e3f20;'>📊 Ringkasan Kebun</h3>", unsafe_allow_html=True)
    
    if st.session_state.kebun_data.empty:
        st.info("📲 Belum ada data kebun Anda yang tersimpan di memori internet HP. Silakan masuk ke menu '🌱 Tambah Blok' untuk mulai mencatatkan kebun Anda.")
    else:
        total_pohon = st.session_state.kebun_data['Jumlah_Pohon'].sum()
        st.metric(label="Total Semua Pohon Kopi Dikelola", value=f"{total_pohon} Batang")
        st.write("")
        
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

# 3. MENU: JADWAL KERJA (🌟 DIURUTKAN BERDASARKAN WAKTU TERDEKAT SECARA GLOBAL LINTAS BLOK 🌟)
elif menu == "📅 Jadwal Kerja":
    st.markdown("<h3 style='color: #1e3f20;'>📅 Daftar Tugas Pemeliharaan</h3>", unsafe_allow_html=True)
    
    if st.session_state.kebun_data.empty:
        st.info("📲 Belum ada jadwal tugas. Tambahkan data kebun terlebih dahulu di menu '🌱 Tambah Blok'.")
    else:
        # Menampung seluruh tugas global ke dalam wadah list DataFrame kustom
        daftar_tugas_gabungan = []
        
        for idx, row in st.session_state.kebun_data.iterrows():
            blok_id = row['Blok']
            musim = row['Status_Musim']
            var_kopi = row['Varietas']
            # Fungsi konversi tanggal murni Pandas untuk menjamin kecocokan tipe data kalender
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
                daftar_tugas_gabungan.append({
                    "Blok": blok_id,
                    "Varietas": var_kopi,
                    "Tugas": nama_tugas,
                    "Tanggal_Target": tgl_target
                })
        
        # 2. PROSES UTAMA: Mengubah list menjadi DataFrame dan mengurutkannya menggunakan fungsi resmi Pandas
        df_tugas_global = pd.DataFrame(daftar_tugas_gabungan)
        df_tugas_global = df_tugas_global.sort_values(by="Tanggal_Target", ascending=True)
        
        # 3. Tampilkan hasil urutan waktu mendesak ke HP petani
        for _, tgs in df_tugas_global.iterrows():
            tgl_indo = tgs["Tanggal_Target"].strftime('%d %b %Y')
            st.error(f"📍 **Blok:** {tgs['Blok']} ({tgs['Varietas']})\n\n⚠️ **TUGAS:** {tgs['Tugas']}\n\n📆 **Target:** {tgl_indo}")
            st.markdown("<div style='margin-bottom:10px;'></div>", unsafe_allow_html=True)
