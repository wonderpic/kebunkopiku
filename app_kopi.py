import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="KopiPlan Pro", layout="centered")
st.title("☕ KopiPlan Pro")
st.caption("Aplikasi Penjadwalan Kebun Kopi")

# --- SISTEM KUNCI DATA PERMANEN DENGAN SECRETS ---
if 'kebun_data' not in st.session_state:
    # Membaca data yang dikunci secara permanen dari dashboard
    if "KEBUN_DATA" in st.secrets:
        st.session_state.kebun_data = pd.DataFrame(st.secrets["KEBUN_DATA"])
    else:
        st.session_state.kebun_data = pd.DataFrame(columns=['Blok', 'Varietas', 'Jenis Pupuk', 'Tanggal Tanam', 'Jumlah Pohon', 'Status Musim'])

# --- NAVIGASI NAVIGASI ---
menu = st.radio("Pilih Menu:", ["📊 Data Kebun", "📅 Jadwal & Peringatan", "🧮 Kalkulator Pupuk", "🌱 Tambah Blok"], horizontal=True)

if menu == "🌱 Tambah Blok":
    st.subheader("🌱 Tambah Blok Kebun Baru")
    with st.form("form_kebun"):
        nama_blok = st.text_input("Nama Blok")
        varietas = st.selectbox("Varietas Kopi", ["Arabika", "Robusta"])
        jenis_pupuk = st.selectbox("Metode Pemupukan Utama", ["Organik (Kompos/Kohe)", "Non-Organik (Kimia/NPK)"])
        status_musim = st.selectbox("Kondisi Cuaca Saat Ini", ["Musim Kemarau", "Musim Hujan"])
        tgl_tanam = st.date_input("Tanggal Tanam", datetime.now().date())
        jml_pohon = st.number_input("Jumlah Pohon (Batang)", min_value=1, value=100)
        submit = st.form_submit_button("⚡ Simpan Blok")

    if submit and nama_blok:
        new_row = pd.DataFrame([[nama_blok, varietas, jenis_pupuk, tgl_tanam, jml_pohon, status_musim]], 
                                columns=['Blok', 'Varietas', 'Jenis Pupuk', 'Tanggal Tanam', 'Jumlah Pohon', 'Status Musim'])
        st.session_state.kebun_data = pd.concat([st.session_state.kebun_data, new_row], ignore_index=True)
        st.success(f"Blok {nama_blok} berhasil ditambahkan!")
        
        # Tampilkan teks kunci untuk Anda salin ke dashboard secrets
        st.info("💡 DATA BARU ANDA SUDAH SIAP. LAKUKAN LANGKAH NOMOR 3 DI BAWAH UNTUK MENGUNCINYA AGAR TIDAK HILANG.")

elif menu == "📊 Data Kebun":
    st.subheader("Ringkasan Kebun")
    if st.session_state.kebun_data.empty:
        st.info("Belum ada data kebun.")
    else:
        for idx, row in st.session_state.kebun_data.iterrows():
            st.markdown(f"### 📍 Blok: {row['Blok']} ({row['Varietas']})")
            st.markdown(f"Sistem: {row['Jenis Pupuk']} | Populasi: {row['Jumlah Pohon']} Pohon")
            st.write("---")

elif menu == "📅 Jadwal & Peringatan":
    st.subheader("📋 Daftar Tugas Kebun")
    if st.session_state.kebun_data.empty:
        st.info("Belum ada data kebun.")
    else:
        for idx, row in st.session_state.kebun_data.iterrows():
            st.markdown(f"### 📍 Target Kerja: {row['Blok']}")
            st.error(f"🚨 **BELUM DIKERJAKAN:** Pengecekan Rutin Hama & Penyiraman Blok {row['Blok']}")
            st.write("---")

elif menu == "🧮 Kalkulator Pupuk":
    st.subheader("🧮 Kalkulator Kebutuhan Pupuk")
    if st.session_state.kebun_data.empty:
        st.info("Belum ada data kebun.")
    else:
        pilihan_blok = st.selectbox("Pilih Blok:", st.session_state.kebun_data['Blok'].unique())
        data_blok = st.session_state.kebun_data[st.session_state.kebun_data['Blok'] == pilihan_blok].iloc[0]
        st.metric(label="Total Kebutuhan Estimasi Pupuk", value=f"{data_blok['Jumlah Pohon'] * 5} Kg")
