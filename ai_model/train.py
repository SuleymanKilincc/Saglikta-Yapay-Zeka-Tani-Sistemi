# -*- coding: utf-8 -*-
"""
============================================================
  Sağlıkta Yapay Zeka Destekli Tanı Sistemi
  Model Eğitim Scripti

  Geliştiren: Ömer Ensar Şahin
  Modül: ai_model/train.py
============================================================
  Bu script, CNN modelini tıbbi görüntü veri seti ile eğitir.
  
  Kullanım:
      python train.py
  
  Veri seti yapısı (dataset/ klasörü altında):
      dataset/
      ├── train/
      │   ├── Normal/       (sağlıklı röntgenler)
      │   ├── Pneumonia/    (pnömoni röntgenleri)
      │   └── Tuberculosis/ (tüberküloz röntgenleri)
      └── test/
          ├── Normal/
          ├── Pneumonia/
          └── Tuberculosis/
============================================================
"""

import os
import sys
import time
import numpy as np

# Windows terminal'de Türkçe karakter ve emoji desteği
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# TensorFlow uyarı mesajlarını sustur
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import (
    ModelCheckpoint,
    EarlyStopping,
    ReduceLROnPlateau,
)

# Konfigürasyon ve model dosyalarını içe aktar
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import (
    DATASET_DIR,
    MODEL_SAVE_PATH,
    TRAINING_HISTORY_PATH,
    IMG_HEIGHT,
    IMG_WIDTH,
    IMG_CHANNELS,
    SINIF_ISIMLERI,
    SINIF_SAYISI,
    DATASET_SINIF_KLASORLERI,
    EPOCHS,
    BATCH_SIZE,
    LEARNING_RATE,
    VALIDATION_SPLIT,
    AUGMENTATION_CONFIG,
)
from model import SaglikCNN


# ============================================================
# VERİ SETİ HAZIRLAMA
# ============================================================
def veri_seti_hazirla():
    """
    Veri setini yükler ve eğitime hazır hale getirir.
    
    İki mod destekler:
    1. Klasör tabanlı: dataset/train/ ve dataset/test/ klasörlerinden yükleme
    2. Otomatik bölme: Tek dataset/ klasöründen train/validation ayırma
    
    Returns:
        tuple: (train_generator, validation_generator, test_generator)
        
    Raises:
        FileNotFoundError: Veri seti klasörü bulunamazsa
    """
    train_dir = os.path.join(DATASET_DIR, "train")
    test_dir = os.path.join(DATASET_DIR, "test")
    
    # Veri seti klasörünün varlığını kontrol et
    if not os.path.exists(DATASET_DIR):
        print("=" * 60)
        print("❌ HATA: Veri seti klasörü bulunamadı!")
        print(f"   Beklenen konum: {DATASET_DIR}")
        print()
        print("📁 Lütfen aşağıdaki yapıyı oluşturun:")
        print("   dataset/")
        print("   ├── train/")
        print("   │   ├── Normal/       (sağlıklı röntgenler)")
        print("   │   ├── Pneumonia/    (pnömoni röntgenleri)")
        print("   │   └── Tuberculosis/ (tüberküloz röntgenleri)")
        print("   └── test/")
        print("       ├── Normal/")
        print("       ├── Pneumonia/")
        print("       └── Tuberculosis/")
        print()
        print("📥 Önerilen veri setleri:")
        print("   1. Chest X-Ray (Pneumonia): kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia")
        print("   2. Tuberculosis (TB): kaggle.com/datasets/tawsifurrahman/tuberculosis-tb-chest-xray-dataset")
        print("=" * 60)
        raise FileNotFoundError(f"Veri seti bulunamadı: {DATASET_DIR}")
    
    if not os.path.exists(train_dir):
        print("❌ HATA: train/ klasörü bulunamadı!")
        print(f"   Beklenen: {train_dir}")
        raise FileNotFoundError(f"Eğitim klasörü bulunamadı: {train_dir}")
    
    print("📂 Veri seti yükleniyor...")
    print(f"   Eğitim dizini: {train_dir}")
    if os.path.exists(test_dir):
        print(f"   Test dizini  : {test_dir}")
    
    # ---- EĞİTİM VERİSİ: Veri Artırma (Data Augmentation) ----
    # Tıbbi görüntülerde veri artırma, modelin farklı açı ve 
    # pozisyonlardaki görüntüleri de öğrenmesini sağlar.
    train_datagen = ImageDataGenerator(
        rescale=1.0 / 255.0,  # Piksel normalizasyonu (0-255 → 0-1)
        validation_split=VALIDATION_SPLIT,
        rotation_range=AUGMENTATION_CONFIG["rotation_range"],
        width_shift_range=AUGMENTATION_CONFIG["width_shift_range"],
        height_shift_range=AUGMENTATION_CONFIG["height_shift_range"],
        zoom_range=AUGMENTATION_CONFIG["zoom_range"],
        horizontal_flip=AUGMENTATION_CONFIG["horizontal_flip"],
        fill_mode=AUGMENTATION_CONFIG["fill_mode"],
    )
    
    # ---- DOĞRULAMA/TEST VERİSİ: Sadece normalizasyon ----
    # Test verisine augmentation uygulanmaz, sadece normalize edilir.
    test_datagen = ImageDataGenerator(rescale=1.0 / 255.0)
    
    # ---- VERİ YÜKLEME ----
    # color_mode='grayscale' → Süleyman'ın preprocess.py ile uyumlu (1 kanal)
    print("\n📊 Eğitim verisi yükleniyor (augmentation ile)...")
    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=(IMG_HEIGHT, IMG_WIDTH),
        color_mode='grayscale',
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training',
        shuffle=True,
    )
    
    print("📊 Doğrulama verisi yükleniyor...")
    validation_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=(IMG_HEIGHT, IMG_WIDTH),
        color_mode='grayscale',
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation',
        shuffle=False,
    )
    
    # Test verisi (varsa)
    test_generator = None
    if os.path.exists(test_dir):
        print("📊 Test verisi yükleniyor...")
        test_generator = test_datagen.flow_from_directory(
            test_dir,
            target_size=(IMG_HEIGHT, IMG_WIDTH),
            color_mode='grayscale',
            batch_size=BATCH_SIZE,
            class_mode='categorical',
            shuffle=False,
        )
    
    # Veri seti istatistiklerini göster
    print(f"\n{'='*40}")
    print(f"📈 Veri Seti Özeti:")
    print(f"   Eğitim görseli    : {train_generator.samples}")
    print(f"   Doğrulama görseli : {validation_generator.samples}")
    if test_generator:
        print(f"   Test görseli      : {test_generator.samples}")
    print(f"   Sınıflar          : {list(train_generator.class_indices.keys())}")
    print(f"   Batch boyutu      : {BATCH_SIZE}")
    print(f"{'='*40}")
    
    return train_generator, validation_generator, test_generator


# ============================================================
# EĞİTİM GEÇMİŞİ GRAFİĞİ
# ============================================================
def egitim_grafigi_kaydet(history):
    """
    Eğitim sürecinin loss ve accuracy grafiklerini kaydeder.
    
    Args:
        history: model.fit() fonksiyonunun döndürdüğü History nesnesi
    """
    try:
        import matplotlib
        matplotlib.use('Agg')  # GUI olmadan çalışabilmek için
        import matplotlib.pyplot as plt
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # ---- Doğruluk (Accuracy) Grafiği ----
        axes[0].plot(history.history['accuracy'], label='Eğitim', linewidth=2)
        axes[0].plot(history.history['val_accuracy'], label='Doğrulama', linewidth=2)
        axes[0].set_title('Model Doğruluğu (Accuracy)', fontsize=14, fontweight='bold')
        axes[0].set_xlabel('Epoch')
        axes[0].set_ylabel('Doğruluk')
        axes[0].legend(fontsize=12)
        axes[0].grid(True, alpha=0.3)
        
        # ---- Kayıp (Loss) Grafiği ----
        axes[1].plot(history.history['loss'], label='Eğitim', linewidth=2)
        axes[1].plot(history.history['val_loss'], label='Doğrulama', linewidth=2)
        axes[1].set_title('Model Kaybı (Loss)', fontsize=14, fontweight='bold')
        axes[1].set_xlabel('Epoch')
        axes[1].set_ylabel('Kayıp')
        axes[1].legend(fontsize=12)
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(TRAINING_HISTORY_PATH, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"\n📊 Eğitim grafikleri kaydedildi: {TRAINING_HISTORY_PATH}")
        
    except ImportError:
        print("⚠️  matplotlib yüklü değil, grafik oluşturulamadı.")
        print("   Yüklemek için: pip install matplotlib")


# ============================================================
# ANA EĞİTİM FONKSİYONU
# ============================================================
def modeli_egit():
    """
    CNN modelini veri setiyle eğitir ve kaydeder.
    
    Süreç:
        1. Veri setini yükle ve augmentation uygula
        2. Model mimarisini oluştur ve derle
        3. Callback'leri ayarla (early stopping, checkpoint, lr reduce)
        4. Modeli eğit
        5. Eğitim grafiklerini kaydet
        6. En iyi modeli diske kaydet
    
    Returns:
        tuple: (model, history) - Eğitilmiş model ve eğitim geçmişi
    """
    print("=" * 60)
    print("  🧠 Sağlıkta Yapay Zeka - Model Eğitimi Başlatılıyor")
    print("=" * 60)
    
    baslangic = time.time()
    
    # 1. Veri setini hazırla
    train_gen, val_gen, test_gen = veri_seti_hazirla()
    
    # 2. Model mimarisini oluştur
    print("\n🏗️  Model mimarisi oluşturuluyor...")
    model = SaglikCNN()
    
    # 3. Modeli derle (compile)
    print("⚙️  Model derleniyor...")
    model.compile(
        optimizer=Adam(learning_rate=LEARNING_RATE),
        loss='categorical_crossentropy',
        metrics=['accuracy'],
    )
    
    model.summary()
    
    # 4. Callback'leri ayarla
    callbacks = [
        # En iyi modeli otomatik kaydet
        ModelCheckpoint(
            MODEL_SAVE_PATH,
            monitor='val_accuracy',
            save_best_only=True,
            mode='max',
            verbose=1,
        ),
        # Gelişme durmazsa eğitimi erken durdur
        EarlyStopping(
            monitor='val_loss',
            patience=5,
            restore_best_weights=True,
            verbose=1,
        ),
        # Gelişme yavaşlarsa öğrenme hızını düşür
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=3,
            min_lr=1e-7,
            verbose=1,
        ),
    ]
    
    # 5. Eğitimi başlat
    print(f"\n🚀 Eğitim başlıyor... ({EPOCHS} epoch, batch size: {BATCH_SIZE})")
    print("-" * 60)
    
    history = model.fit(
        train_gen,
        epochs=EPOCHS,
        validation_data=val_gen,
        callbacks=callbacks,
        verbose=1,
    )
    
    # 6. Eğitim süresini hesapla
    sure = time.time() - baslangic
    dakika = int(sure // 60)
    saniye = int(sure % 60)
    
    print(f"\n{'='*60}")
    print(f"✅ EĞİTİM TAMAMLANDI!")
    print(f"   ⏱️  Süre         : {dakika} dakika {saniye} saniye")
    print(f"   📊 Son Doğruluk  : {history.history['accuracy'][-1]:.2%}")
    print(f"   📊 Val Doğruluk  : {history.history['val_accuracy'][-1]:.2%}")
    print(f"   💾 Model kayıt   : {MODEL_SAVE_PATH}")
    print(f"{'='*60}")
    
    # 7. Eğitim grafiklerini kaydet
    egitim_grafigi_kaydet(history)
    
    # 8. Test seti varsa değerlendir
    if test_gen is not None:
        print("\n🧪 Test seti ile değerlendirme yapılıyor...")
        test_loss, test_accuracy = model.evaluate(test_gen, verbose=0)
        print(f"   Test Kaybı    : {test_loss:.4f}")
        print(f"   Test Doğruluk : {test_accuracy:.2%}")
    
    return model, history


# ============================================================
# ÇALIŞTIRMA
# ============================================================
if __name__ == "__main__":
    print()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║    🩺 Sağlıkta Yapay Zeka Destekli Tanı Sistemi        ║")
    print("║    📚 Model Eğitim Scripti                              ║")
    print("║    👨‍💻 Geliştiren: Ömer Ensar Şahin                     ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()
    
    try:
        model, history = modeli_egit()
    except FileNotFoundError as e:
        print(f"\n{e}")
        print("\n💡 İpucu: Önce veri setini indirip dataset/ klasörüne yerleştirin.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Eğitim kullanıcı tarafından durduruldu.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Beklenmeyen hata: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
