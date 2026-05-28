import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Konfigurasi Halaman Mobile-Friendly
st.set_page_config(page_title="KopiPlan Smart", layout="centered")

st.title("☕ KopiPlan Smart")
st.caption("Sistem Penjadwalan Speimport streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Konfigurasi Halaman Mobile-Friendly
st.set_page_config(page_title="KopiPlan Pro", layout="centered")

st.title("☕ KopiPlan Pro")
st.caption("Sistem Penjadwalan Kebun Kopi dengan Fitur Peringatan")

# 1. Inisialisasi Database Kebun
if 'kebun_data' not in st.session_state:
    st.session_state.kebun_data = pd.DataFrame(columns=['Blok', 'Varietas', 'Jenis Pupuk', 'Tanggal Tanam', 'Jumlah Pohon'])

# 2. Inisialisasi Database Status Tugas (Ceklis)
if 'status_tugas' not in st.session_state:
    st.session_state.status_tugas = {}

# --- MENU NAVIGASI BAWAH (MOBILE OPTIMIZED) ---
menu = st.radio("Pilih Menu:", ["📊 Data Kebun", "📅 Jadwal & Peringatan", "➕ Tambah Blok"], horizontal=True)

# --- MENU: TAMBAH BLOK ---
if menu == "➕ Tambah Blok":
    st.subheader("🌱 Tambah Blok Kebun Baru")
    with st.form("form_kebun"):
        nama_blok = st.text_input("Nama Blok", placeholder="Contoh: Blok A / Lereng")
        varietas = st.selectbox("Varietas Kopi", ["Arabika", "Robusta"])
        jenis_pupuk = st.selectbox("Metode Pemupukan Utama", ["Organik (Kompos/Kohe)", "Non-Organik (Kimia/NPK)"])
        tgl_tanam = st.date_input("Tanggal Tanam", datetime.now())
        jml_pohon = st.number_input("Jumlah Pohon", min_value=1, value=100)
        submit_button = st.form_submit_button(label="⚡ Simpan Blok")

    if submit_button and nama_blok:
        # Cek apakah nama blok sudah ada untuk menghindari duplikasi
        if nama_blok in st.session_state.kebun_data['Blok'].values:
            st.error(f"Nama Blok '{nama_blok}' sudah ada! Gunakan nama lain.")
        else:
            new_data = pd.DataFrame([[nama_blok, varietas, jenis_pupuk, tgl_tanam, jml_pohon]], 
                                    columns=['Blok', 'Varietas', 'Jenis Pupuk', 'Tanggal Tanam', 'Jumlah Pohon'])
            st.session_state.kebun_data = pd.concat([st.session_state.kebun_data, new_data], ignore_index=True)
            st.success(f"Blok {nama_blok} berhasil disimpan!")

# --- MENU: DATA KEBUN ---
elif menu == "📊 Data Kebun":
    st.subheader("Ringkasan Kebun")
    if st.session_state.kebun_data.empty:
        st.info("Belum ada data. Pilih menu '➕ Tambah Blok' terlebih dahulu.")
    else:
        total_pohon = st.session_state.kebun_data['Jumlah Pohon'].sum()
        st.metric(label="Total Pohon Dikelola", value=f"{total_pohon} Batang")
        
        st.write("---")
        for index, row in st.session_state.kebun_data.iterrows():
            with st.container():
                st.markdown(f"### 📍 Blok: {row['Blok']}")
                st.markdown(f"**Varietas:** Kopi {row['Varietas']} | **Sistem Pupuk:** {row['Jenis Pupuk']}")
                st.markdown(f"**Populasi:** {row['Jumlah Pohon']} Pohon | **Tanggal Tanam:** {row['Tanggal Tanam']}")
                st.write("---")

# --- MENU: JADWAL & PERINGATAN (SISTEM SMART CHECKLIST) ---
elif menu == "📅 Jadwal & Peringatan":
    st.subheader("📋 Daftar Tugas Kebun")
    
    if st.session_state.kebun_data.empty:
        st.info("Belum ada jadwal. Tambahkan data blok kebun terlebih dahulu.")
    else:
        for index, row in st.session_state.kebun_data.iterrows():
            blok_id = row['Blok']
            tgl = pd.to_datetime(row['Tanggal Tanam'])
            
            st.markdown(f"### 📍 Blok Kerja: **{blok_id}** ({row['Varietas']})")
            
            # Membuat daftar tugas berdasarkan input jenis pupuk dan varietas kopi
            if row['Jenis Pupuk'] == "Organik (Kompos/Kohe)":
                tugas_list = [
                    ("🟫 Aplikasi Pupuk Dasar (Kompos)", 14),
                    ("🟫 Pemupukan Organik Tahap 1", 120),
                    ("🟫 Pemupukan Organik Tahap 2", 240)
                ]
            else:
                tugas_list = [
                    ("🧪 Aplikasi Pupuk Kimia Dasar", 30),
                    ("🧪 Pemupukan NPK Vegetatif", 90),
                    ("🧪 Pemupukan NPK Generatif", 180)
                ]
            
            if row['Varietas'] == "Arabika":
                tugas_list += [
                    ("✂️ Pangkas Bentuk Batang Tunggal", 365),
                    ("🍒 Estimasi Panen Perdana Arabika", 730)
                ]
            else:
                tugas_list += [
                    ("✂️ Pangkas Wiwilan Tunas Air", 60),
                    ("🍒 Estimasi Panen Perdana Robusta", 900)
                ]
                
            # Tampilkan tugas satu per satu dengan sistem warning pintar
            for nama_tugas, jeda_hari in tugas_list:
                tgl_target = tgl + timedelta(days=jeda_hari)
                tgl_indo = tgl_target.strftime('%d %b %Y')
                
                # ID Unik untuk setiap tugas di memori agar status ceklisnya tidak tertukar
                key_id = f"{blok_id}_{nama_tugas}_{jeda_hari}"
                
                # Set default status belum selesai (False) jika belum terdaftar di memori
                if key_id not in st.session_state.status_tugas:
                    st.session_state.status_tugas[key_id] = False
                
                # Kotak Kontainer Tugas
                with st.container():
                    # Jika belum dikerjakan, munculkan baris peringatan merah terang
                    if not st.session_state.status_tugas[key_id]:
                        st.error(f"🚨 **BELUM DIKERJAKAN!** \n\n **{nama_tugas}** \n\n Target Batas Waktu: {tgl_indo}")
                        # Tombol untuk menyelesaikan tugas dan mematikan warning
                        if st.button(f"✅ Tandai Selesai: {nama_tugas}", key=f"btn_{key_id}"):
                            st.session_state.status_tugas[key_id] = True
                            st.rerun() # Refresh halaman otomatis untuk mengubah warna warning
                    
                    # Jika sudah dikerjakan, warna berubah menjadi hijau aman dan tenang
                    else:
                        st.success(f"🎉 **SUDAH SELESAI** \n\n **{nama_tugas}** (Selesai dilakukan)")
                        # Tombol opsional jika ingin membatalkan/mereset kembali ke status belum selesai
                        if st.button(f"🔄 Batalkan Selesai", key=f"reset_{key_id}"):
                            st.session_state.status_tugas[key_id] = False
                            st.rerun()
                st.write("") # Jarak antar kartu tugas
            st.markdown("---")
sifik Varietas & Jenis Pupuk")

# Inisialisasi Data State
if 'kebun_data' not in st.session_state:
    st.session_state.kebun_data = pd.DataFrame(columns=['Blok', 'Varietas', 'Jenis Pupuk', 'Tanggal Tanam', 'Jumlah Pohon'])

# --- MENU NAVIGASI BAWAH ---
menu = st.radio("Pilih Menu:", ["📊 Data Kebun", "📅 Jadwal Kerja", "➕ Tambah Blok"], horizontal=True)

# --- MENU: TAMBAH BLOK ---
if menu == "➕ Tambah Blok":
    st.subheader("🌱 Tambah Blok Kebun")
    with st.form("form_kebun"):
        nama_blok = st.text_input("Nama Blok", placeholder="Contoh: Blok A / Lereng")
        varietas = st.selectbox("Varietas Kopi", ["Arabika", "Robusta"])
        jenis_pupuk = st.selectbox("Metode Pemupukan Utama", ["Organik (Kompos/Kohe)", "Non-Organik (Kimia/NPK)"])
        tgl_tanam = st.date_input("Tanggal Tanam", datetime.now())
        jml_pohon = st.number_input("Jumlah Pohon", min_value=1, value=100)
        submit_button = st.form_submit_button(label="⚡ Simpan Blok")

    if submit_button and nama_blok:
        new_data = pd.DataFrame([[nama_blok, varietas, jenis_pupuk, tgl_tanam, jml_pohon]], 
                                columns=['Blok', 'Varietas', 'Jenis Pupuk', 'Tanggal Tanam', 'Jumlah Pohon'])
        st.session_state.kebun_data = pd.concat([st.session_state.kebun_data, new_data], ignore_index=True)
        st.success(f"Blok {nama_blok} berhasil disimpan!")

# --- MENU: DATA KEBUN ---
elif menu == "📊 Data Kebun":
    st.subheader("Ringkasan Kebun")
    if st.session_state.kebun_data.empty:
        st.info("Belum ada data. Pilih menu '➕ Tambah Blok' terlebih dahulu.")
    else:
        total_pohon = st.session_state.kebun_data['Jumlah Pohon'].sum()
        st.metric(label="Total Pohon Dikelola", value=f"{total_pohon} Batang")
        
        st.write("---")
        for index, row in st.session_state.kebun_data.iterrows():
            with st.container():
                st.markdown(f"### 📍 {row['Blok']}")
                st.markdown(f"**Jenis:** Kopi {row['Varietas']}")
                st.markdown(f"**Sistem Pupuk:** {row['Jenis Pupuk']}")
                st.markdown(f"**Populasi:** {row['Jumlah Pohon']} Pohon | **Tanam:** {row['Tanggal Tanam']}")
                st.write("---")

# --- MENU: JADWAL KERJA (LOGIKA SPESIFIK) ---
elif menu == "📅 Jadwal Kerja":
    st.subheader("Jadwal Kerja Spesifik Kebun Anda")
    if st.session_state.kebun_data.empty:
        st.info("Belum ada jadwal. Tambahkan data blok kebun terlebih dahulu.")
    else:
        for index, row in st.session_state.kebun_data.iterrows():
            tgl = pd.to_datetime(row['Tanggal Tanam'])
            st.markdown(f"### 📍 Target Kerja: {row['Blok']} ({row['Varietas']})")
            
            # 1. LOGIKA JADWAL PEMUPUKAN (Berdasarkan Pilihan Pupuk)
            if row['Jenis Pupuk'] == "Organik (Kompos/Kohe)":
                tugas_pupuk = [
                    ("🟫 Aplikasi Pupuk Dasar (Kompos/Kohe Matang)", tgl + timedelta(days=14)),
                    ("🟫 Pemupukan Organik Susulan Tahap 1", tgl + timedelta(days=120)),
                    ("🟫 Pemupukan Organik Berkala & Mulsa", tgl + timedelta(days=240))
                ]
            else:
                tugas_pupuk = [
                    ("🧪 Aplikasi Pupuk Kimia Dasar (Awal Tanam)", tgl + timedelta(days=30)),
                    ("🧪 Pemupukan NPK Susulan (Masa Vegetatif)", tgl + timedelta(days=90)),
                    ("🧪 Pemupukan NPK + Unsur Mikro (Masa Generatif)", tgl + timedelta(days=180))
                ]
            
            # 2. LOGIKA JADWAL PEMELIHARAAN & PANEN (Berdasarkan Varietas)
            if row['Varietas'] == "Arabika":
                tugas_varietas = [
                    ("✂️ Pangkas Bentuk (Single Stem / Batang Tunggal)", tgl + timedelta(days=365)),
                    ("🍒 Estimasi Panen Perdana Arabika (Mulai Berbunga)", tgl + timedelta(days=730)) # Generatif lebih cepat di dataran tinggi tertentu
                ]
            else: # Robusta
                tugas_varietas = [
                    ("✂️ Pangkas Wiwilan (Robusta cenderung lebih rimbun/tunas air cepat tumbuh)", tgl + timedelta(days=60)),
                    ("✂️ Pangkas Rejuvenasi / Lepas Batang", tgl + timedelta(days=450)),
                    ("🍒 Estimasi Panen Perdana Robusta (Masa Matang Ceri Lebih Lama)", tgl + timedelta(days=900))
                ]
            
            # Gabungkan semua tugas dan urutkan berdasarkan tanggal target
            semua_tugas = tugas_pupuk + tugas_varietas
            semua_tugas.sort(key=lambda x: x[1])
            
            # Tampilkan ke layar HP
            for nama_tugas, tgl_target in semua_tugas:
                tgl_indo = tgl_target.strftime('%d %b %Y')
                st.info(f"**{nama_tugas}** \n\n Jadwal: {tgl_indo}")
            
            st.write("---")
