import cv2
import numpy as np

def goruntu_hazirla(dosya_yolu):
    print(f"--> İşlem Başlıyor: {dosya_yolu}")
    
    # 1. Görüntüyü Renkli (RGB) olarak oku (MobileNetV2 3 kanal bekler)
    resim = cv2.imread(dosya_yolu, cv2.IMREAD_COLOR)
    
    # Hata kontrolü: Eğer dosya bulunamazsa veya bozuksa uyar
    if resim is None:
        print("HATA: Görüntü okunamadı! Lütfen dosya adını ve yolunu kontrol edin.")
        return None

    # OpenCV BGR okur, biz RGB'ye çevirelim
    resim = cv2.cvtColor(resim, cv2.COLOR_BGR2RGB)

    # 2. Boyutlandırma (Standart 224x224)
    print("--> Görüntü boyutu 224x224 olarak ayarlanıyor...")
    resim_boyutlandirilmis = cv2.resize(resim, (224, 224))
    
    # 3. Normalizasyon (Piksel değerlerini 0-255'ten 0-1 aralığına sıkıştır)
    print("--> Pikseller 0-1 aralığına normalize ediliyor...")
    son_hal = resim_boyutlandirilmis / 255.0
    
    print(f"✅ İŞLEM BAŞARILI! Yapay zekaya gidecek matrisin boyutu: {son_hal.shape}")
    return son_hal

# --- TEST AŞAMASI ---
# Eğer bu dosyayı direkt çalıştırırsak aşağıdaki kod devreye girer:
if __name__ == "__main__":
    test_edilecek_dosya = "test_rontgen.jpg"
    
    # Yazdığımız fonksiyonu çağırıyoruz ve sonucu 'matris' isimli değişkene atıyoruz
    matris = goruntu_hazirla(test_edilecek_dosya)