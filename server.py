from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
from traffic_simulation import run_simulation
from urllib.parse import urlparse, unquote

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # URL'yi parse et ve query parametrelerini temizle
            parsed_url = urlparse(self.path)
            clean_path = unquote(parsed_url.path)

            if clean_path == '/':
                clean_path = '/index.html'
            elif clean_path == '/simulation':
                clean_path = '/simulation.html'
            elif clean_path == '/about':
                clean_path = '/about.html'
            
            # Dosya uzantısını kontrol et
            file_extension = os.path.splitext(clean_path)[1]
            if file_extension == '.html':
                content_type = 'text/html'
            elif file_extension == '.css':
                content_type = 'text/css'
            elif file_extension == '.js':
                content_type = 'application/javascript'
            elif file_extension == '.png':
                content_type = 'image/png'
            elif file_extension == '.ico':
                content_type = 'image/x-icon'
            else:
                content_type = 'text/plain'

            # Dosyayı aç ve oku
            file_path = clean_path[1:] if clean_path.startswith('/') else clean_path
            with open(file_path, 'rb') as file:
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.end_headers()
                self.wfile.write(file.read())
        except FileNotFoundError:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'File not found')
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(str(e).encode('utf-8'))

    def do_POST(self):
        if self.path == '/run_simulation':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                print(f"Alınan veri: {data}")  # Hata ayıklama

                # Simülasyonu çalıştır
                try:
                    print("Simülasyon başlatılıyor...")  # Hata ayıklama
                    results = run_simulation(
                        data['road_type'],
                        data['vehicle_type'],
                        int(data['speed_limit'])
                    )
                    print(f"Simülasyon sonuçları: {results}")  # Hata ayıklama
                except Exception as e:
                    print(f"Simülasyon hatası: {e}")  # Hata ayıklama
                    raise

                # Sonuçları gönder
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
                # NumPy tiplerini Python tiplerine dönüştür
                results = {
                    'average_queue': float(results['average_queue']),
                    'max_queue': int(results['max_queue']),
                    'flow_stats': {
                        'total_vehicles': int(results['flow_stats']['total_vehicles']),
                        'passed_vehicles': int(results['flow_stats']['passed_vehicles']),
                        'average_flow': float(results['flow_stats']['average_flow']),
                        'flow_rate': float(results['flow_stats']['flow_rate'])
                    }
                }
                
                response_data = json.dumps(results, ensure_ascii=False)
                print(f"Gönderilen yanıt: {response_data}")  # Hata ayıklama
                self.wfile.write(response_data.encode('utf-8'))
                self.wfile.flush()  # Yanıtın gönderildiğinden emin olmak için
            except json.JSONDecodeError as e:
                print(f"JSON ayrıştırma hatası: {e}")  # Hata ayıklama
                self.send_error(400, 'Invalid JSON data')
            except KeyError as e:
                print(f"Eksik parametre hatası: {e}")  # Hata ayıklama
                self.send_error(400, f'Missing parameter: {str(e)}')
            except ValueError as e:
                print(f"Geçersiz parametre hatası: {e}")  # Hata ayıklama
                self.send_error(400, f'Invalid parameter: {str(e)}')
            except Exception as e:
                print(f"Beklenmeyen hata: {e}")  # Hata ayıklama
                self.send_error(500, f'Simulation error: {str(e)}')
        else:
            self.send_error(404, 'Page not found')

def run():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, RequestHandler)
    print('Web sunucusu http://localhost:8000 adresinde çalışıyor...')
    httpd.serve_forever()

if __name__ == '__main__':
    run() 