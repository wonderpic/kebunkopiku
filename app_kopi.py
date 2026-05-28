import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="KopiPlan Pro", layout="centered")
st.title("☕ KopiPlan Pro")
st.caption("Aplikasi Penjadwalan Kebun Kopi")

# --- SISTEM DATABASE SECRETS YANG AMAN ---
if 'kebun_data' not in st.session_state:
    if "KEBUN_DATA" in st.secrets:
        # Mengubah data dari secrets menjadi tabel dengan paksaan nama kolom yang benar
        raw_data = st.secrets["KEBUN_DATA"]
        st.session_state.kebun_data = pd.DataFrame({
            'Blok': raw_data.get('Blok', []),
            'Varietas': raw_data.get('Varietas', []),
            'Jenis_Pupuk': raw_data.get('Jenis_Pupuk', []),
            'Tanggal_Tanam': raw_data.get('Tanggal_Tanam', []),
            'Jumlah_Pohon': raw_data.get('Jumlah_Pohon', []),
            'Status_Musim': raw_data.get('Status_Musim', [])
        })
    else:
        st.session_state.kebun_data = pd.DataFrame(columns=['Blok', 'Varietas', 'Jenis_Pupuk', 'Tanggal Tanam', 'Jumlah Pohon', 'Status Musim'])

# --- NAVIGASI MENU ---
menu = st.radio("Pilih Menu:", ["📊 Data Kebun", "📅 Jadwal & Peringatan", "🧮 Kalkulator Pupuk"], horizontal=True)

if menu == "📊 Data Kebun":
    st.subheader("Ringkasan Kebun")
    if st.session_state.kebun_data.empty:
        st.info("Belum ada data kebun. Silakan isi Secrets di dashboard Streamlit Anda.")
    else:
        for idx, row in st.session_state.kebun_data.iterrows():
            st.markdown(f"### 📍 Blok: {row['Blok']}")
            st.markdown(f"**Varietas:** Kopi {row['Varietas']} | **Sistem Pupuk:** {row['Jenis_Pupuk']}")
            st.markdown(f"**Populasi:** {row['Jumlah Pohon']} Pohon | **Cuaca:** {row['Status_Musim']}")
            st.write("---")

elif menu == "📅 Jadwal & Peringatan":
    st.subheader("📋 Daftar Tugas Kebun")
    if st.session_state.kebun_data.empty:
        st.info("Belum ada data kebun.")
    else:
        for idx, row in st.session_state.kebun_data.iterrows():
            st.markdown(f"### 📍 Target Kerja: {row['Blok']} ({row['Varietas']})")
            st.error(f"🚨 **BELUM DIKERJAKAN:** Jadwal Penyiraman & Pengecekan Hama di {row['Blok']}")
            st.write("---")

elif menu == "🧮 Kalkulator Pupuk":
    st.subheader("🧮 Kalkulator Kebutuhan Pupuk")
    if st.session_state.kebun_data.empty:
        st.info("Belum ada data kebun.")
    else:
        pilihan_blok = st.selectbox("Pilih Blok:", st.session_state.kebun_data['Blok'].unique())
        df_filter = st.session_state.kebun_data[st.session_state.kebun_data['Blok'] == pilihan_blok]
        
        if not df_filter.empty:
            pohon = df_filter.iloc[0]['Jumlah Pohon']
            pupuk = df_filter.iloc[0]['Jenis_Pupuk']
            
            if "Organik" in str(pupuk):
                st.metric(label="Total Pupuk Kompos Dibutuhkan", value=f"{pohon * 5} Kg")
            else:
                st.metric(label="Total Pupuk NPK Kimia Dibutuhkan", value=f"{(pohon * 100) / 1000} Kg")
