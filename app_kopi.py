import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Konfigurasi Halaman
st.set_page_config(page_title="KopiPlan - Jadwal Kebun Kopi", layout="wide")
st.title("☕ KopiPlan: Sistem Penjadwalan Kebun Kopi")

# Inisialisasi Data State (Simulasi Database)
if 'kebun_data' not in st.session_state:
    st.session_state.kebun_data = pd.DataFrame(columns=['Blok', 'Varietas', 'Tanggal Tanam', 'Jumlah Pohon'])

# --- SIDEBAR: INPUT DATA KEBUN ---
st.sidebar.header("🌱 Tambah Blok Kebun Baru")
with st.sidebar.form("form_kebun"):
    nama_blok = st.text_input("Nama Blok (Contoh: Blok A / Lereng Utara)")
    varietas = st.selectbox("Varietas Kopi", ["Arabika", "Robusta", "Liberika"])
    tgl_tanam = st.date_input("Tanggal Tanam", datetime.now())
    jml_pohon = st.number_input("Jumlah Pohon", min_value=1, value=100)
    submit_button = st.form_submit_button(label="Simpan Data")

if submit_button and nama_blok:
    new_data = pd.DataFrame([[nama_blok, varietas, tgl_tanam, jml_pohon]], 
                            columns=['Blok', 'Varietas', 'Tanggal Tanam', 'Jumlah Pohon'])
    st.session_state.kebun_data = pd.concat([st.session_state.kebun_data, new_data], ignore_index=True)
    st.sidebar.success(f"Blok {nama_blok} berhasil ditambahkan!")

# --- HALAMAN UTAMA ---
if st.session_state.kebun_data.empty:
    st.info("Silakan tambah data blok kebun Anda di sidebar terlebih dahulu.")
else:
    # Tab Menu
    tab1, tab2 = st.tabs(["📊 Dashboard & Data Kebun", "📅 Jadwal Pemeliharaan"])

    with tab1:
        st.subheader("Data Blok Kebun Saat Ini")
        st.dataframe(st.session_state.kebun_data, use_container_width=True)
        
        # Metrik Singkat
        total_pohon = st.session_state.kebun_data['Jumlah Pohon'].sum()
        st.metric(label="Total Pohon Kopi Dikelola", value=f"{total_pohon} Pohon")

    with tab2:
        st.subheader("Jadwal Aktivitas Kebun Otomatis")
        st.write("Jadwal di bawah ini dibuat otomatis berdasarkan tanggal tanam:")

        jadwal_list = []
        for index, row in st.session_state.kebun_data.iterrows():
            tgl = pd.to_datetime(row['Tanggal Tanam'])
            
            # Logika Aturan Jadwal Budidaya Kopi Singkat
            jadwal_list.append({
                "Blok": row['Blok'],
                "Aktivitas": "Pemupukan Organik Awal",
                "Tanggal Target": (tgl + timedelta(days=30)).strftime('%Y-%m-%d'),
                "Status": "Rencana"
            })
            jadwal_list.append({
                "Blok": row['Blok'],
                "Aktivitas": "Pemangkasan Wiwilan (Tunas Air)",
                "Tanggal Target": (tgl + timedelta(days=90)).strftime('%Y-%m-%d'),
                "Status": "Rencana"
            })
            jadwal_list.append({
                "Blok": row['Blok'],
                "Aktivitas": "Pemupukan Kimia (NPK) Tahap 1",
                "Tanggal Target": (tgl + timedelta(days=180)).strftime('%Y-%m-%d'),
                "Status": "Rencana"
            })
            jadwal_list.append({
                "Blok": row['Blok'],
                "Aktivitas": "Estimasi Panen Perdana (Belajar Berbuah)",
                "Tanggal Target": (tgl + timedelta(days=730)).strftime('%Y-%m-%d'),
                "Status": "Rencana"
            })

        df_jadwal = pd.DataFrame(jadwal_list)
        st.dataframe(df_jadwal, use_container_width=True)

        # Fitur Cetak / Selesai sederhana
        st.caption("💡 Tip: Lakukan pemeliharaan rutin secara berkala sesuai tanggal target untuk hasil ceri kopi yang optimal.")
