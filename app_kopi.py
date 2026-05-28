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
    .judul-utama { color: #1e3f20 !important; font-family: 'Helvetica Neue', sans-serif; font-weight: 800; text-align: center; text-shadow: 1px 1px 2px rgba(0,0,0,0.1); margin-top: 5px !important; margin-bottom: 2px !important; font-size: 24px; }
    .sub-judul { color: #4a6b4c; font-weight: 500; text-align: center; margin-top: 0px; margin-bottom: 12px; font-size: 13px; }
    .kotak-warning-petani { background-color: #fff3cd; color: #856404; padding: 8px 12px; border-radius: 8px; font-size: 11px; line-height: 1.4; margin-bottom: 20px; border: 1px solid #ffeeba; text-align: left; }
    .kartu-kebun { background-color: #ffffff; padding: 20px; border-radius: 15px; border-left: 6px solid #4e3629; box-shadow: 0 4px 12px rgba(0,0,0,0.04); margin-bottom: 20px; }
    div[data-testid="stRadio"] > div { background-color: #ffffff; padding: 10px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.03); }
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
        ⚠️ **PENTING UNTUK PETANI:** Data kebun Anda tersimpan aman dan terisolasi di memori HP Anda. Jangan bersihkan riwayat internet HP Anda agar data tidak terhapus otomatis.
    </div>
""", unsafe_allow_html=True)

# --- PENGUNCIAN DATA METODE STABLE DATASET ---
if 'kebun_data' not in st.session_state:
    st.session_state.kebun_data = pd.DataFrame(columns=['Blok', 'Lokasi', 'Ketinggian', 'Varietas', 'Jenis_Pupuk', 'Tanggal_Tanam', 'Jumlah_Pohon', 'Status_Musim'])

# --- NAVIGASI MENU UTAMA ---
menu = st.radio("Pilih Menu:", ["📊 Data Kebun", "📅 Jadwal Kerja", "🌱 Tambah Blok"], horizontal=True)
st.write("---")

# 1. MENU: TAMBAH BLOK
if menu == "🌱 Tambah Blok":
    st.markdown("<h3 style='color: #1e3f20;'>🌱 Tambah Blok Kebun Baru</h3>", unsafe_allow_html=True)
    with st.form("form_kebun_baru", clear_on_submit=True):
        nama_blok = st.text_input("Nama Blok Baru", placeholder="Contoh: Blok A")
        lokasi_kebun = st.text_input("Lokasi Kebun (Kabupaten/Kota)", placeholder="Contoh: Garut / Temanggung")
        ketinggian_lahan = st.number_input("Ketinggian Lahan Kebun (mdpl)", min_value=0, max_value=3000, value=800)
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
            new_row = pd.DataFrame([[nama_blok, lokasi_kebun, int(ketinggian_lahan), varietas, jenis_pupuk, str(tgl_tanam), int(jml_pohon), status_musim]], 
                                    columns=['Blok', 'Lokasi', 'Ketinggian', 'Varietas', 'Jenis_Pupuk', 'Tanggal_Tanam', 'Jumlah_Pohon', 'Status_Musim'])
            st.session_state.kebun_data = pd.concat([st.session_state.kebun_data, new_row], ignore_index=True)
            st.success(f"🎉 Sukses! {nama_blok} berhasil disimpan.")
            st.toast("Data kebun berhasil dikunci ke memori aplikasi!", icon="💾")

# 2. MENU: DATA KEBUN
elif menu == "📊 Data Kebun":
    st.markdown("<h3 style='color: #1e3f20;'>📊 Ringkasan Kebun</h3>", unsafe_allow_html=True)
    
    if st.session_state.kebun_data.empty:
        st.info("📲 Belum ada data kebun Anda. Silakan isi data baru di menu '🌱 Tambah Blok'.")
    else:
        total_pohon = st.session_state.kebun_data['Jumlah_Pohon'].sum()
        st.metric(label="Total Semua Pohon Kopi Dikelola", value=f"{total_pohon} Batang")
        st.write("")
        
        for idx, row in st.session_state.kebun_data.iterrows():
            st.markdown(f"""
                <div class="kartu-kebun">
                    <h3 style="margin-top:0; color:#4e3629;">📍 Blok: {row['Blok']}</h3>
                    <p style="margin:3px 0; font-size:14px;">🗺️ <b>Lokasi:</b> {row['Lokasi']} | 🏔️ <b>Ketinggian:</b> {row['Ketinggian']} mdpl</p>
                    <p style="margin:3px 0; font-size:14px;">🌱 <b>Varietas:</b> Kopi {row['Varietas']} | 🌦️ <b>Cuaca:</b> {row['Status_Musim']}</p>
                    <p style="margin:3px 0; font-size:14px;">🟫 <b>Sistem Pupuk:</b> {row['Jenis_Pupuk']}</p>
                    <p style="margin:5px 0 0 0; color:#666; font-size:13px;"><b>Populasi:</b> {row['Jumlah_Pohon']} Pohon | <b>Tanggal Tanam:</b> {row['Tanggal_Tanam']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"🗑️ Hapus {row['Blok']}", key=f"hapus_{row['Blok']}_{idx}"):
                st.session_state.kebun_data = st.session_state.kebun_data.drop(idx).reset_index(drop=True)
                st.rerun()

# 3. MENU: JADWAL KERJA (URUTAN WAKTEDU TERDEKAT GLOBAL FIX LINTAS BLOK)
elif menu == "📅 Jadwal Kerja":
    st.markdown("<h3 style='color: #1e3f20;'>📅 Daftar Tugas Pemeliharaan</h3>", unsafe_allow_html=True)
    
    if st.session_state.kebun_data.empty:
        st.info("📲 Belum ada jadwal tugas. Tambahkan data kebun terlebih dahulu di menu '🌱 Tambah Blok'.")
    else:
        keranjang_tugas_global = []
        
        for idx, row in st.session_state.kebun_data.iterrows():
            blok_id = row['Blok']
            lokasi = row['Lokasi']
            musim = row['Status_Musim']
            h_mdpl = int(row['Ketinggian'])
            var_kopi = row['Varietas']
            
            tgl_str = str(row['Tanggal_Tanam'])
            try:
                tgl_obj = datetime.strptime(tgl_str, "%Y-%m-%d")
            except:
                tgl_obj = datetime.now()
            
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
                tgl_target = tgl_obj + timedelta(days=jeda_hari)
                keranjang_tugas_global.append({
                    "nama_tugas": nama_tugas,
                    "tgl_target": tgl_target,
                    "blok": blok_id,
                    "lokasi": lokasi,
                    "mdpl": h_mdpl,
                    "varietas": var_kopi
                })
        
        # Urutkan seluruh daftar tugas berdasarkan waktu pengerjaan yang paling dekat
        keranjang_tugas_global.sort(key=lambda x: x["tgl_target"])
        hari_ini = datetime.now()
        
        for tgs in keranjang_tugas_global:
            tgl_indo = tgs["tgl_target"].strftime('%d %b %Y')
            
            if tgs["tgl_target"] < hari_ini:
                label_waktu = "🚨 **SUDAH LEWAT JADWAL**"
            else:
                selisih = (tgs["tgl_target"] - hari_ini).days
                label_waktu = f"⏳ **JADWAL {selisih} HARI LAGI**"
            
            with st.container():
