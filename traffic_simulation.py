import numpy as np
import matplotlib.pyplot as plt
import os

class TrafficSimulation:
    def __init__(self, road_type, vehicle_type, speed_limit):
        self.road_type = road_type
        self.vehicle_type = vehicle_type
        self.speed_limit = int(speed_limit)
        
        # Araç özellikleri ve hız limitleri
        self.vehicle_properties = {
            'car': {'name': 'Otomobil', 'max_speed': 70, 'length': 4.5},
            'bus': {'name': 'Otobüs', 'max_speed': 50, 'length': 12},
            'truck': {'name': 'Kamyon', 'max_speed': 40, 'length': 16}
        }
        
        # Yol özellikleri ve trafik ışığı süreleri
        self.road_properties = {
            'city': {
                'name': 'Şehir İçi',
                'lanes': 2,
                'red_duration': 60,
                'green_duration': 40,
                'base_arrival_rate': 0.3  # Araç/saniye
            },
            'highway': {
                'name': 'Otoyol',
                'lanes': 3,
                'red_duration': 30,
                'green_duration': 90,
                'base_arrival_rate': 0.2  # Araç/saniye
            }
        }
        
        # Simülasyon süresi (1 saat = 3600 saniye)
        self.simulation_time = 3600
    
    def calculate_arrival_rate(self):
        """Araç varış oranını hesaplar"""
        # Yol türüne göre temel varış oranı
        base_rate = self.road_properties[self.road_type]['base_arrival_rate']
        
        # Araç türüne göre ayarlama
        vehicle_speed = self.vehicle_properties[self.vehicle_type]['max_speed']
        speed_factor = min(self.speed_limit, vehicle_speed) / vehicle_speed
        
        # Hız ve araç türüne göre varış oranını ayarla
        if self.vehicle_type == 'car':
            base_rate *= 1.0  # Otomobiller için standart oran
        elif self.vehicle_type == 'bus':
            base_rate *= 0.4  # Otobüsler daha az sıklıkta
        else:  # truck
            base_rate *= 0.3  # Kamyonlar en az sıklıkta
        
        # Hız faktörünü uygula
        arrival_rate = base_rate * speed_factor
        
        return arrival_rate
    
    def simulate(self):
        """Trafik simülasyonunu çalıştırır"""
        np.random.seed(42)  # Tekrarlanabilirlik için
        time_steps = np.arange(self.simulation_time)
        arrival_rate = self.calculate_arrival_rate()
        
        # Poisson dağılımı ile araç varışları
        arrivals = np.random.poisson(arrival_rate, size=len(time_steps))
        
        # Yol ve trafik ışığı özellikleri
        road_info = self.road_properties[self.road_type]
        red_duration = road_info['red_duration']
        green_duration = road_info['green_duration']
        cycle_time = red_duration + green_duration
        
        # Kuyruk uzunluğu ve akış hesaplama
        queue_lengths = []
        current_queue = 0
        total_vehicles = 0
        passed_vehicles = 0
        
        for t in time_steps:
            # Trafik ışığı durumu
            is_green = (t % cycle_time) < green_duration
            
            # Yeni araçların kuyruğa eklenmesi
            new_arrivals = arrivals[t]
            current_queue += new_arrivals
            total_vehicles += new_arrivals
            
            if is_green:
                # Yeşil ışıkta geçen araç sayısı
                # Her şeritte saniyede geçebilecek araç sayısı
                flow_rate = min(2.0, self.speed_limit / 50.0)  # Maksimum 2 araç/saniye/şerit
                max_outflow = int(flow_rate * road_info['lanes'])
                
                # Kuyruktan çıkan araç sayısı
                outflow = min(current_queue, max_outflow)
                current_queue = max(0, current_queue - outflow)
                passed_vehicles += outflow
            
            queue_lengths.append(current_queue)
        
        # Akış istatistiklerini hesapla
        simulation_minutes = self.simulation_time / 60  # Dakika cinsinden süre
        average_flow = passed_vehicles / simulation_minutes  # Araç/dakika
        
        return time_steps, queue_lengths, {
            'total_vehicles': total_vehicles,
            'passed_vehicles': passed_vehicles,
            'average_flow': average_flow
        }
    
    def plot_results(self, time_steps, queue_lengths):
        """Simülasyon sonuçlarını görselleştirir"""
        try:
            # NumPy dizilerini liste ve int/float'a dönüştür
            time_steps = [int(t) for t in time_steps]
            queue_lengths = [float(q) for q in queue_lengths]
            
            plt.figure(figsize=(12, 6))
            
            # Ana kuyruk uzunluğu grafiği
            plt.plot(time_steps, queue_lengths, 'b-', label='Kuyruk Uzunluğu', alpha=0.6)
            
            # Ortalama değer çizgisi
            avg_queue = sum(queue_lengths) / len(queue_lengths)
            plt.axhline(y=avg_queue, color='b', linestyle='--', label=f'Ortalama ({avg_queue:.2f})')
            
            # Maksimum noktaları işaretle
            max_queue = max(queue_lengths)
            max_times = []
            max_queues = []
            for i, q in enumerate(queue_lengths):
                if q == max_queue:
                    max_times.append(time_steps[i])
                    max_queues.append(q)
            
            if max_times:  # Eğer maksimum noktalar varsa
                plt.plot(max_times, max_queues, 'ro', label=f'Maksimum ({int(max_queue)})', markersize=8)
            
            plt.xlabel('Zaman (saniye)')
            plt.ylabel('Kuyruk Uzunluğu (araç)')
            
            road_name = self.road_properties[self.road_type]['name']
            vehicle_name = self.vehicle_properties[self.vehicle_type]['name']
            
            plt.title(f'Trafik Simülasyonu\n{road_name} - {vehicle_name} (Hız Limiti: {self.speed_limit} km/s)')
            plt.grid(True, alpha=0.3)
            plt.legend()
            
            # Grafik dosyasının tam yolu
            graph_path = os.path.join(os.getcwd(), 'images', 'traffic_simulation_advanced_graph.png')
            print(f"Grafik kaydediliyor: {graph_path}")
            
            # images klasörünün varlığını kontrol et
            os.makedirs(os.path.dirname(graph_path), exist_ok=True)
            
            # Grafiği kaydet
            plt.savefig(graph_path, dpi=100, bbox_inches='tight')
            print("Grafik başarıyla kaydedildi")
            plt.close()
            
            return True
        except Exception as e:
            print(f"Grafik oluşturma hatası: {str(e)}")
            plt.close()
            return False

def run_simulation(road_type, vehicle_type, speed_limit):
    """Simülasyonu çalıştırır ve sonuçları döndürür"""
    try:
        print(f"Simülasyon başlatılıyor: road_type={road_type}, vehicle_type={vehicle_type}, speed_limit={speed_limit}")
        
        # Parametreleri doğrula
        if not isinstance(speed_limit, (int, float)):
            raise ValueError("Hız limiti sayısal bir değer olmalıdır")
        
        simulation = TrafficSimulation(road_type, vehicle_type, speed_limit)
        time_steps, queue_lengths, flow_stats = simulation.simulate()
        
        # NumPy dizilerini Python listelerine dönüştür
        queue_lengths = [float(q) for q in queue_lengths]
        
        # Sonuçları hesapla
        avg_queue = sum(queue_lengths) / len(queue_lengths)
        max_queue = max(queue_lengths)
        
        # Grafiği çiz
        if not simulation.plot_results(time_steps, queue_lengths):
            raise Exception("Grafik oluşturulamadı")
        
        results = {
            'average_queue': round(float(avg_queue), 2),
            'max_queue': int(max_queue),
            'flow_stats': {
                'total_vehicles': int(flow_stats['total_vehicles']),
                'passed_vehicles': int(flow_stats['passed_vehicles']),
                'average_flow': round(float(flow_stats['average_flow']), 2),
                'flow_rate': round(float(flow_stats['passed_vehicles']) / (simulation.simulation_time / 60), 2)
            }
        }
        
        print(f"Simülasyon sonuçları: {results}")
        return results
        
    except Exception as e:
        print(f"Simülasyon hatası: {str(e)}")
        raise Exception(f"Simülasyon hatası: {str(e)}")

if __name__ == "__main__":
    # Test simülasyonu
    results = run_simulation('city', 'car', 50)
    print(f"Ortalama Kuyruk Uzunluğu: {results['average_queue']}")
    print(f"Maksimum Kuyruk Uzunluğu: {results['max_queue']}") 