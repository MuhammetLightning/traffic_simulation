import streamlit as st

st.set_page_config(
    page_title="Hakkında - Trafik Simülasyonu",
    page_icon="ℹ️",
    layout="wide"
)

st.title("ℹ️ Hakkında")

st.markdown("""
## Trafik Akışı Simülasyonu Nedir?

Bu uygulama, farklı yol türleri ve araç tipleri için trafik akışını simüle eden bir web uygulamasıdır. 
Simülasyon, gerçek dünya trafik koşullarını modelleyerek, trafik yoğunluğunu ve akışını analiz eder.

### 🚗 Yol Tipleri

- **Şehir İçi**
  - 2 şeritli yol
  - Trafik ışığı: 60 saniye kırmızı, 40 saniye yeşil
  - Temel varış oranı: 0.3 araç/saniye

- **Otoyol**
  - 3 şeritli yol
  - Trafik ışığı: 30 saniye kırmızı, 90 saniye yeşil
  - Temel varış oranı: 0.2 araç/saniye

### 🚌 Araç Tipleri

- **Otomobil**
  - Maksimum hız: 70 km/s
  - Araç uzunluğu: 4.5 metre

- **Otobüs**
  - Maksimum hız: 50 km/s
  - Araç uzunluğu: 12 metre

- **Kamyon**
  - Maksimum hız: 40 km/s
  - Araç uzunluğu: 16 metre
""")

st.divider()

st.subheader("📊 Teknik Detaylar")
st.markdown("""
- Python tabanlı simülasyon motoru
- Poisson dağılımı kullanılarak rastgele araç varışları
- Araç tipine ve yol türüne göre özelleştirilmiş varış oranları
- Hız limitine bağlı olarak dinamik geçiş oranları
""") 