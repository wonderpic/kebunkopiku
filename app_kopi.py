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

NAMA_LOGO = "logo.png"
html_src_logo = ""
if os.path.exists(NAMA_LOGO):
    try:
        html_src_logo = konversi_gambar_ke_html(NAMA_LOGO)
    except:
        pass

# --- KODE DESAIN TEMA LUXURY (KOREKSI MARGIN PAS) ---
st.markdown("""
    <style>
    /* Menghapus padding bawaan atas secara pas agar logo TIDAK terpotong */
    .stAppHeader {
        display: none !important;
    }
    section.stMain .block-container {
        padding-top: 1rem !important; /* Memberi ruang aman 1rem di atas logo */
        max-width: 100% !important;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f4f7f4 0%, #e6ebe6 100%);
    }
    
    /* Mengubah Teks Judul */
    .judul-utama {
        color: #1e3f20 !important;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 800;
        text-align: center;
        margin-top: 0px !important;
        margin-bottom: 2px !important;
        font-size: 24px;
    }
    
    .sub-judul {
        color: #4a6b4c; 
        font-weight: 500; 
        text-align: center; 
        margin-top: 0px;
        margin-bottom: 12px;
        font-size: 13px;
    }
    
    /* KOTAK PERINGATAN KUNING TIPIS & HEMAT TEMPAT */
    .kotak-warning-petani {
        background-color: #fff3cd;
        color: #856404;
        padding: 6px 12px;
        border-radius: 8px;
        font-size: 11px;
        line-height: 1.4;
        margin-bottom: 15px;
        border: 1px solid #ffeeba;
        text-align: left;
    }
    
    /* Desain Kotak Kartu Informasi */
    .kartu-kebun {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 15px;
        border-left: 6px solid #4e3629;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
        margin-bottom: 15px;
    }
    div[data-testid="stRadio"] > div {
        background-color: #ffffff;
        padding: 8px;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.03);
    }
    </style>
    """, unsafe_allow_html=True)

# --- BLOK HEADER (CENTER & BERJARAK AMAN) ---
if html_src_logo:
    st.markdown(f"""
        <div style="text-align: center; width: 100%; margin-bottom: 5px; margin-top: 0px;">
            <img src="{html_src_logo}" style="width: 95px; height: auto; image-rendering: -webkit-optimize-contrast; image-rendering: crisp-edges;">
        </div>
    """, unsafe_allow_html=True)

st.markdown("<div class='judul-utama'>Talaga Hangsa KopiPlanPro</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-judul'>Asisten Digital Perawatan Kebun Kopi</div>", unsafe_allow_html=True)

# --- KOREKSI: BOX PERINGATAN KUNING TIPIS BERHASIL DIAKTIFKAN ---
st.markdown("""
    <div class="kotak-warning-petani">
        ⚠️ **PENTING PETANI:** Data tersimpan di HP ini. <b>JANGAN</b> hapus riwayat internet browser Anda agar data tidak hilang. Silakan klik tombol <b>Unduh Cadangan</b> di menu Data Kebun secara berkala.
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
        df_filter = st.session_state.kebun_data[st.session_state.kebun_data['Blok'] == pilihan_blok]
        
        if not df_filter.empty:
            jumlah_pohon = int(df_filter.iloc['Jumlah_Pohon'])
            sistem_pupuk = str(df_filter.iloc['Jenis_Pupuk'])
            
            st.info(f"**Blok Terpilih:** {pilihan_blok} | **Populasi:** {jumlah_pohon} Pohon")
            
            if "Organik" in sistem_pupuk:
                total_kebutuhan = jumlah_pohon * 5.0
