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
    const loadingSpinner = document.querySelector('#startSimulation .loading-spinner');
    const resultsSection = document.querySelector('.simulation-results');
    
    if (loadingSpinner) loadingSpinner.style.display = 'block';
    if (resultsSection) resultsSection.style.display = 'none';
    
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
        if (loadingSpinner) loadingSpinner.style.display = 'none';
    }
}

function displayResults(data) {
    const resultsSection = document.querySelector('.simulation-results');
    if (resultsSection) {
        resultsSection.style.display = 'block';
    }
    
    // Sonuçları göster
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

    // Sonuçları güncelle
    if (resultElements.roadType) resultElements.roadType.textContent = data.road_type;
    if (resultElements.vehicleType) resultElements.vehicleType.textContent = data.vehicle_type;
    if (resultElements.speedLimit) resultElements.speedLimit.textContent = `${data.speed_limit} km/s`;
    if (resultElements.averageQueue) resultElements.averageQueue.textContent = data.average_queue.toFixed(2);
    if (resultElements.maxQueue) resultElements.maxQueue.textContent = data.max_queue;
    if (resultElements.queueStdDev) resultElements.queueStdDev.textContent = data.queue_std_dev.toFixed(2);
    if (resultElements.queueMedian) resultElements.queueMedian.textContent = data.queue_median.toFixed(2);
    if (resultElements.maxQueueTime) resultElements.maxQueueTime.textContent = `${data.max_queue_time}s`;
    if (resultElements.maxQueueDuration) resultElements.maxQueueDuration.textContent = `${data.max_queue_duration}s`;
    if (resultElements.averageFlow) resultElements.averageFlow.textContent = data.flow_rate.toFixed(2);
    if (resultElements.totalVehicles) resultElements.totalVehicles.textContent = data.total_vehicles;
    if (resultElements.flowRate) resultElements.flowRate.textContent = `${data.flow_rate.toFixed(2)} araç/dakika`;

    // Grafik gösterimi
    const graphImage = document.getElementById('graphImage');
    if (graphImage && data.graph_url) {
        graphImage.src = data.graph_url;
        graphImage.style.display = 'block';
    }
}

// Hız limiti değerini gösteren script
document.addEventListener('DOMContentLoaded', function() {
    const speedLimit = document.getElementById('speedLimit');
    const speedValue = document.getElementById('speedValue');
    if (speedLimit && speedValue) {
        speedLimit.addEventListener('input', () => {
            speedValue.textContent = speedLimit.value;
        });
    }
});

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