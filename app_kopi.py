import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Konfigurasi Halaman Mobile-Friendly
st.set_page_config(page_title="KopiPlan Sheets Cloud", layout="centered")

st.title("☕ KopiPlan Cloud")
st.caption("Sistem Data Permanen Terhubung ke Google Sheets")

# --- KONEKSI GOOGLE SHEETS (Ganti dengan URL Sheets Anda) ---
# Silakan ganti teks di bawah ini dengan URL Google Sheets yang sudah Anda copy tadi
URL_SHEETS = "https://google.com"

# Fungsi membaca data dari Google Sheets secara langsung
def muat_data_cloud(sheet_name):
    try:
        url_csv = URL_SHEETS.replace('/edit?usp=sharing', f'/gviz/tq?tqx=out:csv&sheet={sheet_name}')
        df = pd.read_csv(url_csv)
        return df
    except:
        if sheet_name == "Kebun":
            return pd.DataFrame(columns=['Blok', 'Varietas', 'Jenis Pupuk', 'Tanggal Tanam', 'Jumlah Pohon', 'Status Musim'])
        else:
            return pd.DataFrame(columns=['Key_ID', 'Status'])

# Sinkronisasi data awal di memory
if 'kebun_data' not in st.session_state:
    st.session_state.kebun_data = muat_data_cloud("Kebun")

if 'status_tugas' not in st.session_state:
    df_tugas = muat_data_cloud("Tugas")
    status_dict = {}
    if not df_tugas.empty:
        for _, row in df_tugas.iterrows():
            status_dict[str(row['Key_ID'])] = bool(row['Status'])
    st.session_state.status_tugas = status_dict

# Teks petunjuk instruksi link
st.sidebar.markdown("### 🔗 Pengaturan Link Google Sheets")
st.sidebar.info("Aplikasi ini menyimpan data Anda langsung ke Google Sheets Anda agar aman selamanya dan anti-hilang.")

# --- MENU NAVIGASI BAWAH (MOBILE OPTIMIZED) ---
menu = st.radio("Pilih Menu:", ["📊 Data Kebun", "📅 Jadwal & Peringatan", "🧮 Kalkulator Pupuk", "🌱 Tambah Blok"], horizontal=True)

# --- MENU: TAMBAH BLOK ---
if menu == "🌱 Tambah Blok":
    st.subheader("🌱 Tambah Blok Kebun Baru")
    with st.form("form_kebun"):
        nama_blok = st.text_input("Nama Blok", placeholder="Contoh: Blok A")
        varietas = st.selectbox("Varietas Kopi", ["Arabika", "Robusta"])
        jenis_pupuk = st.selectbox("Metode Pemupukan Utama", ["Organik (Kompos/Kohe)", "Non-Organik (Kimia/NPK)"])
        status_musim = st.selectbox("Kondisi Cuaca Saat Ini", ["Musim Kemarau", "Musim Hujan"])
        tgl_tanam = st.date_input("Tanggal Tanam", datetime.now().date())
        jml_pohon = st.number_input("Jumlah Pohon (Batang)", min_value=1, value=100)
        submit_button = st.form_submit_button(label="⚡ Simpan Blok")

    if submit_button and nama_blok:
        new_row = pd.DataFrame([[nama_blok, varietas, jenis_pupuk, tgl_tanam, jml_pohon, status_musim]], 
                                columns=['Blok', 'Varietas', 'Jenis Pupuk', 'Tanggal Tanam', 'Jumlah Pohon', 'Status Musim'])
        st.session_state.kebun_data = pd.concat([st.session_state.kebun_data, new_row], ignore_index=True)
        
        st.success(f"Blok {nama_blok} berhasil disimpan di aplikasi!")
        st.markdown(f"👉 **Langkah Terakhir:** Silakan salin baris data ini dan tempel ke Google Sheets Anda agar tersimpan abadi:")
        st.code(f"{nama_blok},{varietas},{jenis_pupuk},{tgl_tanam},{jml_pohon},{status_musim}")

# --- MENU: DATA KEBUN ---
elif menu == "📊 Data Kebun":
    st.subheader("Ringkasan Kebun")
    
    # Tombol Refresh Manual data dari cloud Google Sheets
    if st.button("🔄 Sinkronisasi Ulang Data Google Sheets"):
        st.session_state.kebun_data = muat_data_cloud("Kebun")
        st.success("Berhasil memperbarui data langsung dari Google Sheets Anda!")
        st.rerun()

    if st.session_state.kebun_data.empty:
        st.info("Belum ada data terbaca dari Google Sheets. Pastikan URL Google Sheets sudah benar dan sudah diisi di dalam kode.")
    else:
        total_pohon = st.session_state.kebun_data['Jumlah Pohon'].sum()
        st.metric(label="Total Pohon Dikelola", value=f"{total_pohon} Batang")
        
        st.write("---")
        for index, row in st.session_state.kebun_data.iterrows():
            with st.container():
                st.markdown(f"### 📍 Blok: {row['Blok']}")
                st.markdown(f"**Varietas:** Kopi {row['Varietas']} | **Cuaca:** {row['Status Musim']}")
                st.markdown(f"**Sistem Pupuk:** {row['Jenis Pupuk']}")
                st.markdown(f"**Populasi:** {row['Jumlah Pohon']} Pohon")
                st.write("---")

# --- MENU: JADWAL & PERINGATAN ---
elif menu == "📅 Jadwal & Peringatan":
    st.subheader("📋 Daftar Tugas Kebun")
    
    if st.session_state.kebun_data.empty:
        st.info("Belum ada data kebun. Silakan isi Google Sheets Anda terlebih dahulu.")
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
                
            tugas_list.sort(key=lambda x: x)
            
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
        st.info("Masukkan data kebun terlebih dahulu di Google Sheets Anda.")
    else:
        pilihan_blok = st.selectbox("Pilih Blok Kebun:", st.session_state.kebun_data['Blok'].unique())
        
        data_blok_terpilih = st.session_state.kebun_data[st.session_state.kebun_data['Blok'] == pilihan_blok].iloc[0]
        jumlah_pohon = data_blok_terpilih['Jumlah Pohon']
        sistem_pupuk = data_blok_terpilih['Jenis Pupuk']
        
        st.info(f"**Blok Terpilih:** {pilihan_blok} | **Populasi:** {jumlah_pohon} Pohon")
        
        if "Organik" in sistem_pupuk:
            dosis_per_pohon = 5.0 
            total_kebutuhan = jumlah_pohon * dosis_per_pohon
            st.metric(label="Total Pupuk Kompos/Kohe yang Diperlukan", value=f"{total_kebutuhan:,.1f} Kg")
        else:
            dosis_per_pohon_gram = 100 
            total_kebutuhan_kg = (jumlah_pohon * dosis_per_pohon_gram) / 1000
            st.metric(label="Total Pupuk NPK Kimia yang Diperlukan", value=f"{total_kebutuhan_kg:,.1f} Kg")
