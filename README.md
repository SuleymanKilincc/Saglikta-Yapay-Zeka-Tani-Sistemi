# 🩺 Sağlıkta Yapay Zeka Destekli Tanı Sistemi

Göğüs röntgeni (X-Ray) görüntülerini analiz ederek **Normal**, **Pnömoni (Zatürre)** ve **Tüberküloz (Verem)** teşhisi yapabilen, yapay zeka destekli bir web uygulamasıdır.

---

## 🚀 Özellikler

- 🧠 **Yapay Zeka Analizi:** MobileNetV2 (Transfer Learning) mimarisi ile eğitilmiş CNN modeli (%94 doğruluk)
- 💻 **Modern Web Arayüzü:** Glassmorphism tasarımlı, responsive dark-theme arayüz
- 📄 **Otomatik PDF Raporu:** Her analiz sonrası hasta bilgilerini içeren rapor oluşturma
- 🗄️ **Veritabanı Entegrasyonu:** PostgreSQL ile hasta ve teşhis kayıtlarının güvenli saklanması
- 📁 **Sürükle-Bırak:** Röntgen görüntüsü yüklemek için drag & drop desteği

---

## 🛠️ Kullanılan Teknolojiler

| Katman | Teknoloji |
|---|---|
| **Backend** | Python, Flask |
| **Yapay Zeka** | TensorFlow 2.10, Keras, MobileNetV2 |
| **Görüntü İşleme** | OpenCV (cv2) |
| **Veritabanı** | PostgreSQL, psycopg2 |
| **PDF Raporlama** | ReportLab |
| **Frontend** | HTML5, CSS3 (Glassmorphism), Vanilla JS |
| **Güvenlik** | python-dotenv (.env) |

---

## 📁 Proje Yapısı

```
Saglikta-Yapay-Zeka-Tani-Sistemi/
├── app.py                    # Flask web sunucusu (ana giriş noktası)
├── db_manager.py             # PostgreSQL veritabanı yöneticisi
├── requirements.txt          # Python kütüphane listesi
├── .env.example              # Ortam değişkenleri şablonu
│
├── ai_model/
│   ├── model.py              # MobileNetV2 model mimarisi ve teşhis fonksiyonu
│   ├── train.py              # Model eğitim scripti
│   ├── config.py             # Tüm model ayarları (hyperparametreler)
│   └── saglik_cnn_model.h5   # Eğitilmiş model dosyası (Git'e dahil değil)
│
├── data_processing/
│   └── preprocess.py         # Görüntü ön işleme (resize, normalize)
│
├── frontend/
│   ├── index.html            # Ana sayfa (arayüz)
│   ├── style.css             # CSS stilleri (dark theme, glassmorphism)
│   └── script.js             # Frontend JavaScript (API çağrıları, animasyonlar)
│
├── reports/
│   └── generate_report.py    # PDF rapor oluşturma (ReportLab)
│
└── dataset/                  # Eğitim veri seti (Git'e dahil değil)
    ├── train/
    │   ├── Normal/
    │   ├── Pneumonia/
    │   └── Tuberculosis/
    └── test/
        ├── Normal/
        ├── Pneumonia/
        └── Tuberculosis/
```

---

## ⚙️ Kurulum ve Çalıştırma

### Gereksinimler
- Python 3.10
- PostgreSQL 18+
- pgAdmin 4 (veritabanı yönetimi için)

### Adım 1: Projeyi İndirin
```bash
git clone https://github.com/SuleymanKilincc/Saglikta-Yapay-Zeka-Tani-Sistemi.git
cd Saglikta-Yapay-Zeka-Tani-Sistemi
```

### Adım 2: Kütüphaneleri Yükleyin
```bash
pip install -r requirements.txt
```

### Adım 3: Veritabanını Kurun
1. pgAdmin 4'ü açın
2. `saglik_ai` adında yeni bir veritabanı oluşturun
3. Gerekli tabloları oluşturun: `patients`, `studies`, `images`, `ai_diagnoses`, `reports`

### Adım 4: Ortam Değişkenlerini Ayarlayın
`.env.example` dosyasını kopyalayıp `.env` olarak adlandırın ve içine kendi PostgreSQL şifrenizi yazın:
```
DB_PASSWORD=kendi_sifrenizi_yazin
```

### Adım 5: Uygulamayı Başlatın
```bash
python app.py
```

> **Not:** Model dosyası (`saglik_cnn_model.h5`) ilk çalıştırmada **Google Drive'dan otomatik olarak indirilir** (~90MB). İnternet bağlantınızın olduğundan emin olun. İndirme tamamlandıktan sonra uygulama tam modda çalışmaya başlar.

---

## 🧠 Yapay Zeka Modeli Hakkında

- **Mimari:** MobileNetV2 (Transfer Learning) + Özel sınıflandırıcı katmanlar
- **Eğitim Veri Seti:** Kaggle Chest X-Ray (Pneumonia + Tuberculosis) veri setleri
- **Eğitim Doğruluğu:** %97.24
- **Doğrulama Doğruluğu:** %94.09
- **Test Doğruluğu:** %86.19
- **Sınıflar:** Normal, Pnömoni, Tüberküloz
- **Görüntü Formatı:** 224×224 RGB

---

## 👥 Geliştirme Ekibi

- **Süleyman Kılınç** — Scrum Master / Backend & AI Entegrasyonu
- **Ömer Ensar Şahin** — Yapay Zeka Model Mimarisi
- **Esmanur** — Veritabanı Tasarımı ve Şema
- **Zeynep Karataş** — PDF Raporlama Modülü
- **Cumali Bilgiç** — Frontend / Arayüz Geliştirici
---

> ⚠️ **Yasal Uyarı:** Bu sistem yalnızca akademik amaçlarla geliştirilmiştir. Gerçek tıbbi teşhis için mutlaka bir doktora başvurunuz.
