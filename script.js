// API endpoint'ini tanımla
const API_URL = 'https://traffic-simulation-api.onrender.com/api/simulate';

// Simülasyon formunu yakala
document.addEventListener('DOMContentLoaded', function() {
    const simulationForm = document.getElementById('simulationForm');
    if (simulationForm) {
        simulationForm.addEventListener('submit', runSimulation);
    }
});

async function runSimulation(event) {
    event.preventDefault();
    
    // Loading durumunu göster
    document.getElementById('loadingSpinner').style.display = 'block';
    document.getElementById('results').style.display = 'none';
    
    // Form verilerini al
    const roadType = document.getElementById('roadType').value;
    const vehicleType = document.getElementById('vehicleType').value;
    const speedLimit = parseInt(document.getElementById('speedLimit').value);

    try {
        // API'ye istek at
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                road_type: roadType,
                vehicle_type: vehicleType,
                speed_limit: speedLimit
            })
        });

        if (!response.ok) {
            throw new Error('API yanıt vermedi');
        }

        const data = await response.json();
        displayResults(data);
    } catch (error) {
        console.error('Hata:', error);
        alert('Simülasyon sırasında bir hata oluştu. Lütfen tekrar deneyin.');
    } finally {
        document.getElementById('loadingSpinner').style.display = 'none';
    }
}

function displayResults(data) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.style.display = 'block';
    
    // Sonuçları göster
    document.getElementById('averageQueue').textContent = 
        `Ortalama Kuyruk Uzunluğu: ${data.average_queue.toFixed(2)} araç`;
    document.getElementById('maxQueue').textContent = 
        `Maksimum Kuyruk Uzunluğu: ${data.max_queue} araç`;
    document.getElementById('flowRate').textContent = 
        `Trafik Akış Hızı: ${data.flow_stats.flow_rate.toFixed(2)} araç/dakika`;
    
    // İstatistikleri güncelle
    updateStats(data.flow_stats);
}

function updateStats(flowStats) {
    const statsDiv = document.getElementById('statistics');
    if (statsDiv) {
        statsDiv.innerHTML = `
            <h3>Detaylı İstatistikler</h3>
            <ul>
                <li>Toplam Araç: ${flowStats.total_vehicles}</li>
                <li>Geçen Araç: ${flowStats.passed_vehicles}</li>
                <li>Ortalama Akış: ${flowStats.average_flow.toFixed(2)} araç/dakika</li>
            </ul>
        `;
    }
}

function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    setTimeout(() => {
        errorDiv.style.display = 'none';
    }, 5000);
}

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