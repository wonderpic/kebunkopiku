import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Konfigurasi Tampilan Aplikasi HP
st.set_page_config(page_title="KopiPlan Pro Fix", layout="centered")
st.title("☕ KopiPlan Pro")
st.caption("Aplikasi Penjadwalan, Perawatan & Manajemen Kebun Kopi")

# --- SISTEM PENYIMPANAN DATA MANDIRI (ANTI-ERROR) ---
# Membuat data awal standar jika memori aplikasi masih kosong
if 'kebun_data' not in st.session_state:
    st.session_state.kebun_data = pd.DataFrame([
        {"Blok": "Blok A", "Varietas": "Arabika", "Jenis_Pupuk": "Organik (Kompos/Kohe)", "Tanggal_Tanam": datetime(2025, 1, 1).date(), "Jumlah_Pohon": 150, "Status_Musim": "Musim Kemarau"},
        {"Blok": "Blok B", "Varietas": "Robusta", "Jenis_Pupuk": "Non-Organik (Kimia/NPK)", "Tanggal_Tanam": datetime(2025, 6, 1).date(), "Jumlah_Pohon": 200, "Status_Musim": "Musim Hujan"}
    ])

# --- NAVIGASI MENU UTAMA (MOBILE FRIENDLY) ---
menu = st.radio("Pilih Menu:", ["📊 Data Kebun", "📅 Jadwal & Peringatan", "🧮 Kalkulator Pupuk", "🌱 Tambah Blok"], horizontal=True)

# 1. MENU: TAMBAH BLOK
if menu == "🌱 Tambah Blok":
    st.subheader("🌱 Tambah Blok Kebun Baru")
    with st.form("form_kebun_baru"):
        nama_blok = st.text_input("Nama Blok Baru", placeholder="Contoh: Blok C / Lereng Barat")
        varietas = st.selectbox("Varietas Kopi", ["Arabika", "Robusta"])
        jenis_pupuk = st.selectbox("Metode Pemupukan Utama", ["Organik (Kompos/Kohe)", "Non-Organik (Kimia/NPK)"])
        status_musim = st.selectbox("Kondisi Cuaca Saat Ini", ["Musim Kemarau", "Musim Hujan"])
        tgl_tanam = st.date_input("Tanggal Tanam", datetime.now().date())
        jml_pohon = st.number_input("Jumlah Pohon (Batang)", min_value=1, value=100)
        submit_button = st.form_submit_button(label="⚡ Simpan Blok Baru")

    if submit_button and nama_blok:
        # Validasi agar tidak ada nama blok yang kembar
        if nama_blok in st.session_state.kebun_data['Blok'].values:
            st.error(f"Nama Blok '{nama_blok}' sudah terdaftar! Gunakan nama lain.")
        else:
            # Memasukkan data baru ke dalam tabel memori
            new_row = pd.DataFrame([[nama_blok, varietas, jenis_pupuk, tgl_tanam, jml_pohon, status_musim]], 
                                    columns=['Blok', 'Varietas', 'Jenis_Pupuk', 'Tanggal_Tanam', 'Jumlah_Pohon', 'Status_Musim'])
            st.session_state.kebun_data = pd.concat([st.session_state.kebun_data, new_row], ignore_index=True)
            st.success(f"🎉 Sukses! {nama_blok} berhasil ditambahkan ke sistem.")
            st.rerun()

# 2. MENU: TAMPILAN DATA KEBUN (DENGAN FITUR HAPUS)
elif menu == "📊 Data Kebun":
    st.subheader("Ringkasan Kebun")
    
    if st.session_state.kebun_data.empty:
        st.info("Belum ada data kebun dikelola. Silakan tambah blok terlebih dahulu.")
    else:
        total_pohon = st.session_state.kebun_data['Jumlah_Pohon'].sum()
        st.metric(label="Total Semua Pohon Kopi Dikelola", value=f"{total_pohon} Batang")
        st.write("---")
        
        # Menampilkan data per blok beserta tombol hapus masing-masing
        for idx, row in st.session_state.kebun_data.iterrows():
            with st.container():
                st.markdown(f"### 📍 Blok: {row['Blok']}")
                st.markdown(f"**Varietas:** Kopi {row['Varietas']} | **Cuaca:** {row['Status_Musim']}")
                st.markdown(f"**Sistem Pupuk:** {row['Jenis_Pupuk']}")
                st.markdown(f"**Populasi:** {row['Jumlah_Pohon']} Pohon | **Tanggal Tanam:** {row['Tanggal_Tanam']}")
                
                # FITUR BARU: Tombol hapus spesifik per blok kebun yang sudah tidak ada
                if st.button(f"🗑️ Hapus {row['Blok']}", key=f"hapus_{row['Blok']}_{idx}"):
                    # Menghapus baris berdasarkan index data
                    st.session_state.kebun_data = st.session_state.kebun_data.drop(idx).reset_index(drop=True)
                    st.success(f"Blok {row['Blok']} telah berhasil dihapus dari sistem!")
                    st.rerun() # Muat ulang halaman agar data langsung hilang dari layar
                st.write("---")

# 3. MENU: TAMPILAN JADWAL & PERINGATAN PINTAR
elif menu == "📅 Jadwal & Peringatan":
    st.subheader("📋 Daftar Tugas Pemeliharaan")
    
    if st.session_state.kebun_data.empty:
        st.info("Belum ada jadwal. Tambahkan data kebun terlebih dahulu.")
    else:
        for idx, row in st.session_state.kebun_data.iterrows():
            blok_id = row['Blok']
            tgl = pd.to_datetime(row['Tanggal_Tanam'])
            musim = row['Status_Musim']
            
            st.markdown(f"### 📍 Blok Kerja: **{blok_id}** ({row['Varietas']})")
            
            # Logika Penjadwalan Otomatis Berdasarkan Aturan Kopi
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
            
            # Tampilan alarm peringatan merah di lapangan
            for nama_tugas, jeda_hari in tugas_list:
                tgl_target = tgl + timedelta(days=jeda_hari)
                tgl_indo = tgl_target.strftime('%d %b %Y')
                st.error(f"🚨 **BELUM SELESAI!** \n\n **{nama_tugas}** \n\n Batas Tanggal: {tgl_indo}")
            st.markdown("---")

# 4. MENU: TAMPILAN KALKULATOR PUPUK OTOMATIS
elif menu == "🧮 Kalkulator Pupuk":
    st.subheader("🧮 Kalkulator Kebutuhan Pupuk Kebun")
    
    if st.session_state.kebun_data.empty:
        st.info("Masukkan data kebun terlebih dahulu untuk mengaktifkan kalkulator.")
    else:
        pilihan_blok = st.selectbox("Pilih Blok Kebun:", st.session_state.kebun_data['Blok'].unique())
        
        df_filter = st.session_state.kebun_data[st.session_state.kebun_data['Blok'] == pilihan_blok]
        
        if not df_filter.empty:
            jumlah_pohon = int(df_filter.iloc[0]['Jumlah_Pohon'])
            sistem_pupuk = str(df_filter.iloc[0]['Jenis_Pupuk'])
            
            st.info(f"**Blok Terpilih:** {pilihan_blok} | **Populasi:** {jumlah_pohon} Pohon")
            
            if "Organik" in sistem_pupuk:
                total_kebutuhan = jumlah_pohon * 5.0
                st.metric(label="Total Pupuk Kompos/Kohe yang Diperlukan", value=f"{total_kebutuhan:,.1f} Kg")
                st.caption("💡 Dosis standar: 5 Kg pupuk organik per pohon.")
            else:
                total_kebutuhan_kg = (jumlah_pohon * 100) / 1000
                st.metric(label="Total Pupuk NPK Kimia yang Diperlukan", value=f"{total_kebutuhan_kg:,.1f} Kg")
                st.caption("💡 Dosis standar: 100 Gram pupuk NPK per pohon.")
