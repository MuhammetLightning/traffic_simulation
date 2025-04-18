# Trafik Akışı Simülasyonu

Bu proje, farklı yol türleri ve araç tipleri için trafik akışını simüle eden gelişmiş bir web uygulamasıdır. Simülasyon, gerçek dünya trafik koşullarını modelleyerek, trafik ışıklarının ve araç tiplerinin trafik akışı üzerindeki etkilerini analiz eder.

## Özellikler

### Yol Tipleri

- **Şehir İçi**

  - 2 şeritli yol
  - Trafik ışığı: 60 saniye kırmızı, 40 saniye yeşil
  - Temel varış oranı: 0.3 araç/saniye

- **Otoyol**
  - 3 şeritli yol
  - Trafik ışığı: 30 saniye kırmızı, 90 saniye yeşil
  - Temel varış oranı: 0.2 araç/saniye

### Araç Tipleri ve Özellikleri

- **Otomobil**

  - Maksimum hız: 70 km/s
  - Araç uzunluğu: 4.5 metre
  - Standart varış oranı

- **Otobüs**

  - Maksimum hız: 50 km/s
  - Araç uzunluğu: 12 metre
  - Varış oranı: Normal oranın %40'ı

- **Kamyon**
  - Maksimum hız: 40 km/s
  - Araç uzunluğu: 16 metre
  - Varış oranı: Normal oranın %30'u

## Kurulum

1. Python 3.12 veya daha yüksek bir sürümü yükleyin.

2. Gerekli Python paketlerini yükleyin:

```bash
pip install -r requirements.txt
```

3. Web sunucusunu başlatın:

```bash
py -3.12 server.py
```

4. Tarayıcınızda `http://localhost:8000` adresine gidin.

## Kullanım

1. Ana sayfadan "Simülasyonu Başlat" butonuna tıklayın
2. Simülasyon parametrelerini seçin:
   - Yol tipi (şehir içi veya otoyol)
   - Araç tipi (otomobil, otobüs veya kamyon)
   - Hız limiti (araç tipine göre maksimum değer otomatik ayarlanır)
3. "Simülasyonu Başlat" butonuna tıklayın
4. Sonuçları inceleyin:
   - Ortalama kuyruk uzunluğu
   - Maksimum kuyruk uzunluğu
   - Trafik akış hızı
   - Zaman bazlı kuyruk grafiği

## Teknik Detaylar

### Simülasyon Motoru

- Python tabanlı simülasyon motoru
- Poisson dağılımı kullanılarak rastgele araç varışları
- Araç tipine ve yol türüne göre özelleştirilmiş varış oranları
- Hız limitine bağlı olarak dinamik geçiş oranları

### Veri Analizi

- Ortalama ve maksimum kuyruk uzunluğu hesaplamaları
- Standart sapma ve medyan değerleri
- Trafik akış hızı analizi
- Matplotlib ile grafik görselleştirme

### Web Arayüzü

- Modern ve responsive tasarım
- Gerçek zamanlı veri görselleştirme
- Kullanıcı dostu form kontrolleri
- Detaylı sonuç raporlama

## Örnek Sonuçlar

### 3 Şeritli Otoyol (Otomobil)

- 70 km/s hızda:

  - Ortalama kuyruk: 0.76 araç
  - Maksimum kuyruk: 10 araç
  - Trafik akışı: 11.38 araç/dakika

- 20 km/s hızda:
  - Ortalama kuyruk: 0.23 araç
  - Maksimum kuyruk: 7 araç
  - Trafik akışı: 3.48 araç/dakika

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## İletişim

Proje ile ilgili soru ve önerileriniz için GitHub üzerinden issue açabilirsiniz.
