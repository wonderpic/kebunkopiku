import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Konfigurasi Tampilan Aplikasi HP
st.set_page_config(page_title="KopiPlan Fix", layout="centered")
st.title("☕ KopiPlan Pro")
st.caption("Aplikasi Penjadwalan & Perawatan Kebun Kopi")

# --- DATA KEBUN KOPI ANDA (Ditulis Langsung di Sini agar Aman & Tidak Hilang) ---
# Silakan ubah atau tambah data di dalam tanda kurung siku jika diperlukan
raw_data = {
    'Blok': ["Blok A", "Blok B"],
    'Varietas': ["Arabika", "Robusta"],
    'Jenis_Pupuk': ["Organik (Kompos/Kohe)", "Non-Organik (Kimia/NPK)"],
    'Tanggal_Tanam': ["2026-01-01", "2026-02-15"],
    'Jumlah_Pohon': [150, 250],
    'Status_Musim': ["Musim Kemarau", "Musim Hujan"]
}

# Mengunci data menjadi tabel resmi
st.session_state.kebun_data = pd.DataFrame(raw_data)

# --- NAVIGASI MENU UTAMA ---
menu = st.radio("Pilih Menu:", ["📊 Data Kebun", "📅 Jadwal & Peringatan", "🧮 Kalkulator Pupuk"], horizontal=True)

# 1. TAMPILAN DATA KEBUN
if menu == "📊 Data Kebun":
    st.subheader("Ringkasan Kebun Saat Ini")
    total_pohon = st.session_state.kebun_data['Jumlah_Pohon'].sum()
    st.metric(label="Total Pohon Kopi Dikelola", value=f"{total_pohon} Batang")
    st.write("---")
    
    for idx, row in st.session_state.kebun_data.iterrows():
        with st.container():
            st.markdown(f"### 📍 Blok: {row['Blok']}")
            st.markdown(f"**Varietas:** Kopi {row['Varietas']} | **Cuaca:** {row['Status_Musim']}")
            st.markdown(f"**Sistem Pupuk:** {row['Jenis_Pupuk']}")
            st.markdown(f"**Populasi:** {row['Jumlah_Pohon']} Pohon | **Tanggal Tanam:** {row['Tanggal_Tanam']}")
            st.write("---")

# 2. TAMPILAN JADWAL & PERINGATAN PINTAR
elif menu == "📅 Jadwal & Peringatan":
    st.subheader("📋 Daftar Tugas Kebun")
    
    for idx, row in st.session_state.kebun_data.iterrows():
        blok_id = row['Blok']
        tgl = pd.to_datetime(row['Tanggal_Tanam'])
        musim = row['Status_Musim']
        
        st.markdown(f"### 📍 Blok Kerja: **{blok_id}** ({row['Varietas']})")
        
        # Logika Tugas Otomatis
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
            
        tugas_list.sort(key=lambda x: x[1])
        
        # Memunculkan tanda bahaya merah permanen sebagai pengingat di kebun
        for nama_tugas, jeda_hari in tugas_list:
            tgl_target = tgl + timedelta(days=jeda_hari)
            tgl_indo = tgl_target.strftime('%d %b %Y')
            st.error(f"🚨 **BELUM SELESAI!** \n\n **{nama_tugas}** \n\n Batas Tanggal: {tgl_indo}")
        st.markdown("---")

# 3. TAMPILAN KALKULATOR PUPUK OTOMATIS
elif menu == "🧮 Kalkulator Pupuk":
    st.subheader("🧮 Kalkulator Kebutuhan Pupuk Kebun")
    pilihan_blok = st.selectbox("Pilih Blok Kebun:", st.session_state.kebun_data['Blok'].unique())
    
    # Memfilter data secara aman
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
