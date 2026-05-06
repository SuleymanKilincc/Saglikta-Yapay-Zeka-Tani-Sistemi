📈 Proje Akış Takvimi ve Görev Takibi
Bu dosya, Sağlıkta Yapay Zeka Destekli Tanı Sistemi projesinin haftalık gelişimini ve ekip üyelerinin tamamladığı görevleri takip etmek amacıyla oluşturulmuştur.

🗓️ 1. HAFTA: Planlama ve Temel Hazırlıklar

Süleyman Kılınç: Proje analizi yapıldı, genel hedefler ve kapsam tanımlandı. Çözülecek yapay zeka problemleri ve kullanılacak veri türleri belirlendi.

Ömer Ensar Şahin: Proje için işlevsel, performans ve güvenlik gereksinimleri toplandı; detaylı gereksinim belgesi oluşturuldu.

Cumali Bilgiç: Projeye en uygun yapay zeka algoritmaları ve kütüphaneleri araştırıldı. Teknoloji seçimi gerekçeleriyle birlikte tamamlandı.

Esmanur Yılmaz: Geliştirme ortamı (IDE, Python sanal ortam vb.) kuruldu. Gerekli tüm kütüphaneler ve araçlar yapılandırıldı.

Zeynep Karataş: Kullanılacak tıbbi veri setleri (Röntgen/MR) incelendi, veri kalitesi değerlendirildi ve ön işleme adımları planlandı.


🗓️ 2. HAFTA: Strateji Geliştirme ve Gereksinim Analizi

Süleyman Kılınç: Veri kümeleri boyut, format ve etiketleme açısından incelendi. Gürültü giderme ve normalizasyon gibi ön işleme stratejileri raporlandı.

Cumali Bilgiç: Doktorlar için kullanıcı senaryoları göz önünde bulundurularak web arayüzü gereksinim analizi tamamlandı.

Ömer Ensar Şahin: Literatürdeki başarılı hastalık teşhis algoritmaları (CNN, RNN vb.) araştırıldı ve sistem için uygun mimari tasarım belirlendi.

Esmanur Yılmaz: PostgreSQL veritabanı tasarımı yapıldı ve Python uygulaması ile veritabanı arasındaki entegrasyon süreci planlandı.

Zeynep Karataş: Sistem tarafından üretilecek raporların içeriği (teşhis sonuçları, güvenilirlik skorları vb.) ve formatı (PDF/CSV) belirlendi; tasarım şablonu oluşturuldu.


🗓️ 3. HAFTA: Mimari Tasarım ve Modelleme

Süleyman Kılınç: Veritabanı tabloları arasındaki ilişkiler ve alanlar belirlenerek detaylı veritabanı şeması tasarlandı.

Cumali Bilgiç: Sistemin genel mimarisi (Sunum, İş Mantığı, Veri Katmanı) planlandı. Bileşenler arası veri akışını gösteren akış şeması hazırlandı.

Ömer Ensar Şahin: Kullanıcı arayüzü ve deneyimi (UI/UX) tasarımları yapılarak wireframe (taslak) çizimleri tamamlandı.


🗓️ 4. HAFTA: Geliştirme ve Prototipleme

Süleyman Kılınç: DICOM formatındaki görüntüleri okuyan ve ön işleme (kontrast artırma, yeniden boyutlandırma) yapan Python fonksiyonları geliştirildi.

Cumali Bilgiç: HTML, CSS ve JavaScript kullanılarak temel web arayüzü iskeleti oluşturuldu; görüntü yükleme ve sonuç görüntüleme bileşenleri planlandı.

Ömer Ensar Şahin: TensorFlow/Keras kullanılarak temel bir hastalık teşhis algoritması prototipi (CNN) geliştirildi ve performans ölçümleri yapıldı.

Esmanur Yılmaz: Verilerin (hasta bilgileri, teşhis sonuçları vb.) saklanması için PostgreSQL veritabanı şeması tasarlandı ve veri tipleri belirlendi.

Zeynep Karataş: Teşhis sonuçlarını ve hasta bilgilerini içeren temel raporlama modülü geliştirildi; PDF formatında çıktı alma altyapısı kuruldu.


Hafta 5: Performans Analizi ve Iyilestirme Onerileri

Zeynep Karatas: Yapay zeka modelinin hiz, dogruluk ve genel verimlilik acisindan performans analizi tamamlandi. MobileNetV2 tabanli modelin guclu ve zayif yonleri degerlendirildi; veri kalitesi, sinif dengesi, model izleme, raporlama ve sistem verimliligi icin iyilestirme onerileri dokumante edildi.


Hafta 6: Final Proje Teslimi ve Arsivleme

Zeynep Karatas: Raporlama modulu, rapor gereksinimleri, performans analizi ve final teslim dokumantasyonu bir araya getirildi. Proje ciktilarinin hangi klasorlerde yer aldigi belirlendi, runtime sirasinda olusan rapor dosyalarinin kaynak koddan ayrilmasi icin arsivleme duzeni tamamlandi.


Zeynep Karatas Sprint Teslim Detaylari

Hafta 1: Veri seti kalite kriterleri, dosya formati kontrolleri, sinif dengesi riskleri ve on isleme adimlari `docs/veri-seti-on-isleme-plani.md` dosyasinda detaylandirildi.

Hafta 2: Rapor gereksinimleri doktor/departman bilgisi, model uyari metni, ornek rapor taslagi ve kabul kriterleriyle guclendirildi.

Hafta 3: Raporlama sisteminin hasta bilgileri, goruntu bilgileri, AI sonucu, PDF formati, otomatik olusturma akisi ve veritabani entegrasyonu `reports/raporlama_sistemi_tasarimi.md` dosyasinda tasarlandi.

Hafta 4: PDF raporlama modulu geriye uyumlu sekilde goruntu adi, model bilgisi ve opsiyonel doktor notu alanlarini destekleyecek sekilde guclendirildi.

Hafta 5: Model performans analizi; dogruluk, hiz, verimlilik, zayif/guclu yonler ve iyilestirme onerileriyle `docs/performans-analizi/performans-raporu.md` dosyasinda tamamlandi.

Hafta 6: Final teslim ve arsivleme kapsami `docs/FINAL_PROJE_TESLIMI.md` dosyasinda kod, dokumantasyon, raporlama, veritabani, arayuz ve runtime ciktilari acisindan toparlandi.
