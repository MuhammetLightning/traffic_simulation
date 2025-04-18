import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io

def simulate_traffic(road_type, vehicle_type, speed_limit):
    # Simülasyon parametreleri
    time_steps = 100
    queue_lengths = []
    
    # Poisson dağılımı ile araç varış zamanları
    arrival_times = np.random.poisson(lam=5, size=time_steps)
    
    # Simülasyon döngüsü
    for t in range(time_steps):
        # Kuyruk uzunluğu hesaplama (basit bir örnek)
        queue_length = arrival_times[t] * (speed_limit / 50)  # Hız limitine göre ölçeklendirme
        queue_lengths.append(queue_length)
    
    return queue_lengths

def plot_simulation(queue_lengths):
    plt.figure(figsize=(10, 6))
    plt.plot(queue_lengths)
    plt.xlabel('Zaman')
    plt.ylabel('Kuyruk Uzunluğu')
    plt.title('Trafik Simülasyonu')
    plt.grid(True)
    return plt

st.title('Trafik Akışı Simülasyonu')

# Kontroller
col1, col2, col3 = st.columns(3)

with col1:
    road_type = st.selectbox('Yol Türü', ['Şehir İçi', 'Otoyol'])

with col2:
    vehicle_type = st.selectbox('Araç Türü', ['Otomobil', 'Otobüs', 'Kamyon'])

with col3:
    speed_limit = st.slider('Hız Limiti (km/s)', 30, 120, 50)

if st.button('Simülasyonu Başlat'):
    # Simülasyonu çalıştır
    queue_lengths = simulate_traffic(road_type, vehicle_type, speed_limit)
    
    # Grafiği oluştur
    fig = plot_simulation(queue_lengths)
    
    # Grafiği göster
    st.pyplot(fig)
    
    # Sonuçları göster
    st.write(f"Ortalama Kuyruk Uzunluğu: {np.mean(queue_lengths):.2f}")
    st.write(f"Maksimum Kuyruk Uzunluğu: {np.max(queue_lengths):.2f}") 