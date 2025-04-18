import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io

st.set_page_config(
    page_title="Ana Sayfa - Trafik Simülasyonu",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS stilleri
st.markdown("""
    <style>
    .stSlider > div > div > div > div {
        background-color: #FF4B4B;
    }
    .stButton > button {
        background-color: #FF4B4B;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 2rem;
        border: none;
    }
    .stButton > button:hover {
        background-color: #FF6B6B;
    }
    .stSelectbox {
        background-color: #262730;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚗 Trafik Akışı Simülasyonu")

def simulate_traffic(road_type, vehicle_type, speed_limit):
    # Simülasyon parametreleri
    time_steps = 100
    queue_lengths = []
    
    # Simülasyon parametreleri
    if road_type == "Şehir İçi":
        base_flow = 0.7
    elif road_type == "Otoyol":
        base_flow = 0.9
    else:
        base_flow = 0.8
        
    if vehicle_type == "Otomobil":
        vehicle_factor = 1.0
    elif vehicle_type == "Kamyon":
        vehicle_factor = 0.8
    else:
        vehicle_factor = 1.2
        
    speed_factor = speed_limit / 60.0
    
    # Simülasyon
    current_queue = 0
    for t in range(time_steps):
        # Rastgele trafik akışı
        flow_rate = base_flow * vehicle_factor * speed_factor
        arrivals = np.random.poisson(flow_rate)
        departures = np.random.poisson(flow_rate * 0.9)
        
        # Kuyruk uzunluğunu güncelle
        current_queue = max(0, current_queue + arrivals - departures)
        queue_lengths.append(current_queue)
    
    return queue_lengths

def plot_simulation(queue_lengths):
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(queue_lengths, color='#FF4B4B', linewidth=2)
    ax.set_xlabel('Zaman (saniye)', color='white')
    ax.set_ylabel('Kuyruk Uzunluğu (araç)', color='white')
    ax.set_title('Trafik Akışı Simülasyonu Sonuçları', color='white', pad=20)
    ax.grid(True, alpha=0.2)
    
    # Arka plan rengini ayarla
    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#262730')
    
    # Eksenlerin rengini ayarla
    ax.tick_params(colors='white')
    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color('white')
    ax.spines['right'].set_color('white')
    ax.spines['left'].set_color('white')
    
    return fig

# Yan yana yerleşim için kolonlar
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    road_type = st.selectbox(
        "Yol Türü",
        ["Şehir İçi", "Otoyol", "Ara Yol"],
        index=0
    )

with col2:
    vehicle_type = st.selectbox(
        "Araç Türü",
        ["Otomobil", "Kamyon", "Motosiklet"],
        index=0
    )

with col3:
    speed_limit = st.slider(
        "Hız Limiti (km/s)",
        min_value=30,
        max_value=120,
        value=50,
        step=5
    )

if st.button("Simülasyonu Başlat", key="start_sim"):
    with st.spinner('Simülasyon çalışıyor...'):
        queue_lengths = simulate_traffic(road_type, vehicle_type, speed_limit)
        fig = plot_simulation(queue_lengths)
        st.pyplot(fig)
        
        # Simülasyon sonuçları
        st.subheader("📊 Simülasyon Sonuçları")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Ortalama Kuyruk Uzunluğu", f"{np.mean(queue_lengths):.1f} araç")
        with col2:
            st.metric("Maksimum Kuyruk Uzunluğu", f"{np.max(queue_lengths)} araç")
        with col3:
            st.metric("Minimum Kuyruk Uzunluğu", f"{np.min(queue_lengths)} araç") 