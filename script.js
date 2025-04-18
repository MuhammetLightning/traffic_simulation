// API URL'ini buraya ekleyin (Render'dan alınan URL)
const API_URL = 'https://traffic-simulation-api.onrender.com';

document.addEventListener('DOMContentLoaded', function() {
    // Form ve sonuç elementlerini seç
    const simulationForm = document.getElementById('simulationForm');
    const vehicleTypeSelect = document.getElementById('vehicle_type');
    const speedLimitInput = document.getElementById('speed_limit');
    const startButton = document.getElementById('startSimulation');
    const resultsSection = document.querySelector('.simulation-results');
    const graphImage = document.getElementById('graphImage');
    
    // Sonuç elementleri
    const resultElements = {
        roadType: document.getElementById('resultRoadType'),
        vehicleType: document.getElementById('resultVehicleType'),
        speedLimit: document.getElementById('resultSpeedLimit'),
        averageQueue: document.getElementById('averageQueue'),
        maxQueue: document.getElementById('maxQueue'),
        queueStdDev: document.getElementById('queueStdDev'),
        queueMedian: document.getElementById('queueMedian'),
        maxQueueTime: document.getElementById('maxQueueTime'),
        maxQueueDuration: document.getElementById('maxQueueDuration'),
        averageFlow: document.getElementById('averageFlow'),
        totalVehicles: document.getElementById('totalVehicles'),
        flowRate: document.getElementById('flowRate')
    };
    
    // Araç tiplerine göre maksimum hızlar
    const maxSpeeds = {
        'car': 70,
        'bus': 50,
        'truck': 40
    };

    // Araç ve yol tiplerinin Türkçe karşılıkları
    const translations = {
        road_types: {
            'city': 'Şehir İçi (2 Şerit)',
            'highway': 'Otoyol (3 Şerit)'
        },
        vehicle_types: {
            'car': 'Otomobil',
            'bus': 'Otobüs',
            'truck': 'Kamyon'
        }
    };

    // Varsayılan hız limiti
    speedLimitInput.value = '50';

    // Araç tipi değiştiğinde hız limitini güncelle
    vehicleTypeSelect.addEventListener('change', function() {
        const selectedVehicle = this.value;
        if (selectedVehicle) {
            const maxSpeed = maxSpeeds[selectedVehicle];
            speedLimitInput.max = maxSpeed;
            
            // Eğer mevcut değer maksimum hızdan yüksekse, maksimum hıza ayarla
            if (parseInt(speedLimitInput.value) > maxSpeed) {
                speedLimitInput.value = maxSpeed;
            }
            
            // Yardımcı metni güncelle
            document.querySelector('.speed-limit-text').textContent = 
                `Maksimum hız limiti: ${maxSpeed} km/s`;
        }
    });

    // Ham veri gösterimi ve grafik indirme
    document.getElementById('showRawData').addEventListener('click', function() {
        // Ham veriyi modal veya yeni pencerede göster
        alert('Bu özellik yakında eklenecek');
    });

    document.getElementById('downloadGraph').addEventListener('click', function() {
        const link = document.createElement('a');
        link.download = 'trafik_simulasyonu_grafik.png';
        link.href = graphImage.src;
        link.click();
    });

    // Form gönderildiğinde
    simulationForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Loading durumunu göster
        const loadingSpinner = document.getElementById('loadingSpinner');
        loadingSpinner.style.display = 'block';
        
        // Form verilerini al
        const formData = {
            road_type: document.getElementById('road_type').value,
            vehicle_type: vehicleTypeSelect.value,
            speed_limit: parseInt(speedLimitInput.value)
        };

        try {
            // API'ye istek at
            const response = await fetch(`${API_URL}/api/simulate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                throw new Error('Simülasyon çalıştırılırken bir hata oluştu');
            }

            const data = await response.json();
            
            // Simülasyon parametrelerini güncelle
            resultElements.roadType.textContent = translations.road_types[formData.road_type];
            resultElements.vehicleType.textContent = translations.vehicle_types[formData.vehicle_type];
            resultElements.speedLimit.textContent = formData.speed_limit + ' km/s';
            
            // Ana sonuçları güncelle
            resultElements.averageQueue.textContent = data.average_queue.toFixed(2);
            resultElements.maxQueue.textContent = data.max_queue;
            
            // Detaylı sonuçları güncelle
            if (data.queue_stats) {
                resultElements.queueStdDev.textContent = data.queue_stats.std_dev.toFixed(2);
                resultElements.queueMedian.textContent = data.queue_stats.median.toFixed(2);
            }
            
            if (data.max_queue_info) {
                resultElements.maxQueueTime.textContent = formatTime(data.max_queue_info.time);
                resultElements.maxQueueDuration.textContent = formatDuration(data.max_queue_info.duration);
            }
            
            if (data.flow_stats) {
                resultElements.averageFlow.textContent = data.flow_stats.average_flow.toFixed(2);
                resultElements.totalVehicles.textContent = data.flow_stats.total_vehicles;
                resultElements.flowRate.textContent = data.flow_stats.flow_rate.toFixed(2) + ' araç/dk';
            }
            
            // Grafiği göster
            graphImage.src = '/images/traffic_simulation_advanced_graph.png?' + new Date().getTime();
            graphImage.style.display = 'block';

            // Sonuçlar bölümünü göster ve kaydır
            resultsSection.style.display = 'block';
            resultsSection.scrollIntoView({ behavior: 'smooth' });

        } catch (error) {
            console.error('Hata:', error);
            showError('Simülasyon çalıştırılırken bir hata oluştu: ' + error.message);
        } finally {
            loadingSpinner.style.display = 'none';
        }
    });

    // Yardımcı fonksiyonlar
    function formatTime(seconds) {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = seconds % 60;
        return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
    }

    function formatDuration(seconds) {
        if (seconds < 60) {
            return `${seconds} saniye`;
        }
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = seconds % 60;
        return `${minutes} dk ${remainingSeconds} sn`;
    }

    // Responsive menü için
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.style.backgroundColor = 'rgba(44, 62, 80, 0.9)';
        } else {
            navbar.style.backgroundColor = 'var(--primary-color)';
        }
    });
});

function displayResults(data) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.style.display = 'block';
    
    // Sonuçları güncelle
    document.getElementById('averageQueue').textContent = 
        `${data.average_queue.toFixed(2)} araç`;
    document.getElementById('maxQueue').textContent = 
        `${data.max_queue} araç`;
    document.getElementById('flowRate').textContent = 
        `${data.flow_stats.flow_rate.toFixed(2)} araç/dakika`;
    
    // İstatistikleri güncelle
    const statsDiv = document.getElementById('statistics');
    if (statsDiv) {
        statsDiv.innerHTML = `
            <h3>Detaylı İstatistikler</h3>
            <ul>
                <li>Toplam Araç: ${data.flow_stats.total_vehicles}</li>
                <li>Geçen Araç: ${data.flow_stats.passed_vehicles}</li>
                <li>Ortalama Akış: ${data.flow_stats.average_flow.toFixed(2)} araç/dakika</li>
            </ul>
        `;
    }
    
    // Sonuçlara kaydır
    resultsDiv.scrollIntoView({ behavior: 'smooth' });
}

function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    setTimeout(() => {
        errorDiv.style.display = 'none';
    }, 5000);
}

// Hız limiti değerini gösteren script
const speedLimit = document.getElementById('speed_limit');
const speedValue = document.getElementById('speedValue');
if (speedLimit && speedValue) {
    speedLimit.addEventListener('input', () => {
        speedValue.textContent = speedLimit.value;
    });
} 