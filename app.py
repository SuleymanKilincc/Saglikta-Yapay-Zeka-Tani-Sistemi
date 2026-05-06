from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename

from data_processing.preprocess import goruntu_hazirla
from ai_model.model import teshis_yap
from reports.generate_report import rapor_olustur
import db_manager

# ============================================================
# MODEL OTOMATIK INDIRME
# ============================================================
MODEL_PATH = os.path.join('ai_model', 'saglik_cnn_model.h5')
DRIVE_FILE_ID = '1s4jud1ID-2AXPSMtnMNl63i0RelVc19B'

if not os.path.exists(MODEL_PATH):
    print("=" * 55)
    print("  Model dosyasi bulunamadi, Google Drive'dan indiriliyor...")
    print("  Bu islem birkac dakika surebilir, lutfen bekleyin.")
    print("=" * 55)
    try:
        import gdown
        gdown.download(f'https://drive.google.com/uc?id={DRIVE_FILE_ID}', MODEL_PATH, quiet=False)
        print("  Model basariyla indirildi!")
        print("=" * 55)
    except Exception as e:
        print(f"  HATA: Model indirilemedi: {e}")
        print("  Uygulama demo modunda calisacak.")
        print("=" * 55)

app = Flask(__name__, template_folder='frontend', static_folder='frontend', static_url_path='/static')

UPLOAD_FOLDER = 'static/uploads'
REPORT_FOLDER = 'static/reports'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

# Veritabani tablolari otomatik olusturulsun
db_manager.veritabani_kur()

@app.route('/')
def ana_sayfa():
    return render_template('index.html')

@app.route('/analiz_et', methods=['POST'])
def analiz_api():
    if 'xray_file' not in request.files:
        return jsonify({'hata': 'Dosya bulunamadi'})

    file = request.files['xray_file']

    # Hasta bilgilerini al
    hasta_adi    = request.form.get('hasta_adi', 'Anonim')
    hasta_soyadi = request.form.get('hasta_soyadi', '')
    dogum_tarihi = request.form.get('dogum_tarihi', '2000-01-01')
    cinsiyet     = request.form.get('cinsiyet', 'B')
    doktor_adi   = request.form.get('doktor_adi', 'Belirtilmedi')
    departman    = request.form.get('departman', 'Radyoloji')

    hasta_tam_adi = f"{hasta_adi} {hasta_soyadi}".strip()

    if file and file.filename != '':
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        try:
            # 1. Goruntu On Isleme
            matris = goruntu_hazirla(filepath)
            if matris is None:
                return jsonify({'hata': 'Goruntu okunamadi. Lutfen gecerli bir JPG/PNG dosyasi yukleyin.'})

            # 2. AI Analizi
            sonuc = teshis_yap(matris)

            # 3. Veritabanina Kaydet (TC otomatik uretilir)
            db_manager.sonuclari_kaydet(
                hasta_adi=hasta_tam_adi,
                hasta_soyadi=hasta_soyadi,
                dogum_tarihi=dogum_tarihi,
                cinsiyet=cinsiyet,
                doktor_adi=doktor_adi,
                departman=departman,
                teshis=sonuc['hastalik'],
                guven_skoru=sonuc['guven_skoru']
            )

            # 4. PDF Raporu Olustur
            report_filename = f"rapor_{filename}.pdf"
            report_path = os.path.join(REPORT_FOLDER, report_filename)
            rapor_olustur(
                hasta_adi=hasta_tam_adi,
                sonuc_yuzdesi=sonuc['guven_skoru'],
                teshis_adi=sonuc['hastalik'],
                dosya_adi=report_path,
                doktor_adi=doktor_adi,
                departman=departman
            )

            return jsonify({
                'basari': True,
                'hastalik': sonuc['hastalik'],
                'guven_skoru': sonuc['guven_skoru'],
                'aciklama': sonuc['aciklama'],
                'demo_modu': sonuc.get('demo_modu', False),
                'rapor_url': f"/indir/{report_filename}"
            })

        except Exception as e:
            return jsonify({'hata': f"Sistem hatasi: {str(e)}"})

    return jsonify({'hata': 'Gecersiz dosya'})

@app.route('/indir/<filename>')
def indir(filename):
    return send_from_directory(REPORT_FOLDER, filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port, use_reloader=False)
