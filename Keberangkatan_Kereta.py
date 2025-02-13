import streamlit as st
import matplotlib.pyplot as plt
import datetime

# Fungsi Konversi Waktu
def konversi_ke_menit(waktu):
    try:
        jam, menit = map(int, waktu.split('.'))
        return jam * 60 + menit
    except:
        return None

# Fungsi untuk Menyusun Jadwal Kereta
def jadwal_kereta(waktu):
    waktu.sort(key=lambda x: x[1])
    hasil = []
    waktu_terakhir = 0
    for kereta in waktu:
        if kereta[0] >= waktu_terakhir:
            hasil.append(kereta)
            waktu_terakhir = kereta[1]
    return hasil

# Sidebar Layout
st.sidebar.image("Img/unikom.png", width=150)
st.sidebar.image("Img/kelompok3.png", width=250)
selected_date = st.sidebar.date_input("Tanggal", datetime.date.today())

# Judul Aplikasi
st.title("🚆 Jadwal Keberangkatan Kereta")

# Input jumlah kereta
n = st.number_input("Masukkan jumlah kereta:", min_value=1, step=1, value=1)

# Pilihan rute
rute_options = ['A', 'B', 'C']

# Input Waktu Keberangkatan, Kedatangan, dan Rute
waktu = []
warning_rute = False
for i in range(n):
    st.subheader(f"Kereta {i + 1}")
    col1, col2, col3 = st.columns(3)
    with col1:
        mulai_jam = st.text_input(f"Jam Berangkat Kereta {i + 1} (HH.MM)", key=f"mulai_{i}")
    with col2:
        selesai_jam = st.text_input(f"Jam Sampai Kereta {i + 1} (HH.MM)", key=f"selesai_{i}")
    with col3:
        rute = st.selectbox(f"Rute Kereta {i + 1}", rute_options, key=f"rute_{i}")
    
    if mulai_jam and selesai_jam:
        start = konversi_ke_menit(mulai_jam)
        end = konversi_ke_menit(selesai_jam)
        if start is not None and end is not None:
            waktu.append((start, end, rute, i + 1))
        else:
            st.error(f"Format waktu salah untuk Kereta {i + 1}! Gunakan format HH.MM")

if st.button("🚄 Tampilkan Jadwal"): 
    if waktu:
        jadwal = jadwal_kereta(waktu)
        st.subheader("📅 Jadwal Kereta yang Dipilih:")
        for i, kereta in enumerate(jadwal):
            st.write(f"**Kereta {kereta[3]} (Rute {kereta[2]})**: Berangkat **{kereta[0]} menit**, Tiba **{kereta[1]} menit**")
        
        tercepat = min(jadwal, key=lambda x: x[1] - x[0])
        st.success(f"🔥 Kereta tercepat adalah **Kereta {tercepat[3]} (Rute {tercepat[2]})**: Berangkat **{tercepat[0]} menit**, Tiba **{tercepat[1]} menit**, dengan durasi **{tercepat[1] - tercepat[0]} menit**.")
        
        # Diagram Titik
        st.subheader("📊 Diagram Titik Jadwal Kereta")
        labels = [f"Kereta {kereta[3]} (Rute {kereta[2]})" for kereta in waktu]
        keberangkatan = [kereta[0] for kereta in waktu]
        kedatangan = [kereta[1] for kereta in waktu]
        
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.scatter(labels, keberangkatan, color='blue', label="Keberangkatan", s=100)
        ax.scatter(labels, kedatangan, color='red', label="Kedatangan", s=100)
        
        for i in range(len(labels)):
            ax.vlines(x=labels[i], ymin=keberangkatan[i], ymax=kedatangan[i], colors='black', linestyles='dotted')
        
        y_min = min(keberangkatan) - 10  # Tambahkan margin kecil agar grafik terlihat rapi
        y_max = max(kedatangan) + 10  # Tambahkan margin kecil
        ax.set_ylim(y_min, y_max)
        ax.set_ylabel("Waktu (Menit)")
        ax.set_title("Jadwal Keberangkatan dan Kedatangan Kereta")
        ax.legend()
        ax.grid(True)

        st.pyplot(fig)

# Footer
st.markdown("""
    <style>
        .footer {
            position: fixed;
            bottom: 0;
            width: 100%;
            background-color: #0E1117;
            color: white; 
            padding: 10px;
            font-size: 14px;
        }
    </style>
    <div class="footer">
        &copy; 2025 Kelompok 3 - Universitas Komputer Indonesia | Dibuat oleh Kelompok 3
    </div>
""", unsafe_allow_html=True)
