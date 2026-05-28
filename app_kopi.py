import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Konfigurasi Halaman Mobile-Friendly
st.set_page_config(page_title="KopiPlan Max", layout="centered")

st.title("☕ KopiPlan Max")
st.caption("Sistem Manajemen Kebun Kopi Terpadu")

# 1. Inisialisasi Database Kebun
if 'kebun_data' not in st.session_state:
    st.session_state.kebun_data = pd.DataFrame(columns=['Blok', 'Varietas', 'Jenis Pupuk', 'Tanggal Tanam', 'Jumlah Pohon', 'Status Musim'])

# 2. Inisialisasi Database Status Tugas (Ceklis)
if 'status_tugas' not in st.session_state:
    st.session_state.status_tugas = {}

# --- MENU NAVIGASI BAWAH (MOBILE OPTIMIZED) ---
menu = st.radio("Pilih Menu:", ["📊 Data Kebun", "📅 Jadwal & Peringatan", "🧮 Kalkulator Pupuk", "🌱 Tambah Blok"], horizontal=True)

# --- MENU: TAMBAH BLOK ---
if menu == "🌱 Tambah Blok":
    st.subheader("🌱 Tambah Blok Kebun Baru")
    with st.form("form_kebun"):
        nama_blok = st.text_input("Nama Blok", placeholder="Contoh: Blok A / Lereng")
        varietas = st.selectbox("Varietas Kopi", ["Arabika", "Robusta"])
        jenis_pupuk = st.selectbox("Metode Pemupukan Utama", ["Organik (Kompos/Kohe)", "Non-Organik (Kimia/NPK)"])
        status_musim = st.selectbox("Kondisi Cuaca Saat Ini", ["Musim Kemarau", "Musim Hujan"])
        tgl_tanam = st.date_input("Tanggal Tanam", datetime.now())
        jml_pohon = st.number_input("Jumlah Pohon (Batang)", min_value=1, value=100)
        submit_button = st.form_submit_button(label="⚡ Simpan Blok")

    if submit_button and nama_blok:
        if nama_blok in st.session_state.kebun_data['Blok'].values:
            st.error(f"Nama Blok '{nama_blok}' sudah ada! Gunakan nama lain.")
        else:
            new_data = pd.DataFrame([[nama_blok, varietas, jenis_pupuk, tgl_tanam, jml_pohon, status_musim]], 
                                    columns=['Blok', 'Varietas', 'Jenis Pupuk', 'Tanggal Tanam', 'Jumlah Pohon', 'Status Musim'])
            st.session_state.kebun_data = pd.concat([st.session_state.kebun_data, new_data], ignore_index=True)
            st.success(f"Blok {nama_blok} berhasil disimpan!")

# --- MENU: DATA KEBUN ---
elif menu == "📊 Data Kebun":
    st.subheader("Ringkasan Kebun")
    if st.session_state.kebun_data.empty:
        st.info("Belum ada data. Pilih menu '🌱 Tambah Blok' terlebih dahulu.")
    else:
        total_pohon = st.session_state.kebun_data['Jumlah Pohon'].sum()
        st.metric(label="Total Pohon Dikelola", value=f"{total_pohon} Batang")
        
        st.write("---")
        for index, row in st.session_state.kebun_data.iterrows():
            with st.container():
                st.markdown(f"### 📍 Blok: {row['Blok']}")
                st.markdown(f"**Varietas:** Kopi {row['Varietas']} | **Cuaca:** {row['Status Musim']}")
                st.markdown(f"**Sistem Pupuk:** {row['Jenis Pupuk']}")
                st.markdown(f"**Populasi:** {row['Jumlah Pohon']} Pohon | **Tanggal Tanam:** {row['Tanggal Tanam']}")
                st.write("---")

# --- MENU: JADWAL & PERINGATAN (TERMASUK PENYIRAMAN & PENGECEKAN RUTIN) ---
elif menu == "📅 Jadwal & Peringatan":
    st.subheader("📋 Daftar Tugas Kebun")
    
    if st.session_state.kebun_data.empty:
        st.info("Belum ada jadwal. Tambahkan data blok kebun terlebih dahulu.")
    else:
        for index, row in st.session_state.kebun_data.iterrows():
            blok_id = row['Blok']
            tgl = pd.to_datetime(row['Tanggal Tanam'])
            musim = row['Status Musim']
            
            st.markdown(f"### 📍 Blok Kerja: **{blok_id}** ({row['Varietas']})")
            
            tugas_list = []
            
            # A. LOGIKA JADWAL PEMUPUKAN UTAMA
            if row['Jenis Pupuk'] == "Organik (Kompos/Kohe)":
                tugas_list += [("🟫 Aplikasi Pupuk Dasar (Kompos)", 14), ("🟫 Pemupukan Organik Tahap 1", 120)]
            else:
                tugas_list += [("🧪 Aplikasi Pupuk Kimia Dasar", 30), ("🧪 Pemupukan NPK Vegetatif", 90)]
            
            # B. LOGIKA JADWAL VARIETAS
            if row['Varietas'] == "Arabika":
                tugas_list += [("✂️ Pangkas Bentuk Batang Tunggal", 365), ("🍒 Estimasi Panen Perdana Arabika", 730)]
            else:
                tugas_list += [("✂️ Pangkas Wiwilan Tunas Air", 60), ("🍒 Estimasi Panen Perdana Robusta", 900)]
            
            # C. LOGIKA JADWAL PENYIRAMAN (Berdasarkan Musim)
            if musim == "Musim Kemarau":
                tugas_list += [
                    ("💧 Penyiraman Rutin Kemarau Tahap 1", 3),
                    ("💧 Penyiraman Rutin Kemarau Tahap 2", 6),
                    ("💧 Penyiraman Rutin Kemarau Tahap 3", 9)
                ]
            else:
                tugas_list += [
                    ("🌧️ Cek Saluran Drainase (Cegah Akar Busuk akibat Hujan)", 5),
                    ("🌧️ Pembersihan Gulma Ringan (Gulma cepat tumbuh di musim hujan)", 15)
                ]
                
            # D. LOGIKA JADWAL PENGECEKAN RUTIN (Hama & Penyakit)
            tugas_list += [
                ("🔍 Pengecekan Rutin Hama Penggerek Buah Kopi (PBKo)", 7),
                ("🔍 Pengecekan Rutin Penyakit Karat Daun (Hemileia vastatrix)", 14),
                ("🔍 Inspeksi Kesehatan Batang & Kutu Putih", 21)
            ]
                
            # Urutkan tugas berdasarkan hari tercepat
            tugas_list.sort(key=lambda x: x[1])
            
            # Tampilkan tugas satu per satu dengan warning
            for nama_tugas, jeda_hari in tugas_list:
                tgl_target = tgl + timedelta(days=jeda_hari)
                tgl_indo = tgl_target.strftime('%d %b %Y')
                key_id = f"{blok_id}_{nama_tugas}_{jeda_hari}"
                
                if key_id not in st.session_state.status_tugas:
                    st.session_state.status_tugas[key_id] = False
                
                with st.container():
                    if not st.session_state.status_tugas[key_id]:
                        st.error(f"🚨 **BELUM DIKERJAKAN!** \n\n **{nama_tugas}** \n\n Batas Waktu: {tgl_indo}")
                        if st.button(f"✅ Selesai: {nama_tugas}", key=f"btn_{key_id}"):
                            st.session_state.status_tugas[key_id] = True
                            st.rerun()
                    else:
                        st.success(f"🎉 **SUDAH SELESAI** \n\n **{nama_tugas}**")
                        if st.button(f"🔄 Batalkan", key=f"reset_{key_id}"):
                            st.session_state.status_tugas[key_id] = False
                            st.rerun()
                st.write("") 
            st.markdown("---")

# --- MENU: KALKULATOR PUPUK OTOMATIS ---
elif menu == "🧮 Kalkulator Pupuk":
    st.subheader("🧮 Kalkulator Kebutuhan Pupuk Kebun")
    
    if st.session_state.kebun_data.empty:
        st.info("Masukkan data blok kebun terlebih dahulu untuk menghitung pupuk otomatis.")
    else:
        # Pilih blok kebun yang ingin dihitung
        pilihan_blok = st.selectbox("Pilih Blok Kebun:", st.session_state.kebun_data['Blok'].unique())
        
        # Ambil data jumlah pohon berdasarkan blok yang dipilih
        data_blok_terpilih = st.session_state.kebun_data[st.session_state.kebun_data['Blok'] == pilihan_blok].iloc[0]
        jumlah_pohon = data_blok_terpilih['Jumlah Pohon']
        sistem_pupuk = data_blok_terpilih['Jenis Pupuk']
        
        st.info(f"**Blok Terpilih:** {pilihan_blok} | **Populasi:** {jumlah_pohon} Pohon")
        
        st.write("### Estimasi Kebutuhan Sekali Pemupukan:")
        
        if "Organik" in sistem_pupuk:
            # Standar rata-rata: 5 kg (5000 gram) kompos per pohon muda/dewasa awal
            dosis_per_pohon = 5.0 # kg
            total_kebutuhan = jumlah_pohon * dosis_per_pohon
            
            st.metric(label="Total Pupuk Kompos/Kohe yang Diperlukan", value=f"{total_kebutuhan:,.1f} Kg")
            st.caption(f"💡 Perhitungan berdasarkan dosis rekomendasi standar: **{dosis_per_pohon} Kg** pupuk organik matang per lubang tanam/pohon.")
        
        else:
            # Standar rata-rata pupuk kimia NPK: 100 gram per pohon untuk masa vegetatif/awal
            dosis_per_pohon_gram = 100 # gram
            total_kebutuhan_gram = jumlah_pohon * dosis_per_pohon_gram
            total_kebutuhan_kg = total_kebutuhan_gram / 1000
            
            st.metric(label="Total Pupuk NPK Kimia yang Diperlukan", value=f"{total_kebutuhan_kg:,.1f} Kg")
            st.caption(f"💡 Perhitungan berdasarkan dosis rekomendasi standar: **{dosis_per_pohon_gram} gram** NPK per pohon.")
            
        st.warning("⚠️ Catatan: Dosis di atas adalah estimasi dasar. Sesuaikan kembali dengan tingkat kesuburan tanah dan umur aktual pohon kopi Anda.")
