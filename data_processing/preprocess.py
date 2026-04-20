import cv2
import numpy as np

def goruntu_hazirla(dosya_yolu):
    print(f"--> İşlem Başlıyor: {dosya_yolu}")
    
    # 1. Görüntüyü Siyah-Beyaz olarak oku (Tıbbi görüntülerde renk gereksizdir)
    resim = cv2.imread(dosya_yolu, cv2.IMREAD_GRAYSCALE)
    
    # Hata kontrolü: Eğer dosya bulunamazsa veya bozuksa uyar
    if resim is None:
        print("HATA: Görüntü okunamadı! Lütfen dosya adını ve yolunu kontrol edin.")
        return None

    # 2. Boyutlandırma (Ömer'in yapay zeka modeli sabit boyut isteyecek, standart 224x224'tür)
    print("--> Görüntü boyutu 224x224 olarak ayarlanıyor...")
    resim_boyutlandirilmis = cv2.resize(resim, (224, 224))
    
    # 3. Normalizasyon (Piksel değerlerini 0-255'ten 0-1 aralığına sıkıştır. AI bunu sever)
    print("--> Pikseller 0-1 aralığına normalize ediliyor...")
    resim_normalize = resim_boyutlandirilmis / 255.0
    
    # 4. Model formatına uygun hale getirme (Matris boyutunu ayarlar)
    son_hal = np.expand_dims(resim_normalize, axis=-1)
    
    print(f"✅ İŞLEM BAŞARILI! Yapay zekaya gidecek matrisin boyutu: {son_hal.shape}")
    return son_hal

# --- TEST AŞAMASI ---
# Eğer bu dosyayı direkt çalıştırırsak aşağıdaki kod devreye girer:
if __name__ == "__main__":
    test_edilecek_dosya = "test_rontgen.jpg"
    
    # Yazdığımız fonksiyonu çağırıyoruz ve sonucu 'matris' isimli değişkene atıyoruz
    matris = goruntu_hazirla(test_edilecek_dosya)