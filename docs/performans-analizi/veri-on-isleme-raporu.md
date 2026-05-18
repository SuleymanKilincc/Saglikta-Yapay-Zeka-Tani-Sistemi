# Veri Ön İşleme Raporu

Bu rapor, "Sağlıkta Yapay Zeka Destekli Tanı Sistemi" projesi kapsamında kullanılan veri ön işleme tekniklerini ve bu süreçlerin teknik detaylarını içermektedir. Yapay zeka modelinin başarısı, girdi verilerinin kalitesine ve standart bir formatta olmasına doğrudan bağlıdır.

## 1. Görüntü Formatı ve Renk Dönüşümü (RGB/Grayscale)
Tıbbi görüntüler (Röntgen, MR vb.) genellikle yüksek çözünürlüklü ve farklı renk derinliklerine sahip olabilir. Projemizde:
*   **İşlem:** Görüntüler `cv2.imread(path, cv2.IMREAD_COLOR)` komutu kullanılarak RGB formatında okunmaktadır.
*   **Neden:** MobileNetV2 ve benzeri önceden eğitilmiş (pre-trained) derin öğrenme modelleri 3 kanallı (RGB) giriş resimleri bekler. Bu nedenle, tıbbi görüntüler gri tonlamalı (röntgen vb.) bile olsa, modelin giriş katmanıyla uyumlu olması için 3 kanallı olarak okunur.
*   **Grayscale Notu:** Eğer orijinal görüntü siyah-beyaz ise, OpenCV bunu 3 kanala kopyalayarak RGB formatına dönüştürür.

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
Son aşamada, işlenen görüntü `np.expand_dims(resim, axis=0)` ile boyutlandırılarak modelin beklediği batch boyutuna uygun hale getirilir ve tek bir resim `(1, 224, 224, 3)` şeklinde ifade edilir. Burada asıl görüntünün boyutu `(224, 224, 3)`'tür. Bu işlem veriyi eğitim veya tahmin için hazır hale getirir.

---
**Dosya:** `data_processing/preprocess.py`  
**Hazırlayan:** Ömer Ensar Şahin  
**Tarih:** 10.05.2026
