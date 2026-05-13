# Veri Ön İşleme Raporu

Bu rapor, "Sağlıkta Yapay Zeka Destekli Tanı Sistemi" projesi kapsamında kullanılan veri ön işleme tekniklerini ve bu süreçlerin teknik detaylarını içermektedir. Yapay zeka modelinin başarısı, girdi verilerinin kalitesine ve standart bir formatta olmasına doğrudan bağlıdır.

## 1. Görüntü Formatı ve Renk Dönüşümü (RGB/Grayscale)
Tıbbi görüntüler (Röntgen, MR vb.) genellikle yüksek çözünürlüklü ve farklı renk derinliklerine sahip olabilir. Projemizde:
*   **İşlem:** Görüntüler `cv2.imread(path, cv2.IMREAD_GRAYSCALE)` komutu kullanılarak okunmaktadır.
*   **Neden:** Tıbbi tanıda renk bilgisi genellikle tanısal bir değer taşımaz; doku yoğunluğu ve yapısal formlar gri tonlarda daha net analiz edilebilir. Ayrıca, tek kanal (grayscale) kullanımı modelin parametre sayısını azaltarak eğitim sürecini hızlandırır.
*   **RGB Notu:** Eğer kaynak görüntüler RGB formatındaysa, bunlar işleme aşamasında gri tonlamaya çevrilerek veri boyutundan tasarruf sağlanır ve modelin odak noktası doku anomalilerine yönlendirilir.

## 2. Boyutlandırma (Resize) İşlemi
Farklı cihazlardan gelen tıbbi görüntüler çok farklı çözünürlüklerde (2000x2000, 1024x768 vb.) olabilir. Sinir ağlarının sabit bir giriş boyutu beklemesi nedeniyle:
*   **İşlem:** Tüm görüntüler **224x224 piksel** boyutuna getirilmektedir.
*   **Yöntem:** OpenCV kütüphanesinin `cv2.resize()` fonksiyonu kullanılarak inter-area interpolasyon yöntemiyle boyut küçültme yapılır.
*   **Sonuç:** Bu standartlaştırma, modelin her görüntüde aynı ölçekteki özellikleri öğrenmesini sağlar.

## 3. Normalizasyon (0-1 Aralığı)
Görüntü pikselleri standart olarak 0 ile 255 (8-bit) arasında değerler alır. Ancak yapay zeka modelleri, aktivasyon fonksiyonlarının (ReLU, Softmax vb.) daha verimli çalışması için daha küçük sayısal aralıkları tercih eder.
*   **İşlem:** Piksel değerleri 255.0'a bölünerek **[0, 1]** aralığına sıkıştırılır.
*   **Neden:**
    *   Gradyanların (gradients) daha dengeli dağılmasını sağlar.
    *   Modelin daha hızlı yakınsamasını (convergence) sağlar.
    *   Aşırı büyük sayısal değerlerin neden olabileceği hesaplama hatalarını önler.

## 4. Model Formatına Hazırlık
Son aşamada, işlenen görüntü `np.expand_dims(resim, axis=0)` ile `(224, 224, 1)` boyutuna getirilir. Bu, modelin beklediği "kanal" boyutunu ekler ve veriyi eğitim için hazır hale getirir.

---
**Dosya:** `data_processing/preprocess.py`  
**Hazırlayan:** Ömer Ensar Şahin  
**Tarih:** 10.05.2026
