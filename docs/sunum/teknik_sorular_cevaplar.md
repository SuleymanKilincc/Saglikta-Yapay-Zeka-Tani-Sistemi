# Teknik Sorular ve Cevaplar

**Hazırlayan:** Süleyman Kılınç  
**Amaç:** Hoca tarafından sorulabilecek teknik sorulara hazırlıklı olmak  
**Tarih:** 11.05.2026

---

## Model ve Yapay Zeka

**S: Neden MobileNetV2 seçtiniz, başka model denediniz mi?**
> MobileNetV2'yi seçtik çünkü hız ve doğruluk dengesi açısından tıbbi görüntüleme görevleri için uygun bir mimaridir. ImageNet üzerinde önceden eğitilmiş ağırlıkları sayesinde az veriyle güçlü sonuç alınır. ResNet veya EfficientNet gibi alternatifler daha yüksek doğruluk verebilir ancak çok daha fazla hesaplama kaynağı gerektirir. Kısıtlı donanımda çalışacak şekilde optimize edilmesi de bir avantajdır.

---

**S: Transfer Learning nedir, neden kullandınız?**
> Transfer Learning, büyük veri setleri üzerinde eğitilmiş bir modelin öğrendiği özellikleri farklı bir görev için kullanmaktır. Biz ImageNet üzerinde eğitilmiş MobileNetV2'nin özellik çıkarma katmanlarını dondurarak (freeze) üstüne kendi sınıflandırma katmanımızı ekledik. Bu sayede binlerce görüntüyle eğitmek yerine mevcut veriyle yüksek doğruluk elde ettik.

---

**S: %86.19 test doğruluğu yeterli mi?**
> Literatürdeki benzer 3 sınıflı akciğer teşhis çalışmaları %80-90 bandında test doğruluğu raporlamaktadır. Bizim %86.19 değerimiz bu aralığın üst kısmındadır. Ancak tıbbi sistemlerde doğruluk tek başına yeterli değildir; recall (geri çağırma) daha kritiktir. Hasta olan birini kaçırmamak için Pnömoni ve Tüberküloz recall değerlerimiz %80+ seviyesindedir. Sistem kesin tanı aracı değil, **karar destek sistemi** olarak tasarlanmıştır.

---

**S: Overfitting var mı? Nasıl önlediniz?**
> Eğitim doğruluğu %97.24, test doğruluğu %86.19 — aradaki ~11 puanlık fark overfitting belirtisi olabilir. Ancak eğitim ve doğrulama eğrilerinin yakın seyretmesi ciddi overfitting olmadığını göstermektedir. Önlemler: Dropout(0.5) katmanı ekledik, veri artırma (rotation, flip, zoom) uyguladık, base modeli dondurarak gereksiz parametre öğrenimini önledik.

---

**S: Confusion Matrix'te hangi sınıf karışıyor?**
> En çok karışan sınıf Pnömonidir. Precision değeri %73.4 olduğundan bazı Normal ve Tüberküloz görüntüleri Pnömoni olarak etiketleniyor. Bu, tıbbi literatürde de bilinen bir sorundur — Pnömoni ve Tüberküloz radyolojik olarak benzer infiltrasyon bulguları gösterebilir.

---

## Sistem Mimarisi

**S: Neden Flask kullandınız, Django değil mi?**
> Flask mikro-çerçevedir, yani yalnızca ihtiyacımız olan bileşenleri kullanırız. Projemiz tek endpoint'li basit bir API olduğu için Flask'ın sadeliği avantajlıdır. Django daha büyük, çok sayfalı web uygulamaları için uygundur; bizim gibi model servis eden API'ler için Flask daha yaygın tercih edilir.

---

**S: Neden PostgreSQL, SQLite yetmez miydi?**
> SQLite dosya tabanlı bir veritabanıdır ve tek kullanıcı için yeterlidir. Ancak PostgreSQL ile birden fazla eş zamanlı bağlantı, ACID uyumluluğu ve ileri ölçeklenebilirlik sağlanır. Gerçek hastane ortamında aynı anda birden fazla doktorun sistemi kullanacağını göz önünde bulundurarak PostgreSQL seçtik.

---

**S: Hasta verisi güvenli mi?**
> Evet. Gerçek TC Kimlik No kullanılmıyor — sistem otomatik anonimleştirilmiş bir ID üretiyor. `.env` dosyasıyla veritabanı şifresi kaynak koddan ayrıldı. `.gitignore` ile gizli bilgiler repoya gönderilmiyor. Üretim ortamında HTTPS ve kimlik doğrulama katmanı eklenmesi gerekir.

---

**S: Sistem nasıl ölçeklenebilir?**
> Şu an Flask geliştirme sunucusuyla çalışıyor. Üretim için Gunicorn (çok iş parçacıklı) ve Nginx (reverse proxy) kullanılabilir. Model inferansı GPU ile hızlandırılabilir. Docker ile konteynerize edilerek bulut ortamına taşınabilir.

---

## Veri Seti

**S: Hangi veri setini kullandınız?**
> Kaggle'dan alınan akciğer röntgeni veri setini kullandık. Normal, Pneumonia (Pnömoni) ve Tuberculosis (Tüberküloz) sınıflarını içermektedir. Eğitim/doğrulama/test ayrımı yapılarak modelin gerçek performansı ölçüldü.

---

**S: Veri seti dengeli miydi?**
> Hayır, tıbbi veri setlerinde sınıf dengesizliği yaygın bir sorundur. Pnömoni sınıfının düşük precision değeri (%73.4) kısmen bu dengesizlikten kaynaklanıyor olabilir. İyileştirme olarak `class_weight` parametresiyle sınıf ağırlıklandırması uygulanabilir.

---

## Geliştirme Süreci

**S: Ekip olarak nasıl çalıştınız?**
> GitHub üzerinden Git Flow benzeri bir süreç izledik. Her ekip üyesi kendi branch'inde çalıştı ve Pull Request açarak code review sürecinden geçti. Haftalık görev takibi yapıldı. Toplam 150+ commit ve birden fazla PR ile sürüm kontrolü sağlandı.

---

**S: En büyük teknik zorluğunuz ne oldu?**
> En büyük zorluk TensorFlow modelinin bellek tüketimiydi. Railway (bulut sunucusu) ücretsiz planında RAM yetersizliği nedeniyle OOM (Out of Memory) hatası aldık. Bu nedenle sistemi lokal öncelikli olarak yapılandırdık. Ayrıca farklı işletim sistemlerinde `opencv` ve `tensorflow` uyumluluk sorunları yaşandı.

---

*Hazırlayan: Süleyman Kılınç — Hafta 6 Sunum Görevi*
