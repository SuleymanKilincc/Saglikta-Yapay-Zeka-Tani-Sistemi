# Canlı Demo Akışı

**Hazırlayan:** Süleyman Kılınç  
**Amaç:** Sunum sırasında sistemi akıcı ve profesyonel göstermek  
**Süre:** ~5 dakika

---

## Demo Öncesi Hazırlık (Sunum salonuna girmeden önce)

- [ ] `python app.py` komutuyla sistemi başlat
- [ ] `http://127.0.0.1:5000` adresinin açıldığını kontrol et
- [ ] PostgreSQL servisinin çalıştığını kontrol et
- [ ] Test röntgen görüntüsünü masaüstüne hazırla (JPG/PNG)
- [ ] Tarayıcı sekmesini tam ekran yap

---

## Demo Adımları

### Adım 1 — Sistemi Tanıt (30 saniye)
> *"Şu an ekranınızda gördüğünüz, sistemimizin web arayüzüdür. Sol tarafta hasta kayıt formu, sağ tarafta analiz sonuçları gösterilecek."*

- Sayfayı kaydırarak forma göster
- Sağ alttaki **3 Hastalık Sınıfı | %94 Model Doğruluğu | MobileNetV2** istatistiklerini göster

---

### Adım 2 — Hasta Bilgilerini Gir (45 saniye)
> *"Önce hasta bilgilerini giriyoruz."*

| Alan | Girilecek Değer |
|---|---|
| Ad | Ahmet |
| Soyad | Yılmaz |
| Doğum Tarihi | 1975-03-20 |
| Cinsiyet | Erkek |
| Doktor Adı | Dr. Mehmet Demir |
| Departman | Göğüs Hastalıkları |

---

### Adım 3 — Röntgen Görüntüsü Yükle (30 saniye)
> *"Şimdi hastanın röntgen görüntüsünü yüklüyoruz. Sistem JPG, PNG ve DICOM formatlarını destekliyor."*

- Upload alanına tıkla veya görüntüyü sürükle-bırak
- Yeşil çerçeve ve dosya adının göründüğünü belirt
- **"Analiz Et"** butonu aktif hale gelir

---

### Adım 4 — Analizi Başlat (60 saniye)
> *"Analiz Et butonuna basıyorum. Sistem görüntüyü işliyor..."*

- Yükleme animasyonu göster:
  - "Görüntü hazırlanıyor..."
  - "AI analizi yapılıyor..."
  - "Rapor oluşturuluyor..."

> *"Sistem 3 aşamadan geçiyor: önce görüntü 224×224 boyutuna getiriliyor ve normalize ediliyor, ardından MobileNetV2 modelimiz tahmin yapıyor, son olarak PDF raporu oluşturuluyor."*

---

### Adım 5 — Sonucu Göster (60 saniye)
> *"Sonuç geldi. Sistem [Pnömoni/Normal/Tüberküloz] teşhisi koydu, güven skoru %XX."*

- Teşhis sonucunu oku
- Güven skorunu belirt
- Risk durumunu (Yüksek Risk / Sağlıklı) göster

> *"Sağ panelde tüm olasılıklar gösteriliyor. Model her sınıf için ayrı bir olasılık üretiyor."*

---

### Adım 6 — PDF Raporu İndir (30 saniye)
> *"Sistem otomatik olarak PDF raporu oluşturdu. Raporun içeriğine bakalım."*

- **"Raporu İndir"** butonuna tıkla
- PDF'i aç, içeriğini göster:
  - Hasta adı, doktor, departman
  - Teşhis ve güven skoru
  - Risk durumu (renkli)
  - AI uyarı notu

> *"Bu rapor hastanın dosyasına eklenebilir ya da doktora iletilebilir."*

---

### Adım 7 — Veritabanını Göster (opsiyonel, 30 saniye)
> *"Yapılan her analiz PostgreSQL veritabanımıza kaydediliyor."*

- pgAdmin'i açıp `SELECT * FROM patients` sorgusunu çalıştır
- Az önce girilen kaydın eklendiğini göster

---

## B Planı — Sorun Çıkarsa

| Sorun | Çözüm |
|---|---|
| Model indirme yavaş | Önceden indirilmiş modeli kullan, Drive'a bağlanma |
| PostgreSQL bağlanamıyor | Demo modunda çalıştır — sadece AI sonucu göster |
| Internet yok | Localhost çalışır, internet gerekmez |
| Görüntü yüklenmiyor | Farklı format dene (JPG → PNG) |
| Sayfa açılmıyor | `python app.py` tekrar çalıştır |

---

*Hazırlayan: Süleyman Kılınç — Hafta 6 Sunum Görevi*
