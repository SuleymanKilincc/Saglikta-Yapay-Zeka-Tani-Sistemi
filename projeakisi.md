1. Hafta (6 - 12 Mart) - Başlangıç ve Ortam Kurulumu
* Süleyman Kılınç (Scrum Master / Yönetici): GitHub reposu kuruldu ve koruma ayarları yapıldı. Proje Kapsamı Belirlendi: Sistem, akciğer röntgenlerinden "Pnömoni (Zatürre)" tespiti yapacaktır. İkili sınıflandırma (Sağlıklı/Hastalıklı) problemi çözülecek olup, model olarak Evrişimli Sinir Ağları (CNN) kullanılacaktır. Veri seti olarak Kaggle "Chest X-Ray Images (Pneumonia)" seçilmiştir.

* Ömer Ensar Şahin: Proje için gereksinim analizi tamamlandı. Doktorlar sisteme giriş yapabilecek. MR ve röntgen görüntüleri yüklenecek. Yapay zeka analiz yapacak. Sonuçlar raporlanacak. Model doğruluk hedefi %85. Veri güvenliği KVKK kurallarına uygun olacak.

* Cumali Bilgiç: Proje için teknoloji araştırması tamamlandı. Görüntü işleme ve derin öğrenme (CNN) modelleri için yüksek performans sunan TensorFlow/Keras kütüphanesi seçildi. Verilerin düzenli ve güvenli bir şekilde saklanması için PostgreSQL veritabanı kullanılacaktır. Geliştirme dili olarak kütüphane desteği nedeniyle Python tercih edilmiştir.

* Esmanur Yılmaz: Geliştirme ortamı için VS Code kullanıldı. Python sanal ortamı (hospital_ai_env) kuruldu ve aktif edildi. CNN modelleri için TensorFlow, Keras, Pandas ve Numpy kurulumları tamamlandı. PostgreSQL bağlantıları sağlandı.

* Zeynep Karataş: Kaggle üzerindeki veri seti araştırıldı. Görüntülerin Normal ve Pnömoni olarak iki sınıfa ayrıldığı görüldü. Model eğitimi öncesinde tüm görüntülerin 224x224 boyutuna yeniden ölçeklendirilmesi ve ön işleme adımlarının uygulanması planlandı.

2. Hafta (13 - 19 Mart) - Mimari Tasarım ve Strateji Geliştirme
* Süleyman Kılınç: Veri Kümesi İncelemesi ve Ön İşleme Stratejisi Geliştirme. (Mevcut tıbbi görüntü veri kümelerinin detaylı incelenmesi; gürültü giderme, normalizasyon ve yeniden boyutlandırma stratejilerinin raporlanması.)

* Ömer Ensar Şahin: Hastalık Teşhis Algoritması Araştırması ve Mimari Tasarımı. Literatürde yaygın kullanılan ve başarı sağlamış algoritmalar (CNN, RNN, Transformer vb.) araştırıldı. Proje gereksinimlerine en uygun mimari belirlenerek çalışma prensipleri ve katmanları planlandı.

* Esmanur Yılmaz: Veritabanı Tasarımı ve Entegrasyon Planlaması. Projenin ihtiyaç duyduğu PostgreSQL şeması tasarlandı. Hastaların bilgileri, tıbbi görüntüler ve teşhis sonuçlarının nasıl saklanacağı belirlenerek tablo ilişkileri tanımlandı.

* Zeynep Karataş: Raporlama sistemi için detaylı gereksinim analizi yapıldı. Raporlarda hasta bilgileri, görüntü meta verileri, yapay zeka teşhis sonucu, güvenilirlik skoru ve doktor notlarının yer alması planlandı. Ayrıca raporların PDF ve CSV formatlarında oluşturulmasına karar verildi ve bu doğrultuda standart bir rapor şablonu hazırlandı.
 3. Hafta (20 - 26 Mart) - Detaylı Tasarım ve Geliştirme
* Süleyman Kılınç: DICOM Görüntü Okuma ve Ön İşleme Fonksiyonlarının Geliştirilmesi. (Python tabanlı görüntü iyileştirme fonksiyonlarının planlanması.)

* Ömer Ensar Şahin: UI/UX Wireframe Oluşturma. Kullanıcı arayüzü ve kullanıcı deneyimi tasarımı yapılarak sistemin wireframe yapısı oluşturuldu. [⚠️ Gecikmiş Görev Takibi Yapılıyor]

* Cumali Bilgiç: Web arayüzü gereksinim analizi ve temel iskelet tasarımı çalışmaları.

4. Hafta (27 Mart - 2 Nisan) - Modül ve Algoritma Geliştirme
* Ömer Ensar Şahin: Temel Hastalık Teşhis Algoritması Prototipi Geliştirilmesi. TensorFlow/Keras kullanılarak, evrişimli sinir ağı (CNN) katmanları içeren temel bir model prototipi ve eğitim süreci kurgulandı.

* Esmanur Yılmaz: PostgreSQL Veritabanı Şemasının Tasarlanması. Sistemde kullanılacak verilerin (hasta bilgileri, meta veriler, teşhis sonuçları) saklanması için uygun indeksler ve ölçeklenebilir bir yapı tasarlandı.

* Zeynep Karataş: Belirlenen gereksinimlere uygun olarak temel raporlama modülü geliştirildi. Yapay zeka modelinden elde edilen teşhis sonuçları ile hasta verileri entegre edilerek düzenli bir rapor formatına dönüştürüldü. Modül sayesinde sistem çıktıları PDF formatında oluşturulabilir hale getirildi.
