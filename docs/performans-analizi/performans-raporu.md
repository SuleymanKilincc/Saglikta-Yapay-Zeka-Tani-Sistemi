# Performans Analizi ve Iyilestirme Onerileri

## Gorev Bilgisi

- Sorumlu: Zeynep Karatas
- Hafta: 5
- Gorev: Yapay zeka modelinin hiz, dogruluk ve genel verimlilik acisindan analiz edilmesi; iyilestirme alanlarinin belirlenmesi.

## Mevcut Model Ozeti

Projede gogus rontgeni goruntulerini Normal, Pnomoni ve Tuberkuloz siniflarina ayirmak icin MobileNetV2 tabanli transfer learning mimarisi kullanilmistir. Model, web uygulamasinda yuklenen goruntuyu on isleme adimindan gecirdikten sonra teshis sonucunu ve guven skorunu uretir. Bu sonuc PDF raporlama modulu ve veritabani kaydi ile birlikte kullaniciya sunulur.

README dosyasinda paylasilan referans sonuclara gore modelin temel metrikleri asagidaki gibidir:

| Metrik | Deger |
|---|---:|
| Egitim dogrulugu | %97.24 |
| Dogrulama dogrulugu | %94.09 |
| Test dogrulugu | %86.19 |
| Model mimarisi | MobileNetV2 Transfer Learning |
| Giris boyutu | 224 x 224 RGB |
| Sinif sayisi | 3 |

## Dogruluk Analizi

Egitim ve dogrulama dogruluklari yuksek seviyededir. Ancak test dogrulugunun dogrulama dogrulugundan daha dusuk olmasi, modelin gercek hayattaki farkli rontgen kalitelerine ve veri dagilimina karsi daha dikkatli izlenmesi gerektigini gosterir. Bu fark, veri seti dengesizligi, goruntu kalitesi farklari veya egitim verisine fazla uyum gibi nedenlerden kaynaklanabilir.

Modelin sinif bazli davranisini netlestirmek icin `ai_model/evaluate.py` dosyasinda accuracy, precision, recall, F1-score ve confusion matrix ureten degerlendirme akisi bulunmaktadir. Bu akisin model dosyasi ve test veri seti hazir oldugunda calistirilmasi, hangi hastalik siniflarinda karisma oldugunu gormek icin yeterlidir.

## Hiz ve Verimlilik Analizi

MobileNetV2 hafif ve verimli bir CNN mimarisi oldugu icin web tabanli kullanim icin uygundur. Tek rontgen goruntusu uzerinde tahmin akisi genel olarak su adimlardan olusur:

1. Goruntunun yuklenmesi ve guvenli dosya adi ile kaydedilmesi.
2. Goruntunun 224 x 224 boyutuna getirilmesi ve normalize edilmesi.
3. Model tahmininin alinmasi.
4. Sonucun veritabanina kaydedilmesi.
5. PDF raporunun uretilmesi.

Bu akis icinde en fazla sure tuketebilecek noktalar modelin ilk yuklenmesi, buyuk goruntu dosyalarinin islenmesi ve PDF rapor olusturma adimidir. Modelin her tahminde tekrar yuklenmesi yerine uygulama baslangicinda bir kez yuklenip bellekten kullanilmasi performansi belirgin sekilde artirabilir.

## Guclu Yonler

- Transfer learning kullanimi kucuk ve orta olcekli tibbi veri setlerinde daha dengeli sonuc almayi kolaylastirir.
- MobileNetV2 mimarisi hiz ve dogruluk arasinda iyi bir denge sunar.
- Tahmin sonucu guven skoru ile birlikte rapora aktarildigi icin doktorun yorumu desteklenir.
- PDF raporlama ve veritabani kaydi ile model ciktisi kalici hale getirilmistir.
- Demo modu, model dosyasi bulunmadiginda uygulamanin tamamen durmasini engeller.

## Zayif Yonler ve Riskler

- Test dogrulugunun dogrulama dogrulugundan dusuk olmasi genelleme riskine isaret eder.
- Veri seti sinif dagilimi dengesizse az temsil edilen hastaliklarda recall degeri dusuk kalabilir.
- Guven skoru tek basina klinik karar icin yeterli degildir; doktor onayi zorunlu tutulmalidir.
- Model dosyasinin dis kaynaktan indirilmesi ilk calistirmada gecikmeye neden olabilir.
- Uygulama tarafinda uretilen rapor dosyalari duzenli temizlenmezse depolama alani gereksiz buyuyebilir.

## Iyilestirme Onerileri

| Alan | Oneri | Beklenen Katki |
|---|---|---|
| Veri kalitesi | Dusuk kaliteli ve hatali etiketli goruntuler ayiklanmali | Daha guvenilir egitim |
| Veri dengesi | Normal, Pnomoni ve Tuberkuloz siniflari dengeli hale getirilmeli | Sinif bazli performans artisi |
| Veri artirma | Rotation, zoom, brightness ve contrast augmentation uygulanmali | Gercek dunya goruntulerine dayaniklilik |
| Model izleme | Confusion matrix ve F1-score her egitimden sonra kaydedilmeli | Zayif siniflarin erken tespiti |
| Performans | Model uygulama baslangicinda tek kez yuklenmeli | Daha hizli tahmin |
| Raporlama | Raporlara model surumu ve analiz tarihi eklenmeli | Izlenebilirlik |
| Guvenlik | Yuklenen dosya tipi ve boyutu daha siki dogrulanmali | Kullanim guvenligi |

## Sonuc

Model mevcut haliyle akademik bir tani destek sistemi icin yeterli bir prototip seviyesindedir. En onemli gelistirme alani, test performansinin sinif bazinda daha detayli izlenmesi ve gercek hayattaki farkli rontgen kalitelerine karsi dayanimin artirilmasidir. Raporlama sistemi ile model ciktisinin PDF olarak saklanmasi proje teslimi acisindan guclu bir tamamlayici katman olusturmaktadir.
