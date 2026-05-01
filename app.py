from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename

# Modül İmportları
from data_processing.preprocess import goruntu_hazirla
from ai_model.model import teshis_yap
from reports.generate_report import rapor_olustur # Zeynep'in kodu
import db_manager # Yeni yazdığımız veritabanı yardımcısı

app = Flask(__name__, template_folder='frontend', static_folder='frontend', static_url_path='/static')

UPLOAD_FOLDER = 'static/uploads' # Resimleri kalıcı tutalım ki raporda görünsün
REPORT_FOLDER = 'static/reports' # PDF'lerin gideceği yer
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

@app.route('/')
def ana_sayfa():
    return render_template('index.html')

@app.route('/analiz_et', methods=['POST'])
def analiz_api():
    if 'xray_file' not in request.files:
        return jsonify({'hata': 'Dosya bulunamadı'})
    
    file = request.files['xray_file']
    hasta_adi = request.form.get('hasta_adi', 'Anonim Hasta') # Frontend'den hasta adını al

    if file and file.filename != '':
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        try:
            # 1. Görüntü Ön İşleme
            matris = goruntu_hazirla(filepath)
            if matris is None:
                return jsonify({'hata': 'Görüntü okunamadı. Lütfen geçerli bir JPG/PNG dosyası yükleyin.'})

            # 2. AI Analizi
            sonuc = teshis_yap(matris)

            # 3. Veritabanına Kaydet (Esmanur'un şemasına göre)
            db_manager.sonuclari_kaydet(hasta_adi, sonuc['hastalik'], sonuc['guven_skoru'])

            # 4. PDF Raporu Oluştur (Zeynep'in modülü)
            report_filename = f"rapor_{filename}.pdf"
            report_path = os.path.join(REPORT_FOLDER, report_filename)
            rapor_olustur(hasta_adi, sonuc['guven_skoru'], sonuc['hastalik'], report_path)

            return jsonify({
                'basari': True,
                'hastalik': sonuc['hastalik'],
                'guven_skoru': sonuc['guven_skoru'],
                'aciklama': sonuc['aciklama'],
                'demo_modu': sonuc.get('demo_modu', False),
                'rapor_url': f"/indir/{report_filename}"
            })
            
        except Exception as e:
            return jsonify({'hata': f"Sistem hatası: {str(e)}"})

@app.route('/indir/<filename>')
def indir(filename):
    return send_from_directory(REPORT_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000, use_reloader=False)
