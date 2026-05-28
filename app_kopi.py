import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# Konfigurasi Halaman Mobile-Friendly
st.set_page_config(page_title="KopiPlan Max Permanent", layout="centered")

st.title("☕ KopiPlan Max")
st.caption("Sistem Manajemen Kebun Kopi Terpadu (Data Permanen Aman)")

# --- SISTEM PENYIMPANAN DATA PERMANEN (CSV) ---
FILE_KEBUN = "database_kebun.csv"
FILE_TUGAS = "database_tugas.csv"

# Fungsi memuat data kebun dari file CSV
def muat_data_kebun():
    if os.path.exists(FILE_KEBUN):
        try:
            df = pd.read_csv(FILE_KEBUN)
            # Pastikan format tanggal konsisten
            if 'Tanggal Tanam' in df.columns:
                df['Tanggal Tanam'] = pd.to_datetime(df['Tanggal Tanam']).dt.date
            return df
        except:
            return pd.DataFrame(columns=['Blok', 'Varietas', 'Jenis Pupuk', 'Tanggal Tanam', 'Jumlah Pohon', 'Status Musim'])
    return pd.DataFrame(columns=['Blok', 'Varietas', 'Jenis Pupuk', 'Tanggal Tanam', 'Jumlah Pohon', 'Status Musim'])

# Fungsi memuat status tugas dari file CSV
def muat_data_tugas():
    status_dict = {}
    if os.path.exists(FILE_TUGAS):
        try:
            df = pd.read_csv(FILE_TUGAS)
            for _, row in df.iterrows():
                # Ubah string 'True'/'False' kembali menjadi tipe data Boolean asli
                status_dict[row['Key_ID']] = bool(row['Status'])
        except:
            pass
    return status_dict

# Fungsi menyimpan data kebun ke CSV
def simpan_data_kebun(df):
    df.to_csv(FILE_KEBUN, index=False)

# Fungsi menyimpan status tugas ke CSV
def simpan_data_tugas(status_dict):
    df = pd.DataFrame(list(status_dict.items()), columns=['Key_ID', 'Status'])
    df.to_csv(FILE_TUGAS, index=False)

# Sinkronisasi data awal saat aplikasi pertama kali dibuka
if 'kebun_data' not in st.session_state:
    st.session_state.kebun_data = muat_data_kebun()

if 'status_tugas' not in st.session_state:
    st.session_state.status_tugas = muat_data_tugas()


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
        tgl_tanam = st.date_input("Tanggal Tanam", datetime.now().date())
        jml_pohon = st.number_input("Jumlah Pohon (Batang)", min_value=1, value=100)
        submit_button = st.form_submit_button(label="⚡ Simpan Blok Permanen")

    if submit_button and nama_blok:
        # Cek duplikasi data
        if not st.session_state.kebun_data.empty and nama_blok in st.session_state.kebun_data['Blok'].values:
            st.error(f"Nama Blok '{nama_blok}' sudah ada! Gunakan nama lain.")
        else:
            new_data = pd.DataFrame([[nama_blok, varietas, jenis_pupuk, tgl_tanam, jml_pohon, status_musim]], 
                                    columns=['Blok', 'Varietas', 'Jenis Pupuk', 'Tanggal Tanam', 'Jumlah Pohon', 'Status Musim'])
            
            # Gabungkan data baru ke memory session state
            st.session_state.kebun_data = pd.concat([st.session_state.kebun_data, new_data], ignore_index=True)
            
            # LANGSUNG KUNCI DAN SIMPAN KE FILE FISIK CSV
            simpan_data_kebun(st.session_state.kebun_data)
            st.success(f"Blok {nama_blok} berhasil disimpan secara permanen!")

# --- MENU: DATA KEBUN ---
elif menu == "📊 Data Kebun":
    st.subheader("Ringkasan Kebun")
    if st.session_state.kebun_data.empty:
        st.info("Belum ada data. Pilih menu '🌱 Tambah Blok' terlebih dahulu.")
    else:
        total_pohon = st.session_state.kebun_data['Jumlah Pohon'].sum()
        st.metric(label="Total Pohon Dikelola", value=f"{total_pohon} Batang")
        
        # Fitur Hapus Semua Data untuk reset kebun jika diperlukan
        if st.button("🗑️ Hapus Semua Data Kebun"):
            st.session_state.kebun_data = pd.DataFrame(columns=['Blok', 'Varietas', 'Jenis Pupuk', 'Tanggal Tanam', 'Jumlah Pohon', 'Status Musim'])
            st.session_state.status_tugas = {}
            if os.path.exists(FILE_KEBUN): os.remove(FILE_KEBUN)
            if os.path.exists(FILE_TUGAS): os.remove(FILE_TUGAS)
            st.success("Semua database berhasil dibersihkan!")
            st.rerun()
            
        st.write("---")
        for index, row in st.session_state.kebun_data.iterrows():
            with st.container():
                st.markdown(f"### 📍 Blok: {row['Blok']}")
                st.markdown(f"**Varietas:** Kopi {row['Varietas']} | **Cuaca:** {row['Status Musim']}")
                st.markdown(f"**Sistem Pupuk:** {row['Jenis Pupuk']}")
                st.markdown(f"**Populasi:** {row['Jumlah Pohon']} Pohon | **Tanggal Tanam:** {row['Tanggal Tanam']}")
                st.write("---")

# --- MENU: JADWAL & PERINGATAN ---
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
            if row['Jenis Pupuk'] == "Organik (Kompos/Kohe)":
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
                
            tugas_list += [
                ("🔍 Cek Hama PBKo (Penggerek Buah)", 7),
                ("🔍 Cek Karat Daun Kopi", 14)
            ]
                
            tugas_list.sort(key=lambda x: x)
            
            for nama_tugas, jeda_hari in tugas_list:
                tgl_target = tgl + timedelta(days=jeda_hari)
                tgl_indo = tgl_target.strftime('%d %b %Y')
                key_id = f"{blok_id}_{nama_tugas}_{jeda_hari}"
                
                if key_id not in st.session_state.status_tugas:
                    st.session_state.status_tugas[key_id] = False
                
                with st.container():
                    # Jika tugas belum dikerjakan
                    if not st.session_state.status_tugas[key_id]:
                        st.error(f"🚨 **BELUM DIKERJAKAN!** \n\n **{nama_tugas}** \n\n Batas Waktu: {tgl_indo}")
                        if st.button(f"✅ Selesai: {nama_tugas}", key=f"btn_{key_id}"):
                            st.session_state.status_tugas[key_id] = True
                            # SIMPAN PERMANEN STATUS BARU KE CSV
                            simpan_data_tugas(st.session_state.status_tugas)
                            st.rerun()
                    # Jika tugas sudah dikerjakan
                    else:
                        st.success(f"🎉 **SUDAH SELESAI** \n\n **{nama_tugas}**")
                        if st.button(f"🔄 Batalkan", key=f"reset_{key_id}"):
                            st.session_state.status_tugas[key_id] = False
                            # UPDATE PERMANEN STATUS BARU KE CSV
                            simpan_data_tugas(st.session_state.status_tugas)
                            st.rerun()
                st.write("") 
            st.markdown("---")

# --- MENU: KALKULATOR PUPUK OTOMATIS ---
elif menu == "🧮 Kalkulator Pupuk":
    st.subheader("🧮 Kalkulator Kebutuhan Pupuk Kebun")
    
    if st.session_state.kebun_data.empty:
        st.info("Masukkan data blok kebun terlebih dahulu untuk menghitung pupuk otomatis.")
    else:
        pilihan_blok = st.selectbox("Pilih Blok Kebun:", st.session_state.kebun_data['Blok'].unique())
        
        data_blok_terpilih = st.session_state.kebun_data[st.session_state.kebun_data['Blok'] == pilihan_blok].iloc[0]
        jumlah_pohon = data_blok_terpilih['Jumlah Pohon']
        sistem_pupuk = data_blok_terpilih['Jenis Pupuk']
        
        st.info(f"**Blok Terpilih:** {pilihan_blok} | **Populasi:** {jumlah_pohon} Pohon")
        st.write("### Estimasi Kebutuhan Sekali Pemupukan:")
        
        if "Organik" in sistem_pupuk:
            dosis_per_pohon = 5.0 
            total_kebutuhan = jumlah_pohon * dosis_per_pohon
            st.metric(label="Total Pupuk Kompos/Kohe yang Diperlukan", value=f"{total_kebutuhan:,.1f} Kg")
        else:
            dosis_per_pohon_gram = 100 
            total_kebutuhan_kg = (jumlah_pohon * dosis_per_pohon_gram) / 1000
            st.metric(label="Total Pupuk NPK Kimia yang Diperlukan", value=f"{total_kebutuhan_kg:,.1f} Kg")
            
        st.warning("⚠️ Catatan: Data kalkulator ini berbasis real-time dari data blok yang Anda kunci secara aman.")
