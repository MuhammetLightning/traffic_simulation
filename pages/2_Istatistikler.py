import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="İstatistikler - Trafik Simülasyonu",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Trafik İstatistikleri")

# Örnek veriler
yol_tipleri = {
    "Şehir İçi": {
        "ortalama_kuyruk": [0.76, 1.2, 0.9],
        "maksimum_kuyruk": [10, 15, 12],
        "trafik_akisi": [11.38, 8.5, 10.2]
    },
    "Otoyol": {
        "ortalama_kuyruk": [0.23, 0.5, 0.35],
        "maksimum_kuyruk": [7, 9, 8],
        "trafik_akisi": [3.48, 4.2, 3.8]
    }
}

# Seçim kutuları
col1, col2 = st.columns(2)
with col1:
    yol_tipi = st.selectbox("Yol Tipi", ["Şehir İçi", "Otoyol"])
with col2:
    veri_tipi = st.selectbox("Veri Tipi", ["Ortalama Kuyruk", "Maksimum Kuyruk", "Trafik Akışı"])

# Grafik oluşturma
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(10, 6))

data = None
if veri_tipi == "Ortalama Kuyruk":
    data = yol_tipleri[yol_tipi]["ortalama_kuyruk"]
    title = f"{yol_tipi} - Ortalama Kuyruk Uzunluğu"
    ylabel = "Araç Sayısı"
elif veri_tipi == "Maksimum Kuyruk":
    data = yol_tipleri[yol_tipi]["maksimum_kuyruk"]
    title = f"{yol_tipi} - Maksimum Kuyruk Uzunluğu"
    ylabel = "Araç Sayısı"
else:
    data = yol_tipleri[yol_tipi]["trafik_akisi"]
    title = f"{yol_tipi} - Trafik Akış Hızı"
    ylabel = "Araç/Dakika"

ax.plot(data, color='#FF4B4B', linewidth=2, marker='o')
ax.set_title(title, color='white', pad=20)
ax.set_xlabel('Zaman Dilimi', color='white')
ax.set_ylabel(ylabel, color='white')
ax.grid(True, alpha=0.2)

# Arka plan ve eksen renkleri
fig.patch.set_facecolor('#0E1117')
ax.set_facecolor('#262730')
ax.tick_params(colors='white')
for spine in ax.spines.values():
    spine.set_color('white')

st.pyplot(fig)

# İstatistiksel bilgiler
st.subheader("📈 İstatistiksel Özet")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Ortalama",
        f"{np.mean(data):.2f}",
        delta=f"{np.mean(data) - np.median(data):.2f}"
    )
with col2:
    st.metric(
        "Medyan",
        f"{np.median(data):.2f}"
    )
with col3:
    st.metric(
        "Standart Sapma",
        f"{np.std(data):.2f}"
    ) 