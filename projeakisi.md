Sağlıkta Yapay Zeka - Proje Akışı ve Haftalık İlerleme
Bu dosya, Sağlıkta Yapay Zeka takımının haftalık proje ilerlemesini ve üyelerin görev dağılımları sonucunda elde ettikleri çıktıları içermektedir.

1. Hafta (6 - 12 Mart)
Süleyman Kılınç (Scrum Master / Yönetici): GitHub reposu kuruldu ve koruma ayarları yapıldı. Proje Kapsamı Belirlendi: Sistem, akciğer röntgenlerinden "Pnömoni (Zatürre)" tespiti yapacaktır. İkili sınıflandırma (Sağlıklı/Hastalıklı) problemi çözülecek olup, model olarak Evrişimli Sinir Ağları (CNN) kullanılacaktır. Veri seti olarak Kaggle "Chest X-Ray Images (Pneumonia)" seçilmiştir.

Ömer Ensar Şahin: Proje için gereksinim analizi tamamlandı. Doktorlar sisteme giriş yapabilecek. MR ve röntgen görüntüleri yüklenecek. Yapay zeka analiz yapacak. Sonuçlar raporlanacak. Model doğruluk hedefi %85. Veri güvenliği KVKK kurallarına uygun olacak.

Cumali Bilgiç: Proje için teknoloji araştırması tamamlandı. Görüntü işleme ve derin öğrenme (CNN) modelleri için yüksek performans sunan TensorFlow/Keras kütüphanesi seçildi. Verilerin düzenli ve güvenli bir şekilde saklanması için PostgreSQL veritabanı kullanılacaktır. Geliştirme dili olarak kütüphane desteği nedeniyle Python tercih edilmiştir.

Esmanur Yılmaz: Geliştirme ortamı için VS Code kullandım. İlk iş, VS Code'da hospital_ai_env adlı bir python sanal ortamı kurdum ve onu aktive ettim. CNN modelleri için terminal üzerinden "pip install" ile TensorFlow ve Keras'ın kurulumunu da tamamladıktan sonra, ek olarak kendim de biraz araştırma yaptıktan sonra hasta verilerini organize etmemize yardımcı olabilmesi için Pandas & Numpy kurulumu da yaptım. PostgreSQL'i de en son bilgisayarıma indirdikten sonra Antigravity'nin desteyle bunları birbirine bağladım. Sonuç olarak, kurulumu tamamladım.

Zeynep Karataş: Projede kullanılacak veri setini incelemek amacıyla Kaggle üzerinde yer alan Chest X-Ray Images (Pneumonia) veri setini araştırdım. Veri setinin göğüs röntgeni görüntülerinden oluştuğu ve Normal ile Pnömoni olmak üzere iki sınıfa ayrıldığı görüldü. Görüntüler farklı çözünürlüklere sahip olduğu için model eğitimi öncesinde tüm görüntülerin 224x224 boyutuna yeniden ölçeklendirilmesi ve gerekli ön işleme adımlarının uygulanması planlandı.

2. Hafta (13 - 19 Mart) - Mimari Tasarım ve Strateji Geliştirme
Süleyman Kılınç: Veri Kümesi İncelemesi ve Ön İşleme Stratejisi Geliştirme. (Mevcut tıbbi görüntü veri kümelerinin detaylı incelenmesi; gürültü giderme, normalizasyon ve yeniden boyutlandırma stratejilerinin raporlanması.)

Ömer Ensar Şahin: Hastalık Teşhis Algoritması Araştırması ve Mimari Tasarımı. (Literatürdeki başarılı algoritmaların (CNN, RNN, Transformer) araştırılması ve projeye en uygun mimarinin belirlenmesi.)

Cumali Bilgiç: Web Arayüzü Gereksinim Analizi ve Prototip Tasarımı. (Doktorların sisteme nasıl erişeceği, görüntüleri nasıl yükleyeceği ve sonuçları nasıl indireceği senaryolarının belirlenerek wireframe tasarımı yapılması.)

Esmanur Yılmaz: Veritabanı Tasarımı ve Entegrasyon Planlaması. (PostgreSQL şemasının tasarlanması; hasta bilgileri, tıbbi görüntüler ve teşhis sonuçlarının nasıl saklanacağının belirlenmesi.)

Zeynep Karataş: Raporlama Sistemi Gereksinimleri ve Tasarım Şablonu Oluşturma. (Teşhis sonuçları, güvenilirlik skorları ve doktor notlarını içerecek olan PDF/CSV formatındaki rapor tasarımlarının yapılması.)

3. Hafta ve Sonrası (Gelecek Planı)
Süleyman Kılınç: DICOM Görüntü Okuma ve Ön İşleme Fonksiyonlarının Geliştirilmesi.

Ömer Ensar Şahin: Temel Hastalık Teşhis Algoritması Prototipi Geliştirilmesi.

Cumali Bilgiç: Web Arayüzü Temel Tasarımının Oluşturulması.

Esmanur Yılmaz: PostgreSQL Veritabanı Şemasının Tasarlanması (Hafta 4).

Zeynep Karataş: Temel Raporlama Modülünün Geliştirilmesi (Hafta 4).
