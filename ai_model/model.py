# -*- coding: utf-8 -*-
"""
============================================================
  Sağlıkta Yapay Zeka Destekli Tanı Sistemi
  CNN Model Mimarisi ve Teşhis Fonksiyonu

  Geliştiren: Ömer Ensar Şahin
  Modül: ai_model/model.py
============================================================
  Bu dosya iki ana bileşen içerir:
  1. SaglikCNN(): Evrişimsel Sinir Ağı (CNN) model mimarisi
  2. teshis_yap(): Süleyman'ın preprocess çıktısını alıp
     hastalık teşhisi döndüren ana fonksiyon
============================================================
"""

import os
import sys
import numpy as np

# Windows terminal'de Türkçe karakter ve emoji desteği
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# TensorFlow uyarı mesajlarını sustur (temiz çıktı için)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models

# Konfigürasyon dosyasını içe aktar
# (Bu dosya ile aynı dizinde olan config.py)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import (
    INPUT_SHAPE,
    SINIF_ISIMLERI,
    SINIF_SAYISI,
    SINIF_ACIKLAMALARI,
    DROPOUT_RATE,
    DENSE_UNITS,
    MODEL_SAVE_PATH,
    DEMO_MODE,
)


# ============================================================
# CNN MODEL MİMARİSİ
# ============================================================
def SaglikCNN():
    """
    Göğüs röntgeni görüntülerinden hastalık teşhisi yapan
    Evrişimsel Sinir Ağı (CNN) modeli oluşturur.

    Mimari:
        Input (224, 224, 1)
            → Conv2D(32, 3x3) + BatchNorm + ReLU + MaxPool(2x2)
            → Conv2D(64, 3x3) + BatchNorm + ReLU + MaxPool(2x2)
            → Conv2D(128, 3x3) + BatchNorm + ReLU + MaxPool(2x2)
            → GlobalAveragePooling2D
            → Dense(128) + Dropout(0.5)
            → Dense(3, softmax)

    Returns:
        tensorflow.keras.Model: Derlenmiş CNN modeli

    Not:
        - Giriş boyutu Süleyman'ın preprocess.py çıktısıyla
          uyumludur: (224, 224, 1) gri tonlama
        - Çıkış: 3 sınıf (Normal, Pnömoni, Tüberküloz)
          üzerinde olasılık dağılımı
    """

    model = models.Sequential(name="SaglikCNN")

    # ---- BLOK 1: İlk Özellik Çıkarma Katmanı ----
    # 32 adet 3x3 filtre ile temel kenar ve doku özellikleri çıkarılır
    model.add(layers.Conv2D(
        filters=32,
        kernel_size=(3, 3),
        padding='same',
        input_shape=INPUT_SHAPE,
        name='conv2d_blok1'
    ))
    model.add(layers.BatchNormalization(name='batchnorm_blok1'))
    model.add(layers.Activation('relu', name='relu_blok1'))
    model.add(layers.MaxPooling2D(pool_size=(2, 2), name='maxpool_blok1'))
    # Çıkış boyutu: (112, 112, 32)

    # ---- BLOK 2: Orta Seviye Özellik Çıkarma ----
    # 64 filtre ile daha karmaşık yapılar (lezyon sınırları vb.) öğrenilir
    model.add(layers.Conv2D(
        filters=64,
        kernel_size=(3, 3),
        padding='same',
        name='conv2d_blok2'
    ))
    model.add(layers.BatchNormalization(name='batchnorm_blok2'))
    model.add(layers.Activation('relu', name='relu_blok2'))
    model.add(layers.MaxPooling2D(pool_size=(2, 2), name='maxpool_blok2'))
    # Çıkış boyutu: (56, 56, 64)

    # ---- BLOK 3: Üst Seviye Özellik Çıkarma ----
    # 128 filtre ile hastalık-spesifik örüntüler (konsolidasyon, kavite vb.) yakalanır
    model.add(layers.Conv2D(
        filters=128,
        kernel_size=(3, 3),
        padding='same',
        name='conv2d_blok3'
    ))
    model.add(layers.BatchNormalization(name='batchnorm_blok3'))
    model.add(layers.Activation('relu', name='relu_blok3'))
    model.add(layers.MaxPooling2D(pool_size=(2, 2), name='maxpool_blok3'))
    # Çıkış boyutu: (28, 28, 128)

    # ---- GLOBAL AVERAGE POOLING ----
    # Her özellik haritasının ortalamasını alarak boyut indirgeme yapar.
    # Flatten yerine kullanılır çünkü parametresizdir ve aşırı öğrenmeyi azaltır.
    model.add(layers.GlobalAveragePooling2D(name='global_avg_pool'))
    # Çıkış boyutu: (128,)

    # ---- SINIFLANDIRMA KATMANLARI ----
    # Tam bağlı (Dense) katman ile özellikler birleştirilir
    model.add(layers.Dense(DENSE_UNITS, activation='relu', name='dense_fc'))
    model.add(layers.Dropout(DROPOUT_RATE, name='dropout'))
    # Çıkış boyutu: (128,)

    # ---- ÇIKIŞ KATMANI ----
    # Softmax aktivasyonu her sınıf için olasılık üretir (toplamı 1.0)
    model.add(layers.Dense(SINIF_SAYISI, activation='softmax', name='output'))
    # Çıkış boyutu: (3,) → [Normal, Pnömoni, Tüberküloz] olasılıkları

    return model


# ============================================================
# MODEL YÜKLEME
# ============================================================
def _modeli_yukle():
    """
    Eğitilmiş modeli diskten yükler.
    Eğer model dosyası yoksa None döndürür (demo modu devreye girer).

    Returns:
        tensorflow.keras.Model veya None
    """
    if os.path.exists(MODEL_SAVE_PATH):
        try:
            model = keras.models.load_model(MODEL_SAVE_PATH)
            print(f"✅ Model başarıyla yüklendi: {MODEL_SAVE_PATH}")
            return model
        except Exception as e:
            print(f"⚠️ Model yüklenirken hata oluştu: {e}")
            print("   Demo moduna geçiliyor...")
            return None
    else:
        return None


# ============================================================
# ANA TEŞHİS FONKSİYONU
# ============================================================
def teshis_yap(goruntu_matrisi):
    """
    Süleyman'ın goruntu_hazirla() fonksiyonundan gelen numpy
    array'ini alır ve hastalık teşhisi yapar.

    Bu fonksiyon projenin ana entegrasyon noktasıdır:
        preprocess.py → model.py → frontend

    Args:
        goruntu_matrisi (numpy.ndarray):
            Süleyman'ın goruntu_hazirla() fonksiyonundan dönen
            normalize edilmiş görüntü matrisi.
            Beklenen boyut: (224, 224, 1) veya (1, 224, 224, 1)

    Returns:
        dict: Teşhis sonucunu içeren sözlük
            {
                "hastalik": str,        # Tespit edilen hastalık adı
                "guven_skoru": float,    # 0.0 - 1.0 arası güven skoru
                "aciklama": str,         # Hastalık açıklaması
                "tum_olasiliklar": dict, # Her sınıf için olasılık
                "demo_modu": bool        # Demo modunda mı çalışıyor
            }

    Raises:
        ValueError: Geçersiz girdi boyutu veya tipi durumunda

    Örnek Kullanım:
        >>> from data_processing.preprocess import goruntu_hazirla
        >>> from ai_model.model import teshis_yap
        >>>
        >>> matris = goruntu_hazirla("rontgen.jpg")
        >>> sonuc = teshis_yap(matris)
        >>> print(sonuc["hastalik"])      # "Pnömoni"
        >>> print(sonuc["guven_skoru"])   # 0.87
    """

    # ---- GİRDİ DOĞRULAMA ----
    if goruntu_matrisi is None:
        raise ValueError(
            "Hata: goruntu_matrisi None! "
            "Lütfen goruntu_hazirla() fonksiyonunun doğru çalıştığını kontrol edin."
        )

    if not isinstance(goruntu_matrisi, np.ndarray):
        raise ValueError(
            f"Hata: Beklenen tip numpy.ndarray, gelen tip: {type(goruntu_matrisi)}. "
            "Lütfen goruntu_hazirla() fonksiyonunun çıktısını kontrol edin."
        )

    # ---- BOYUT AYARLAMA ----
    # goruntu_hazirla() fonksiyonu (224, 224, 1) boyutunda döndürür.
    # Keras modeli (batch_size, 224, 224, 1) boyutu bekler.
    # Tek bir görüntü için batch boyutunu eklememiz gerekir.
    if goruntu_matrisi.ndim == 3:
        # (224, 224, 1) → (1, 224, 224, 1)
        goruntu_batch = np.expand_dims(goruntu_matrisi, axis=0)
    elif goruntu_matrisi.ndim == 4:
        # Zaten (1, 224, 224, 1) formatında
        goruntu_batch = goruntu_matrisi
    else:
        raise ValueError(
            f"Hata: Beklenen boyut 3D veya 4D, gelen boyut: {goruntu_matrisi.ndim}D "
            f"(shape: {goruntu_matrisi.shape}). "
            "goruntu_hazirla() fonksiyonu (224, 224, 1) döndürmelidir."
        )

    # ---- TAHMİN ----
    if DEMO_MODE:
        # Demo modu: Eğitilmiş model yoksa rastgele tahmin üret
        print("⚠️  DEMO MODU: Eğitilmiş model bulunamadı, simülasyon tahmini üretiliyor.")
        print("   Gerçek tahmin için önce train.py ile modeli eğitin.")
        olasiliklar = _demo_tahmin_uret()
    else:
        # Gerçek tahmin: Eğitilmiş modeli yükle ve tahmin yap
        model = _modeli_yukle()
        if model is None:
            print("⚠️  Model yüklenemedi, demo moduna geçiliyor...")
            olasiliklar = _demo_tahmin_uret()
        else:
            # Model tahmini: (1, 3) boyutunda olasılık dizisi döner
            tahmin = model.predict(goruntu_batch, verbose=0)
            olasiliklar = tahmin[0]  # İlk (ve tek) görüntünün sonuçları

    # ---- SONUÇ OLUŞTURMA ----
    # En yüksek olasılıklı sınıfı bul
    en_yuksek_index = int(np.argmax(olasiliklar))
    hastalik_adi = SINIF_ISIMLERI[en_yuksek_index]
    guven_skoru = float(olasiliklar[en_yuksek_index])

    # Tüm sınıflar için olasılıkları sözlük olarak hazırla
    tum_olasiliklar = {}
    for i, sinif in enumerate(SINIF_ISIMLERI):
        tum_olasiliklar[sinif] = round(float(olasiliklar[i]), 4)

    # Sonuç sözlüğünü döndür
    sonuc = {
        "hastalik": hastalik_adi,
        "guven_skoru": round(guven_skoru, 4),
        "aciklama": SINIF_ACIKLAMALARI.get(hastalik_adi, ""),
        "tum_olasiliklar": tum_olasiliklar,
        "demo_modu": DEMO_MODE or (not os.path.exists(MODEL_SAVE_PATH)),
    }

    return sonuc


# ============================================================
# DEMO TAHMİN ÜRETİCİ
# ============================================================
def _demo_tahmin_uret():
    """
    Eğitilmiş model olmadan test amaçlı rastgele tahmin üretir.
    Softmax benzeri olasılık dağılımı simüle eder.

    Returns:
        numpy.ndarray: (3,) boyutunda olasılık dizisi (toplamı 1.0)
    """
    # Rastgele olasılıklar üret
    raw = np.random.dirichlet(np.ones(SINIF_SAYISI))
    return raw


# ============================================================
# TEST / DEMO
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("  Sağlıkta Yapay Zeka Tanı Sistemi - Model Testi")
    print("=" * 60)

    # 1. Model mimarisini oluştur ve özetini göster
    print("\n📐 CNN Model Mimarisi:")
    print("-" * 40)
    model = SaglikCNN()
    model.summary()

    # 2. Demo teşhis testi
    print("\n🧪 Demo Teşhis Testi:")
    print("-" * 40)

    # Süleyman'ın fonksiyonunun üreteceği formatta sahte görüntü oluştur
    # (224, 224, 1) boyutunda rastgele gri tonlama görüntü
    sahte_goruntu = np.random.rand(224, 224, 1).astype(np.float32)
    print(f"   Girdi boyutu: {sahte_goruntu.shape}")

    # Teşhis yap
    sonuc = teshis_yap(sahte_goruntu)

    # Sonuçları göster
    print(f"\n📋 Teşhis Sonucu:")
    print(f"   🏥 Hastalık    : {sonuc['hastalik']}")
    print(f"   📊 Güven Skoru : {sonuc['guven_skoru']:.2%}")
    print(f"   📝 Açıklama    : {sonuc['aciklama']}")
    print(f"   🔬 Demo Modu   : {'Evet' if sonuc['demo_modu'] else 'Hayır'}")
    print(f"\n   Tüm Olasılıklar:")
    for sinif, oran in sonuc['tum_olasiliklar'].items():
        barcik = "█" * int(oran * 30)
        print(f"      {sinif:12s} : {oran:.2%} {barcik}")

    print("\n✅ Model testi başarıyla tamamlandı!")
