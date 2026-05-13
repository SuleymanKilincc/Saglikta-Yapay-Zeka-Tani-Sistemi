# Raporlama Sistemi Gereksinimleri

## 1. Rapor İçeriği
Sistem tarafından üretilecek raporlar şu bilgileri içermelidir:
- Hasta adı soyadı
- Rapor tarihi ve saati
- Yüklenen röntgen görüntüsü (referans)
- Yapay zeka teşhis sonucu (hastalık adı)
- Güvenilirlik skoru (örn: %85)
- Risk düzeyi (düşük / orta / yüksek)
- Doktor notu (opsiyonel alan)
- Doktor adı ve departman bilgisi
- Model/analiz uyarısı: sonuçların doktor onayı gerektirdiği belirtilmelidir

## 2. Rapor Formatları
- Birincil format: PDF (A4, Türkçe)
- İsteğe bağlı: CSV (toplu dışa aktarım için)

## 3. Filtreleme Kriterleri
Kullanıcılar şu kriterlere göre rapor oluşturabilmelidir:
- Tarih aralığı (başlangıç - bitiş)
- Hastalık türü
- Risk düzeyi

## 4. Örnek Rapor Taslağı
[Hasta Adı]: Ahmet Yılmaz
[Doktor]: Dr. Ayşe Demir
[Departman]: Radyoloji
[Tarih]: 24.04.2026 14:30
[Teşhis]: Pnömoni
[Güvenilirlik]: %85
[Risk]: YÜKSEK RİSK
NOT: Bu rapor yapay zeka tarafından üretilmiştir.
Kesin tanı için doktor görüşü alınız.

## 5. Kabul Kriterleri
- PDF rapor A4 formatında üretilebilmelidir.
- Türkçe karakterler mümkün olduğunca doğru gösterilmelidir.
- Rapor klasörü yoksa sistem otomatik oluşturmalıdır.
- Güven skoru yüzde formatında yazılmalıdır.
- Normal sonuçlarda risk alanı sağlıklı/risk yok şeklinde belirtilmelidir.
- Hastalık tespitlerinde risk düzeyi güven skoruna göre düşük, orta veya yüksek olarak hesaplanmalıdır.
- Rapor çıktısı uygulama tarafından indirilebilir olmalıdır.
