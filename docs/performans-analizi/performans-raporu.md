# Performans Raporu

## Gorev Bilgisi

- Sorumlu: Zeynep Karatas
- Hafta: 5
- Incelenen grafik: `ai_model/training_history.png`
- Teslim klasoru: `docs/performans-analizi/`

## Kullanilan Performans Degerleri

Model egitimi MobileNetV2 tabanli transfer learning mimarisi ile yapilandirilmistir. Projede paylasilan referans sonuclara gore egitim dogrulugu %97.24, dogrulama dogrulugu %94.09 ve test dogrulugu %86.19 seviyesindedir. `training_history.png` grafigi bu egitim surecinin accuracy ve loss egilimlerini gostermek icin hazirlanmistir.

| Metrik | Deger |
|---|---:|
| Egitim dogrulugu | %97.24 |
| Dogrulama dogrulugu | %94.09 |
| Test dogrulugu | %86.19 |
| Epoch sayisi | 20 |

## En Iyi Sonuc Kacinci Epoch'ta Alindi?

Grafikte dogrulama dogrulugunun en iyi seviyeye egitimin son bolumunde ulastigi gorulmektedir. En iyi dogrulama sonucu 20. epoch civarinda alinmistir. Bu noktada egitim dogrulugu %97.24, dogrulama dogrulugu ise %94.09 seviyesindedir.

## Egitim ve Dogrulama Egrileri Nasil?

Egitim dogrulugu epoch ilerledikce duzenli olarak artmistir. Dogrulama dogrulugu da benzer sekilde yukselen bir egilim gostermistir; ancak egitim dogrulugunun biraz altinda kalmistir. Iki egri arasindaki fark cok acilmadigi icin agir overfitting belirtisi yoktur. Loss grafiginde hem egitim hem dogrulama kaybinin zamanla azaldigi gorulmektedir. Bu durum modelin egitim boyunca daha kararlı tahminler yapmaya basladigini gosterir.

Test dogrulugunun dogrulama dogrulugundan dusuk olmasi, modelin farkli kaynaklardan gelen rontgenlerde daha fazla veriyle desteklenmesi gerektigini gosterir.

## Iyilestirme Onerileri

| Oneri | Beklenen Katki |
|---|---|
| Daha fazla Normal, Pnomoni ve Tuberkuloz goruntusu eklemek | Test dogrulugunu ve genelleme gucunu artirir |
| Sinif dengesini kontrol etmek | Az temsil edilen siniflarda recall degerini iyilestirir |
| Veri artirma yontemlerini genisletmek | Farkli rontgen kalitelerine dayanikliligi artirir |
| MobileNetV2 son katmanlarinda fine-tuning yapmak | Dogrulama ve test performansini artirabilir |
| Confusion matrix'i duzenli incelemek | Hangi hastalik siniflarinin karistigini netlestirir |

## Sonuc

Model, mevcut sonuclara gore proje icin guclu bir tani destek prototipi sunmaktadir. En iyi performans 20. epoch civarinda alinmistir. Egitim ve dogrulama egrileri genel olarak uyumludur; ancak test dogrulugunu artirmak icin daha fazla veri, sinif dengesi kontrolu, veri artirma ve fine-tuning onerilmektedir.
