1. Hafta (6 - 12 Mart) - Başlangıç ve Ortam Kurulumu
Süleyman Kılınç (Scrum Master / Yönetici): GitHub reposu kuruldu ve koruma ayarları yapıldı. Proje Kapsamı Belirlendi: Sistem, akciğer röntgenlerinden "Pnömoni (Zatürre)" tespiti yapacaktır. İkili sınıflandırma (Sağlıklı/Hastalıklı) problemi çözülecek olup, model olarak Evrişimli Sinir Ağları (CNN) kullanılacaktır. Veri seti olarak Kaggle "Chest X-Ray Images (Pneumonia)" seçilmiştir.

Ömer Ensar Şahin: Proje için gereksinim analizi tamamlandı. Doktorlar sisteme giriş yapabilecek. MR ve röntgen görüntüleri yüklenecek. Yapay zeka analiz yapacak. Sonuçlar raporlanacak. Model doğruluk hedefi %85. Veri güvenliği KVKK kurallarına uygun olacak.

Cumali Bilgiç: Proje için teknoloji araştırması tamamlandı. Görüntü işleme ve derin öğrenme (CNN) modelleri için yüksek performans sunan TensorFlow/Keras kütüphanesi seçildi. Verilerin düzenli ve güvenli bir şekilde saklanması için PostgreSQL veritabanı kullanılacaktır. Geliştirme dili olarak kütüphane desteği nedeniyle Python tercih edilmiştir.

Esmanur Yılmaz: Geliştirme ortamı için VS Code kullanıldı. Python sanal ortamı (hospital_ai_env) kuruldu ve aktif edildi. CNN modelleri için TensorFlow, Keras, Pandas ve Numpy kurulumları tamamlandı. PostgreSQL bağlantıları sağlandı.

Zeynep Karataş: Kaggle üzerindeki veri seti araştırıldı. Görüntülerin Normal ve Pnömoni olarak iki sınıfa ayrıldığı görüldü. Model eğitimi öncesinde tüm görüntülerin 224x224 boyutuna yeniden ölçeklendirilmesi ve ön işleme adımlarının uygulanması planlandı.

2. Hafta (13 - 19 Mart) - Mimari Tasarım ve Strateji Geliştirme
Süleyman Kılınç: Veri Kümesi İncelemesi ve Ön İşleme Stratejisi Geliştirme. (Mevcut tıbbi görüntü veri kümelerinin detaylı incelenmesi; gürültü giderme, normalizasyon ve yeniden boyutlandırma stratejilerinin raporlanması.)

Ömer Ensar Şahin: Hastalık Teşhis Algoritması Araştırması ve Mimari Tasarımı. (Literatürdeki başarılı algoritmaların (CNN, RNN, Transformer) araştırılması ve projeye en uygun mimarinin belirlenmesi.)

Cumali Bilgiç: Web Arayüzü Gereksinim Analizi ve Prototip Tasarımı. (Doktorların sisteme erişim senaryolarının belirlenerek wireframe tasarımı yapılması.)

Esmanur Yılmaz: Veritabanı Tasarımı ve Entegrasyon Planlaması. (PostgreSQL şemasının tasarlanması; hasta bilgileri, görüntüler ve teşhis sonuçlarının saklanma planı.)

Zeynep Karataş: Raporlama Sistemi Gereksinimleri ve Tasarım Şablonu Oluşturma. (Teşhis sonuçları ve doktor notlarını içerecek rapor şablonlarının tasarımı.)

3. Hafta (20 - 26 Mart) - Detaylı Tasarım ve Geliştirme
Ömer Ensar Şahin: UI/UX Wireframe Oluşturma. (Kullanıcı arayüzü ve deneyimi tasarımının tamamlanması.) [⚠️ Gecikmiş Görev Takibi Yapılıyor]

Süleyman Kılınç: DICOM Görüntü Okuma ve Ön İşleme Fonksiyonlarının Geliştirilmesi.

Ömer Ensar Şahin: Temel Hastalık Teşhis Algoritması Prototipi Geliştirilmesi.

Cumali Bilgiç: Web Arayüzü Temel Tasarımının Oluşturulması.
