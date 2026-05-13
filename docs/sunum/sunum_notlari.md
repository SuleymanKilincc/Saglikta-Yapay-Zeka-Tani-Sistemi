# Proje Sunum Notları

**Sorumlu:** Süleyman Kılınç  
**Görev:** Proje Sunumu Hazırlığı ve Prova — Hafta 6  
**Tarih:** 11.05.2026

---

## 1. Açılış Konuşması (1-2 dakika)

> *"Hocam, merhaba. Ben Süleyman Kılınç. Bugün size Sağlıkta Yapay Zeka Destekli Tanı Sistemi projemizi sunacağım. Bu proje, akciğer röntgeni görüntülerini analiz ederek Normal, Pnömoni ve Tüberküloz tanısı koyabilen, web tabanlı bir yapay zeka destekli karar destek sistemidir. Beş kişilik ekip olarak altı hafta boyunca geliştirdik. Önce sistemi kısaca tanıtacağım, ardından canlı demo yapacağım."*

---

## 2. Slayt / Anlatım Sırası

### Bölüm 1 — Proje Tanıtımı (2 dakika)
- Projenin amacı: Doktorlara X-Ray analizinde destek sağlamak
- Neden bu konu? → Pnömoni ve Tüberküloz erken teşhis edilirse tedavi başarısı artar
- Sistemin çözdüğü problem: Manuel radyoloji analizi zaman alır, insan hatası riski var

### Bölüm 2 — Kullanılan Teknolojiler (2 dakika)
- **Yapay Zeka:** TensorFlow / Keras — MobileNetV2 Transfer Learning
- **Backend:** Python / Flask — REST API
- **Frontend:** HTML / CSS / JavaScript
- **Veritabanı:** PostgreSQL — hasta ve teşhis kayıtları
- **Raporlama:** ReportLab — otomatik PDF üretimi
- **Versiyon Kontrolü:** GitHub — 5 kişilik ekip iş birliği

### Bölüm 3 — Sistem Mimarisi (2 dakika)
```
Kullanıcı (Tarayıcı)
        ↓
   Flask API (app.py)
        ↓
  Görüntü Ön İşleme (preprocess.py)
  224×224 RGB, Normalize
        ↓
  MobileNetV2 Modeli (model.py)
  → Normal / Pnömoni / Tüberküloz
        ↓
  PostgreSQL (db_manager.py)   +   PDF Rapor (generate_report.py)
        ↓
  Kullanıcıya Sonuç + İndirilebilir Rapor
```

### Bölüm 4 — Model Performansı (2 dakika)
| Aşama | Doğruluk |
|---|---|
| Eğitim | %97.24 |
| Doğrulama | %94.09 |
| **Test** | **%86.19** |

- Macro F1: %82.81
- En iyi sınıf: Tüberküloz (Precision: %92.0)
- İyileştirme alanı: Pnömoni (Precision: %73.4)

### Bölüm 5 — Ekip Görev Dağılımı (1 dakika)
| Kişi | Görev |
|---|---|
| Süleyman Kılınç | Scrum Master, sistem entegrasyonu, veri ön işleme |
| Ömer Ensar Şahin | AI model geliştirme, config yönetimi |
| Cumali Bilgiç | Model değerlendirme (evaluate.py), metrikler |
| Esmanur Yılmaz | PostgreSQL veritabanı tasarımı ve entegrasyonu |
| Zeynep Karataş | PDF raporlama modülü, performans analizi |

### Bölüm 6 — Canlı Demo (5 dakika)
*(Bkz. demo_akisi.md)*

### Bölüm 7 — Kapanış (1 dakika)
> *"Sistemimiz şu an lokal ortamda tam çalışır durumda. Aynı ağa bağlı herhangi bir cihazdan tarayıcıyla erişilebilir. Modelimiz %86.19 test doğruluğuyla literatürdeki benzer çalışmalarla rekabet eder düzeydedir. Sorularınızı bekliyorum. Teşekkürler."*

---

## 3. Genel Sunum İpuçları

- ✅ Demo öncesi sistemi **çalıştır ve hazır tut** (`python app.py`)
- ✅ Model dosyası zaten indirilmişse Drive'dan tekrar indirmez, hızlı açılır
- ✅ PostgreSQL servisi çalışıyor mu kontrol et
- ✅ Bir test röntgen görüntüsünü masaüstüne hazır koy
- ⚠️ Wi-Fi yavaşsa demo üzerinden değil, ekran kaydıyla göster
- ⚠️ Teknik soru gelirse "evet, bunu test_senaryolari.md'de belgeledik" de

---

*Hazırlayan: Süleyman Kılınç — Hafta 6 Sunum Görevi*
