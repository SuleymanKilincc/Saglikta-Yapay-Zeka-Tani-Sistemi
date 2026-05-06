# Veri Seti Incelemesi ve On Isleme Planlamasi

## Gorev Bilgisi

- Sorumlu: Zeynep Karatas
- Hafta: 1
- Gorev: Kullanilacak tibbi veri setlerini incelemek, veri kalitesini degerlendirmek ve on isleme adimlarini planlamak.

## Veri Seti Kapsami

Proje, gogus rontgeni goruntuleri uzerinden Normal, Pnomoni ve Tuberkuloz siniflari icin tani destek ciktisi uretmeyi hedefler.

| Kontrol Alani | Beklenen Durum | Not |
|---|---|---|
| Goruntu formati | JPG, JPEG veya PNG | Web arayuzu bu formatlari kabul edecek sekilde tasarlanmistir. |
| Sinif klasorleri | Normal, Pneumonia, Tuberculosis | Egitim ve test ayrimi sinif bazinda korunmalidir. |
| Etiket kalitesi | Dogru ve tutarli etiketleme | Yanlis etiketler model performansini dogrudan dusurur. |
| Goruntu kalitesi | Okunabilir, bozulmamis rontgen | Cok dusuk kontrastli veya hatali dosyalar ayiklanmalidir. |
| Veri dengesi | Siniflar arasi makul dagilim | Dengesizlik varsa augmentation veya class weight kullanilmalidir. |

## Kalite Degerlendirme Kriterleri

1. Dosya acilabilirligi kontrol edilir.
2. Goruntunun tekil rontgen karesi icerip icermedigi incelenir.
3. Cok kucuk, bozuk veya bos goruntuler ayrilir.
4. Sinif dagilimi sayisal olarak kontrol edilir.
5. Egitim, dogrulama ve test verileri birbirine karismayacak sekilde ayrilir.

## On Isleme Plani

| Adim | Aciklama | Amac |
|---|---|---|
| Dosya dogrulama | Gecerli uzanti ve okunabilirlik kontrolu | Hatali girdileri engellemek |
| Yeniden boyutlandirma | Goruntuyu 224 x 224 boyutuna getirmek | Model girisini standartlastirmak |
| Kanal uyumu | Gri tonlama veya RGB formatini modele uygun hale getirmek | Tahmin hatalarini azaltmak |
| Normalizasyon | Piksel degerlerini 0-1 araligina cekmek | Egitimi ve tahmini kararli yapmak |
| Veri artirma | Donme, yakinlastirma, parlaklik/kontrast degisimi | Modelin farkli rontgen kosullarina dayanimini artirmak |

## Riskler ve Onlemler

- Veri seti dengesizse model cogunluk sinifina egilim gosterebilir. Bu durumda sinif agirliklari veya veri artirma uygulanmalidir.
- Dusuk kaliteli rontgenler yanlis tani riskini artirabilir. Kalite kontrol listesi egitimden once calistirilmalidir.
- Test verisi egitim verisine karisirsa performans yapay olarak yuksek gorunur. Ayrim klasor yapisi korunmalidir.

## Sonuc

Hafta 1 kapsaminda veri seti icin kalite kontrol kriterleri, on isleme akisi ve risk yonetimi planlanmistir. Bu plan, `data_processing/preprocess.py` dosyasindaki goruntu hazirlama akisi ve `ai_model/` altindaki model egitim dosyalari ile uyumludur.
