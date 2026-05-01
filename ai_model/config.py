# -*- coding: utf-8 -*-
"""
============================================================
  Sağlıkta Yapay Zeka Destekli Tanı Sistemi
  Konfigürasyon Dosyası
  
  Geliştiren: Ömer Ensar Şahin
  Modül: ai_model/config.py
============================================================
  Bu dosya, yapay zeka modelinin tüm ayarlarını merkezi
  bir yerde tutar. Hiperparametreler, sınıf isimleri,
  dosya yolları ve veri seti yapılandırmaları burada
  tanımlanır.
============================================================
"""

import os

# ============================================================
# DOSYA YOLLARI
# ============================================================
# Bu dosyanın bulunduğu dizin (ai_model/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Proje kök dizini (Saglikta-Yapay-Zeka-Tani-Sistemi/)
PROJECT_ROOT = os.path.dirname(BASE_DIR)

# Veri seti dizini (proje kökünde dataset/ klasörü)
DATASET_DIR = os.path.join(PROJECT_ROOT, "dataset")

# Eğitilmiş model kayıt yolu
MODEL_SAVE_PATH = os.path.join(BASE_DIR, "saglik_cnn_model.h5")

# Değerlendirme raporu kayıt yolu
EVALUATION_REPORT_PATH = os.path.join(BASE_DIR, "evaluation_report.txt")

# Eğitim geçmişi grafiği kayıt yolu
TRAINING_HISTORY_PATH = os.path.join(BASE_DIR, "training_history.png")

# ============================================================
# GÖRÜNTÜ AYARLARI
# ============================================================
# Süleyman'ın preprocess.py dosyasındaki goruntu_hazirla()
# fonksiyonu 224x224 boyutunda RGB görüntü üretecek.
# Profesyonel modeller (MobileNetV2) 3 kanal bekler.
IMG_HEIGHT = 224
IMG_WIDTH = 224
IMG_CHANNELS = 3  # RGB Renkli

# Model girdi boyutu (height, width, channels)
INPUT_SHAPE = (IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS)

# ============================================================
# SINIF (HASTALIK) TANIMLARI
# ============================================================
# Modelin teşhis edebileceği hastalık sınıfları
# Sıralama önemlidir: index numarası = sınıf ID'si
SINIF_ISIMLERI = ["Normal", "Pnömoni", "Tüberküloz"]

# Sınıf sayısı (otomatik hesaplanır)
SINIF_SAYISI = len(SINIF_ISIMLERI)

# Sınıf açıklamaları (raporlama ve frontend için)
SINIF_ACIKLAMALARI = {
    "Normal": "Sağlıklı akciğer görüntüsü, herhangi bir patoloji tespit edilmedi.",
    "Pnömoni": "Pnömoni (Zatürre) bulguları tespit edildi. Akciğerde enfeksiyon belirtileri mevcut.",
    "Tüberküloz": "Tüberküloz (Verem) bulguları tespit edildi. İleri tetkik önerilir.",
}

# ============================================================
# VERİ SETİ KLASÖR YAPISI
# ============================================================
# Beklenen klasör yapısı:
#   dataset/
#   ├── train/
#   │   ├── Normal/
#   │   ├── Pneumonia/
#   │   └── Tuberculosis/
#   └── test/
#       ├── Normal/
#       ├── Pneumonia/
#       └── Tuberculosis/
#
# Not: Klasör isimleri İngilizce, sınıf isimleri Türkçe eşleştirilir.
DATASET_SINIF_KLASORLERI = {
    "Normal": "Normal",
    "Pnömoni": "Pneumonia",
    "Tüberküloz": "Tuberculosis",
}

# ============================================================
# HİPERPARAMETRELER
# ============================================================
# Eğitim ayarları
EPOCHS = 20              # Eğitim tur sayısı
BATCH_SIZE = 32           # Her adımda işlenecek görüntü sayısı
LEARNING_RATE = 0.0001    # Transfer Learning için düşük öğrenme hızı (Adam)
VALIDATION_SPLIT = 0.2    # Doğrulama seti oranı (%20)

# Model mimarisi ayarları
DROPOUT_RATE = 0.5        # Dropout oranı (aşırı öğrenmeyi önler)
DENSE_UNITS = 128         # Son tam bağlı katmandaki nöron sayısı

# ============================================================
# VERİ ARTIRMA (DATA AUGMENTATION) AYARLARI
# ============================================================
# Eğitim verisini yapay olarak çoğaltmak için kullanılır.
# Tıbbi görüntülerde dikkatli kullanılmalıdır.
AUGMENTATION_CONFIG = {
    "rotation_range": 15,        # ±15 derece döndürme
    "width_shift_range": 0.1,    # Yatay kaydırma (%10)
    "height_shift_range": 0.1,   # Dikey kaydırma (%10)
    "zoom_range": 0.1,           # Yakınlaştırma (%10)
    "horizontal_flip": True,     # Yatay çevirme (ayna)
    "fill_mode": "nearest",      # Boşlukları en yakın piksel ile doldur
}

# ============================================================
# MODEL MODU
# ============================================================
# True: Eğitilmiş model yüklenir ve gerçek tahmin yapar
# False: Demo modu - rastgele tahmin üretir (test amaçlı)
DEMO_MODE = not os.path.exists(MODEL_SAVE_PATH)
