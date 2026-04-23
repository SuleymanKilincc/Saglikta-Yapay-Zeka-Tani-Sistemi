from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename

# Ekibimizin Modülleri (Senin ve Ömer'in yazdığı kodlar)
from data_processing.preprocess import goruntu_hazirla
from ai_model.model import teshis_yap

# Flask uygulamasını başlat (Cumali'nin frontend klasörünü tanıyacak şekilde)
app = Flask(__name__, template_folder='frontend', static_folder='frontend')

# Yüklenen röntgenlerin işlem sırasında geçici olarak duracağı klasör
UPLOAD_FOLDER = 'temp_uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def ana_sayfa():
    # Cumali'nin tasarımını ekrana basıyoruz
    return render_template('index.html')

@app.route('/analiz_et', methods=['POST'])
def analiz_api():
    # Frontend'den dosya geldi mi kontrolü
    if 'xray_file' not in request.files:
        return jsonify({'hata': 'Dosya bulunamadı'})
        
    file = request.files['xray_file']
    if file.filename == '':
        return jsonify({'hata': 'Dosya seçilmedi'})

    if file:
        # 1. Dosyayı güvenli bir şekilde geçici klasöre kaydet
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            # 2. SÜLEYMAN'IN KODU ÇALIŞIYOR (Görüntüyü Temizle ve Boyutlandır)
            matris = goruntu_hazirla(filepath)

            # 3. ÖMER'İN KODU ÇALIŞIYOR (Yapay Zeka Tahmini)
            # (Ömer'in Demo Modu sayesinde eğitilmiş model olmasa bile çalışacak)
            sonuc = teshis_yap(matris)

            # İşlem bitince sunucuyu şişirmemek için geçici resmi siliyoruz
            os.remove(filepath)

            # 4. Sonucu Cumali'nin arayüzüne gönderiyoruz
            return jsonify({
                'basari': True,
                'hastalik': sonuc['hastalik'],
                'guven_skoru': sonuc['guven_skoru'],
                'aciklama': sonuc['aciklama']
            })
            
        except Exception as e:
            return jsonify({'hata': f"İşlem sırasında hata: {str(e)}"})

if __name__ == '__main__':
    print("🚀 AI Tanı Sunucusu Başlatılıyor...")
    app.run(debug=True, port=5000)
