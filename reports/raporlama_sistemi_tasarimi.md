# Raporlama Sistemi Tasarimi

## Gorev Bilgisi

- Sorumlu: Zeynep Karatas
- Hafta: 3
- Gorev: Teshis sonuclari, hasta bilgileri, goruntu bilgileri ve algoritma sonuclarini iceren ozellestirilebilir raporlama sistemini tasarlamak.

## Raporlama Amaci

Raporlama sistemi, yapay zeka tarafindan uretilen tani sonucunu doktorun inceleyebilecegi, arsivlenebilir ve paylasilabilir bir ciktiya donusturur. Bu sistem klinik karar vermez; tani destek bilgisi sunar ve kesin degerlendirme icin doktor gorusunu zorunlu tutar.

## Rapor Icerik Tasarimi

| Bolum | Alanlar | Kaynak |
|---|---|---|
| Hasta bilgileri | Hasta adi soyadi, dogum tarihi, cinsiyet | Web formu |
| Doktor bilgileri | Doktor adi, departman | Web formu |
| Goruntu bilgileri | Dosya adi, analiz tarihi, goruntu tipi | Yukleme akisi |
| AI sonucu | Teshis, guven skoru, risk durumu | `ai_model/model.py` |
| Uyari metni | Yapay zeka destek notu ve doktor onayi uyarisi | Rapor sablonu |

## Format Tasarimi

Birincil rapor formati PDF olarak belirlenmistir. PDF formatinin secilme nedeni, hasta bazli tekil analizlerin kolay arsivlenmesi, yazdirilmasi ve paylasilmasidir. Toplu analiz ihtiyaci icin CSV dis aktarimi sonraki gelistirme asamasi olarak planlanmistir.

## Otomatik Olusturma Akisi

1. Kullanici web arayuzunden hasta ve doktor bilgilerini girer.
2. Rontgen goruntusu yuklenir.
3. `data_processing/preprocess.py` goruntuyu modele uygun hale getirir.
4. `ai_model/model.py` teshis sonucunu ve guven skorunu uretir.
5. `db_manager.py` sonuc kaydini veritabanina alir.
6. `reports/generate_report.py` PDF raporu olusturur.
7. Flask uygulamasi rapor indirme baglantisini kullaniciya dondurur.

## Veritabani Entegrasyonu

Raporlama sistemi, hasta ve teshis bilgilerinin veritabaninda saklanmasi ile birlikte calisir. Boylece rapor dosyasi tekrar uretilmek istendiginde hasta, doktor, teshis ve guven skoru bilgileri sistem kayitlarindan izlenebilir.

## Ozellestirme Kriterleri

- Tarih araligina gore rapor listeleme.
- Hastalik turune gore filtreleme.
- Risk duzeyine gore filtreleme.
- Doktor veya departman bazli rapor takibi.
- PDF rapora doktor notu ekleyebilme.

## Sonuc

Bu tasarim, projenin mevcut Flask, PostgreSQL, AI model ve PDF raporlama yapisi ile uyumludur. Hafta 4'te gelistirilen `generate_report.py` modulu bu tasarimin temel PDF uretim katmanini karsilar.
