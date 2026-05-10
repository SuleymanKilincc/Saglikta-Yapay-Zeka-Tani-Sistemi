# 🩺 Sağlıkta Yapay Zeka Destekli Tanı Sistemi

Bu proje, tıbbi görüntüleri (Röntgen, MR) analiz ederek hastalıkları teşhis etmeye yardımcı olan bir yapay zeka sistemidir. Derin öğrenme teknikleri kullanılarak, sağlık çalışanlarına karar destek mekanizması sunmayı hedefler.

## 👥 1. Ekip ve Görev Dağılımı
* **Süleyman Kılınç** - Scrum Master & Veri Ön İşleme
* **Ömer Ensar Şahin** - Yapay Zeka Modeli Geliştirme
* **Cumali Bilgiç** - Web Arayüzü (Frontend)
* **Esmanur Yılmaz** - Veritabanı (Backend)
* **Zeynep Karataş** - Raporlama Sistemi

## 🛠️ 2. Teknolojiler ve Mimari

Proje, modern yazılım geliştirme prensiplerine uygun olarak katmanlı bir mimari (3-Tier Architecture) üzerine inşa edilmiştir.

### 📊 Kullanılan Teknolojiler Tablosu

| Alan | Teknoloji / Araç | Açıklama |
| :--- | :--- | :--- |
| **Programlama Dili** | Python 3.10+ | Tüm sistemin temel programlama dili. |
| **Yapay Zeka** | TensorFlow / Keras | CNN (Convolutional Neural Networks) model tasarımı ve eğitimi. |
| **Görüntü İşleme** | OpenCV / NumPy | Görüntülerin okunması, boyutlandırılması ve matris işlemleri. |
| **Frontend** | HTML5 / CSS3 / JavaScript | Modern ve kullanıcı dostu web arayüzü. |
| **Backend** | Python / Flask | Web arayüzü ile AI modeli arasındaki köprü (API). |
| **Veritabanı** | PostgreSQL | Hasta kayıtları ve teşhis sonuçlarının güvenli saklanması. |
| **Versiyon Kontrol** | Git / GitHub | Kod yönetimi ve ekip içi senkronizasyon. |

### 🏗️ Sistem Mimarisi
Sistem üç ana katmandan oluşmaktadır:
1.  **Sunum Katmanı (Frontend):** Kullanıcının görüntü yüklediği ve sonuçları gördüğü web arayüzü.
2.  **İş Mantığı Katmanı (Backend & AI):** Görüntülerin ön işlendiği ve yapay zeka modelinin tahmin yürüttüğü çekirdek bölüm.
3.  **Veri Katmanı (Database):** Tüm verilerin kalıcı olarak saklandığı PostgreSQL veritabanı.

## 🚀 Proje Durumu
Şu an **Hafta 6: Proje Dokümantasyonu** aşamasındayız. Veri ön işleme ve AI model prototipi başarıyla tamamlanmıştır.

## 📂 Klasör Yapısı
*   `ai_model/`: Model mimarisi ve eğitim scriptleri.
*   `data_processing/`: Görüntü ön işleme fonksiyonları.
*   `frontend/`: Kullanıcı arayüzü dosyaları.
*   `backend/`: API ve sunucu tarafı kodları.
*   `docs/`: Proje raporları ve gelişim dosyaları.
