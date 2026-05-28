import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Konfigurasi Halaman agar Pas di Layar HP
st.set_page_config(page_title="KopiPlan Mobile", layout="centered")

st.title("☕ KopiPlan Mobile")
st.caption("Asisten Penjadwalan Kebun Kopi Anda")

# Inisialisasi Data State (Simulasi Database)
if 'kebun_data' not in st.session_state:
    st.session_state.kebun_data = pd.DataFrame(columns=['Blok', 'Varietas', 'Tanggal Tanam', 'Jumlah Pohon'])

# --- MENU NAVIGASI BAWAH (Cocok untuk HP) ---
menu = st.radio("Pilih Menu:", ["📊 Data Kebun", "📅 Jadwal Kerja", "➕ Tambah Blok"], horizontal=True)

# --- MENU: TAMBAH BLOK ---
if menu == "➕ Tambah Blok":
    st.subheader("🌱 Tambah Blok Kebun")
    with st.form("form_kebun"):
        nama_blok = st.text_input("Nama Blok", placeholder="Contoh: Blok A / Lereng")
        varietas = st.selectbox("Varietas Kopi", ["Arabika", "Robusta", "Liberika"])
        tgl_tanam = st.date_input("Tanggal Tanam", datetime.now())
        jml_pohon = st.number_input("Jumlah Pohon", min_value=1, value=100)
        submit_button = st.form_submit_button(label="⚡ Simpan Blok")

    if submit_button and nama_blok:
        new_data = pd.DataFrame([[nama_blok, varietas, tgl_tanam, jml_pohon]], 
                                columns=['Blok', 'Varietas', 'Tanggal Tanam', 'Jumlah Pohon'])
        st.session_state.kebun_data = pd.concat([st.session_state.kebun_data, new_data], ignore_index=True)
        st.success(f"Blok {nama_blok} berhasil disimpan!")

# --- MENU: DATA KEBUN ---
elif menu == "📊 Data Kebun":
    st.subheader("Ringkasan Kebun")
    if st.session_state.kebun_data.empty:
        st.info("Belum ada data. Pilih menu '➕ Tambah Blok' terlebih dahulu.")
    else:
        # Metrik Besar untuk Layar HP
        total_pohon = st.session_state.kebun_data['Jumlah Pohon'].sum()
        st.metric(label="Total Pohon Dikelola", value=f"{total_pohon} Batang")
        
        st.write("---")
        # Menampilkan data dalam bentuk kartu, bukan tabel lebar
        for index, row in st.session_state.kebun_data.iterrows():
            with st.container():
                st.markdown(f"### 📍 {row['Blok']}")
                st.markdown(f"**Jenis:** {row['Varietas']} | **Populasi:** {row['Jumlah Pohon']} Pohon")
                st.markdown(f"📅 **Tanam:** {row['Tanggal Tanam']}")
                st.write("---")

# --- MENU: JADWAL KERJA ---
elif menu == "📅 Jadwal Kerja":
    st.subheader("Aktivitas yang Harus Dilakukan")
    if st.session_state.kebun_data.empty:
        st.info("Belum ada jadwal. Tambahkan data blok kebun terlebih dahulu.")
    else:
        for index, row in st.session_state.kebun_data.iterrows():
            tgl = pd.to_datetime(row['Tanggal Tanam'])
            
            st.markdown(f"#### 🪵 Target Kerja: {row['Blok']}")
            
            # Daftar Tugas berbentuk list vertikal yang mudah dibaca di HP
            tugas = [
                ("🌿 Pemupukan Organik", tgl + timedelta(days=30)),
                ("✂️ Pangkas Tunas Air", tgl + timedelta(days=90)),
                ("🧪 Pupuk NPK Tahap 1", tgl + timedelta(days=180)),
                ("🍒 Estimasi Panen", tgl + timedelta(days=730))
            ]
            
            for nama_tugas, tgl_target in tugas:
                tgl_indo = tgl_target.strftime('%d %b %Y')
                # Menggunakan status sukses jika sudah lewat atau info untuk rencana
                st.info(f"**{nama_tugas}** \n\n Target: {tgl_indo}")
            
            st.write("---")
