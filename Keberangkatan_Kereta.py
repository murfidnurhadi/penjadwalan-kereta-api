import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime

# Fungsi untuk membaca dataset kereta
@st.cache_data
def load_data():
    return pd.read_csv("kereta_jadwal.csv")

# Load dataset
df = load_data()

# Sidebar untuk memilih stasiun asal
st.sidebar.image("Img/unikom.png", width=150)
st.sidebar.image("Img/kelompok3.png", width=250)

st.sidebar.subheader("🔍 Filter Data Kereta")
stasiun_asal = st.sidebar.selectbox("Pilih Stasiun Asal", df["Stasiun_Asal"].unique())

# Filter data berdasarkan stasiun asal yang dipilih
df_filtered = df[df["Stasiun_Asal"] == stasiun_asal]

# Tampilkan tabel data kereta yang sesuai
st.subheader(f"🚆 Jadwal Keberangkatan dari {stasiun_asal}")
st.dataframe(df_filtered)

# Tambahkan visualisasi jadwal keberangkatan
fig, ax = plt.subplots(figsize=(8, 5))
ax.barh(df_filtered["Kereta"], pd.to_datetime(df_filtered["Keberangkatan"], format='%H.%M').dt.hour, color='blue')
ax.set_xlabel("Jam Keberangkatan")
ax.set_ylabel("Kereta")
ax.set_title("Jadwal Keberangkatan")
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
