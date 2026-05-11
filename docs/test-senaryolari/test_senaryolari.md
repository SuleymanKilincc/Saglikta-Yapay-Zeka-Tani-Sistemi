# Algoritma Optimizasyonu ve Test Senaryoları

## Görev Bilgisi
- **Sorumlu:** Süleyman Kılınç
- **Hafta:** 5
- **Görev:** Mevcut yapay zeka algoritmalarının performansını artırmak için test senaryoları geliştirmek ve optimizasyon önerileri sunmak.
- **Tarih:** 11.05.2026

---

## 1. Test Ortamı

| Parametre | Değer |
|---|---|
| Model | MobileNetV2 Transfer Learning |
| Framework | TensorFlow / Keras |
| Giriş Boyutu | 224 × 224 × 3 (RGB) |
| Sınıf Sayısı | 3 (Normal, Pnömoni, Tüberküloz) |
| Epoch | 20 |
| Batch Size | 32 |
| Learning Rate | 0.0001 (Adam) |
| Dropout | 0.5 |

---

## 2. Test Senaryoları

### Senaryo 1 — Normal Akciğer Testi
**Amaç:** Sistemin sağlıklı akciğer görüntüsünü doğru sınıflandırıp sınıflandıramadığını doğrulamak.

| Adım | Açıklama |
|---|---|
| Girdi | Normal (sağlıklı) akciğer X-Ray görüntüsü |
| Beklenen Çıktı | Sınıf: Normal, Güven Skoru ≥ %70 |
| Test Edilen Metrik | Precision: %84.5, Recall: %87.0, F1: %85.7 |
| Sonuç | ✅ Başarılı |

**Gözlem:** Normal sınıfı en yüksek recall değerine sahiptir (%87.0), yani sistem sağlıklı hastaları büyük ölçüde doğru tespit etmektedir. Bu kritik öneme sahiptir — hasta olmayan kişiye yanlış tanı konulmamalıdır.

---

### Senaryo 2 — Pnömoni (Zatürre) Testi
**Amaç:** Sistemin pnömoni bulgularını doğru tespit edip edemediğini doğrulamak.

| Adım | Açıklama |
|---|---|
| Girdi | Pnömoni bulgulu akciğer X-Ray görüntüsü |
| Beklenen Çıktı | Sınıf: Pnömoni, Güven Skoru ≥ %60 |
| Test Edilen Metrik | Precision: %73.4, Recall: %80.0, F1: %76.6 |
| Sonuç | ⚠️ Kısmen Başarılı |

**Gözlem:** Pnömoni sınıfı en düşük precision değerine sahiptir (%73.4). Bu, bazı Normal veya Tüberküloz görüntülerinin Pnömoni olarak yanlış sınıflandırıldığını göstermektedir. Pnömoni ve Tüberküloz görüntüleri zaman zaman benzer radyolojik bulgular sergilemektedir.

---

### Senaryo 3 — Tüberküloz (Verem) Testi
**Amaç:** Sistemin tüberküloz bulgularını tespit edip edemediğini doğrulamak.

| Adım | Açıklama |
|---|---|
| Girdi | Tüberküloz bulgulu akciğer X-Ray görüntüsü |
| Beklenen Çıktı | Sınıf: Tüberküloz, Güven Skoru ≥ %60 |
| Test Edilen Metrik | Precision: %92.0, Recall: %81.0, F1: %86.2 |
| Sonuç | ✅ Başarılı |

**Gözlem:** Tüberküloz sınıfı en yüksek precision değerine sahiptir (%92.0). Sistem Tüberküloz dediğinde büyük olasılıkla doğrudur. Ancak recall %81.0 olduğu için bazı Tüberküloz vakaları kaçırılmaktadır.

---

### Senaryo 4 — Bozuk / Geçersiz Görüntü Testi
**Amaç:** Sisteme geçersiz dosya gönderildiğinde nasıl davrandığını test etmek.

| Adım | Açıklama |
|---|---|
| Girdi | PDF, TXT veya bozuk resim dosyası |
| Beklenen Çıktı | Hata mesajı: "Görüntü okunamadı" |
| Gerçek Çıktı | `goruntu_hazirla()` → None döner → API hata mesajı verir |
| Sonuç | ✅ Başarılı |

---

### Senaryo 5 — Farklı Görüntü Boyutu Testi
**Amaç:** Farklı çözünürlükteki görüntülerin işlenip işlenemediğini test etmek.

| Girdi Boyutu | İşlem | Sonuç |
|---|---|---|
| 512 × 512 | OpenCV ile 224×224'e küçültülür | ✅ Çalışır |
| 2000 × 1500 | OpenCV ile 224×224'e küçültülür | ✅ Çalışır |
| 100 × 100 | OpenCV ile 224×224'e büyütülür | ✅ Çalışır |
| 50 × 50 | İşlenir ancak kalite düşer | ⚠️ Düşük güvenilirlik |

---

### Senaryo 6 — Aynı Anda Birden Fazla İstek (Yük Testi)
**Amaç:** Sistemin eş zamanlı isteklerde kararlı çalışıp çalışmadığını test etmek.

| Eş Zamanlı İstek | Sonuç |
|---|---|
| 1 istek | ✅ ~2-3 saniye (model ilk yüklemede) |
| 1 istek (önbellek) | ✅ ~0.5-1 saniye |
| 3 eş zamanlı istek | ⚠️ Flask tek iş parçacıklı olduğundan sıralı işler |

**Not:** Flask geliştirme sunucusu tek iş parçacıklıdır. Üretim ortamında Gunicorn kullanılmalıdır.

---

## 3. Genel Performans Sonuçları

| Metrik | Değer |
|---|---|
| Test Doğruluğu (Accuracy) | **%86.19** |
| Makro F1 Skoru | **%82.81** |
| Makro AUC | **%75.02** |

### Sınıf Bazında Detay

| Sınıf | Precision | Recall | F1 | AUC |
|---|---|---|---|---|
| Normal | %84.5 | %87.0 | %85.7 | %77.1 |
| Pnömoni | %73.4 | %80.0 | %76.6 | %74.3 |
| **Tüberküloz** | **%92.0** | %81.0 | %86.2 | %72.5 |

---

## 4. Tespit Edilen Sorunlar

### 4.1 Pnömoni Sınıfında Düşük Precision
- **Sorun:** %73.4 precision → sistem bazen diğer sınıfları Pnömoni olarak yanlış etiketliyor
- **Muhtemel Neden:** Pnömoni ve Tüberküloz radyolojik görüntüleri benzer infiltrasyon (beyazlık) bulguları gösterebilir
- **Etki:** Yanlış pozitif tanı → hastada gereksiz kaygı

### 4.2 Tüberküloz Sınıfında Düşük Recall
- **Sorun:** %81.0 recall → 100 Tüberküloz vakasından ~19'u kaçırılıyor
- **Muhtemel Neden:** Veri setinde Tüberküloz görüntü sayısı diğer sınıflara göre az olabilir (sınıf dengesizliği)
- **Etki:** Yanlış negatif tanı → hasta gerçekte Tüberkülozlu ama sistem Normal diyor

### 4.3 Eğitim / Test Doğruluğu Farkı
- Eğitim: %97.24 → Test: %86.19 → **~11 puanlık düşüş**
- Bu fark overfitting riski olmakla birlikte, Dropout(0.5) ve 20 epoch ile kontrol altında tutulmuştur
- Eğitim ve doğrulama eğrileri yakın seyrettiğinden ciddi overfitting yoktur

---

## 5. Optimizasyon Önerileri

| Öncelik | Öneri | Beklenen Kazanım |
|---|---|---|
| 🔴 Yüksek | Veri artırma (augmentation) genişletmek — özellikle Pnömoni sınıfı için | Precision +5% |
| 🔴 Yüksek | Sınıf ağırlıklandırması (`class_weight`) eklemek | Dengeli F1 skoru |
| 🟡 Orta | Fine-tuning: MobileNetV2'nin son 20 katmanını açmak | Accuracy +3-5% |
| 🟡 Orta | Learning Rate Scheduler eklemek (azalan LR) | Daha stabil eğitim |
| 🟢 Düşük | Daha büyük Dense katmanı (256 nöron) denemek | Marginal iyileşme |
| 🟢 Düşük | EfficientNetB0 mimarisi ile karşılaştırma yapmak | Referans değer |

### Uygulama Kolaylığı Açısından İlk 2 Öneri:

```python
# 1. Sınıf Ağırlıklandırması (class_weight) — config.py'e eklenebilir
CLASS_WEIGHTS = {
    0: 1.0,   # Normal
    1: 1.3,   # Pnömoni (az precision nedeniyle ağırlık artırıldı)
    2: 1.2,   # Tüberküloz (düşük recall nedeniyle ağırlık artırıldı)
}

# 2. Learning Rate Scheduler
from tensorflow.keras.callbacks import ReduceLROnPlateau
lr_scheduler = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.5,       # LR'yi yarıya indir
    patience=3,       # 3 epoch iyileşme yoksa tetikle
    min_lr=1e-6
)
```

---

## 6. Sonuç

Sistem mevcut haliyle **%86.19 test doğruluğu** ile literatürdeki benzer çalışmalarla rekabet edebilir düzeydedir. Transfer Learning yaklaşımı sınırlı veriyle güçlü sonuçlar üretmiştir.

Kısa vadede uygulanabilecek en etkili iyileştirme **sınıf ağırlıklandırması** ve **veri artırmadır.** Bu değişiklikler mevcut mimari değiştirilmeden yapılabilir ve test doğruluğunun **%88-90** bandına taşınması beklenmektedir.

---

*Hazırlayan: Süleyman Kılınç*  
*Tarih: 11.05.2026*  
*Modül: Algoritma Optimizasyonu ve Test Senaryoları — Hafta 5*
