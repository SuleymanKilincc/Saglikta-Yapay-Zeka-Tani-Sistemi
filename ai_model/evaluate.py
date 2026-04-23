# -*- coding: utf-8 -*-
"""
============================================================
  Sağlıkta Yapay Zeka Destekli Tanı Sistemi
  Model Performans Değerlendirmesi

  Geliştiren: Ömer Ensar Şahin
  Modül: ai_model/evaluate.py
============================================================
  Bu script, eğitilmiş CNN modelinin performansını ölçer:
  - Doğruluk (Accuracy)
  - Hassasiyet (Precision)
  - Duyarlılık (Recall / Sensitivity)
  - F1-Skoru
  - Karmaşıklık Matrisi (Confusion Matrix)
  
  Kullanım:
      python evaluate.py
============================================================
"""

import os
import sys
import numpy as np
from datetime import datetime

# Windows terminal'de Türkçe karakter ve emoji desteği
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# TensorFlow uyarı mesajlarını sustur
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)

# Konfigürasyon dosyasını içe aktar
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import (
    DATASET_DIR,
    MODEL_SAVE_PATH,
    EVALUATION_REPORT_PATH,
    IMG_HEIGHT,
    IMG_WIDTH,
    BATCH_SIZE,
    SINIF_ISIMLERI,
    SINIF_SAYISI,
)


# ============================================================
# MODEL DEĞERLENDİRME
# ============================================================
def modeli_degerlendir():
    """
    Eğitilmiş modeli test veri seti üzerinde değerlendirir.
    
    Ölçülen metrikler:
        - Accuracy (Doğruluk): Tüm doğru tahminlerin oranı
        - Precision (Hassasiyet): Pozitif tahminlerin ne kadarı doğru
        - Recall (Duyarlılık): Gerçek pozitiflerin ne kadarı yakalandı
        - F1-Score: Precision ve Recall'un harmonik ortalaması
        - Confusion Matrix: Hangi sınıflar birbiriyle karıştırılıyor
    
    Returns:
        dict: Tüm metrikleri içeren sözlük
        
    Raises:
        FileNotFoundError: Model veya test verisi bulunamazsa
    """
    
    print("=" * 60)
    print("  📊 Model Performans Değerlendirmesi")
    print("=" * 60)
    
    # ---- MODEL KONTROLÜ ----
    if not os.path.exists(MODEL_SAVE_PATH):
        print(f"\n❌ HATA: Eğitilmiş model bulunamadı!")
        print(f"   Beklenen: {MODEL_SAVE_PATH}")
        print(f"   Önce train.py ile modeli eğitin.")
        raise FileNotFoundError(f"Model bulunamadı: {MODEL_SAVE_PATH}")
    
    # ---- TEST VERİSİ KONTROLÜ ----
    test_dir = os.path.join(DATASET_DIR, "test")
    if not os.path.exists(test_dir):
        print(f"\n❌ HATA: Test veri seti bulunamadı!")
        print(f"   Beklenen: {test_dir}")
        raise FileNotFoundError(f"Test klasörü bulunamadı: {test_dir}")
    
    # ---- MODEL YÜKLEME ----
    print("\n📥 Eğitilmiş model yükleniyor...")
    model = keras.models.load_model(MODEL_SAVE_PATH)
    print(f"   ✅ Model yüklendi: {MODEL_SAVE_PATH}")
    
    # ---- TEST VERİSİ YÜKLEME ----
    print("\n📂 Test verisi yükleniyor...")
    test_datagen = ImageDataGenerator(rescale=1.0 / 255.0)
    
    test_generator = test_datagen.flow_from_directory(
        test_dir,
        target_size=(IMG_HEIGHT, IMG_WIDTH),
        color_mode='grayscale',
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=False,  # Sıralı yükle (karmaşıklık matrisi için gerekli)
    )
    
    print(f"   Test görseli sayısı: {test_generator.samples}")
    print(f"   Sınıflar: {list(test_generator.class_indices.keys())}")
    
    # ---- TAHMİN YAPMA ----
    print("\n🔮 Tahminler yapılıyor...")
    tahminler_raw = model.predict(test_generator, verbose=1)
    
    # Tahmin edilen sınıflar (en yüksek olasılıklı)
    tahmin_etiketleri = np.argmax(tahminler_raw, axis=1)
    
    # Gerçek etiketler
    gercek_etiketler = test_generator.classes
    
    # Sınıf isimleri (generator'dan)
    sinif_isimleri_sirali = list(test_generator.class_indices.keys())
    
    # ---- METRİKLER ----
    print("\n📈 Metrikler hesaplanıyor...")
    
    # Genel doğruluk
    accuracy = accuracy_score(gercek_etiketler, tahmin_etiketleri)
    
    # Sınıf bazlı metrikler (macro: tüm sınıfların ortalaması)
    precision = precision_score(
        gercek_etiketler, tahmin_etiketleri, average='macro', zero_division=0
    )
    recall = recall_score(
        gercek_etiketler, tahmin_etiketleri, average='macro', zero_division=0
    )
    f1 = f1_score(
        gercek_etiketler, tahmin_etiketleri, average='macro', zero_division=0
    )
    
    # Karmaşıklık matrisi
    conf_matrix = confusion_matrix(gercek_etiketler, tahmin_etiketleri)
    
    # Detaylı sınıflandırma raporu
    detayli_rapor = classification_report(
        gercek_etiketler,
        tahmin_etiketleri,
        target_names=sinif_isimleri_sirali,
        zero_division=0,
    )
    
    # ---- SONUÇLARI GÖSTER ----
    print(f"\n{'='*60}")
    print(f"  📋 PERFORMANS SONUÇLARI")
    print(f"{'='*60}")
    print(f"   🎯 Doğruluk  (Accuracy)  : {accuracy:.2%}")
    print(f"   🔍 Hassasiyet (Precision) : {precision:.2%}")
    print(f"   📡 Duyarlılık (Recall)    : {recall:.2%}")
    print(f"   ⚖️  F1-Skoru              : {f1:.2%}")
    print(f"{'='*60}")
    
    print(f"\n📊 Detaylı Sınıflandırma Raporu:")
    print("-" * 60)
    print(detayli_rapor)
    
    print(f"\n🔢 Karmaşıklık Matrisi (Confusion Matrix):")
    print("-" * 60)
    _karmasiklik_matrisi_yazdir(conf_matrix, sinif_isimleri_sirali)
    
    # ---- SONUÇLARI SÖZLÜKTE TOPLA ----
    sonuclar = {
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1, 4),
        "confusion_matrix": conf_matrix.tolist(),
        "classification_report": detayli_rapor,
        "test_samples": test_generator.samples,
        "siniflar": sinif_isimleri_sirali,
    }
    
    # ---- RAPORU DOSYAYA KAYDET ----
    _rapor_kaydet(sonuclar, detayli_rapor, conf_matrix, sinif_isimleri_sirali)
    
    # ---- KARMAŞIKLIK MATRİSİ GRAFİĞİ ----
    _karmasiklik_matrisi_grafigi(conf_matrix, sinif_isimleri_sirali)
    
    return sonuclar


# ============================================================
# YARDIMCI FONKSİYONLAR
# ============================================================
def _karmasiklik_matrisi_yazdir(matris, sinif_isimleri):
    """Karmaşıklık matrisini terminal'de tablo olarak gösterir."""
    
    # Başlık satırı
    baslik = "Gerçek \\ Tahmin"
    print(f"{'':>15s}", end="")
    for isim in sinif_isimleri:
        print(f"{isim:>14s}", end="")
    print()
    print("-" * (15 + 14 * len(sinif_isimleri)))
    
    # Veri satırları
    for i, isim in enumerate(sinif_isimleri):
        print(f"{isim:>15s}", end="")
        for j in range(len(sinif_isimleri)):
            deger = matris[i][j]
            print(f"{deger:>14d}", end="")
        print()


def _rapor_kaydet(sonuclar, detayli_rapor, conf_matrix, sinif_isimleri):
    """Değerlendirme sonuçlarını metin dosyasına kaydeder."""
    
    tarih = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    rapor_icerik = f"""{'='*60}
  Sağlıkta Yapay Zeka Destekli Tanı Sistemi
  Model Performans Değerlendirme Raporu
  
  Tarih: {tarih}
  Geliştiren: Ömer Ensar Şahin
{'='*60}

📊 GENEL METRİKLER
{'-'*40}
  Doğruluk  (Accuracy)  : {sonuclar['accuracy']:.2%}
  Hassasiyet (Precision) : {sonuclar['precision']:.2%}
  Duyarlılık (Recall)    : {sonuclar['recall']:.2%}
  F1-Skoru               : {sonuclar['f1_score']:.2%}
  Test Görüntü Sayısı    : {sonuclar['test_samples']}

📋 DETAYLI SINIFLANDIRMA RAPORU
{'-'*40}
{detayli_rapor}

🔢 KARMAŞIKLIK MATRİSİ
{'-'*40}
Satır: Gerçek Sınıf | Sütun: Tahmin Edilen Sınıf

"""
    
    # Karmaşıklık matrisini ekle
    baslik_satir = f"{'':>15s}"
    for isim in sinif_isimleri:
        baslik_satir += f"{isim:>14s}"
    rapor_icerik += baslik_satir + "\n"
    rapor_icerik += "-" * (15 + 14 * len(sinif_isimleri)) + "\n"
    
    for i, isim in enumerate(sinif_isimleri):
        satir = f"{isim:>15s}"
        for j in range(len(sinif_isimleri)):
            satir += f"{conf_matrix[i][j]:>14d}"
        rapor_icerik += satir + "\n"
    
    rapor_icerik += f"\n{'='*60}\n"
    rapor_icerik += "Bu rapor otomatik olarak evaluate.py tarafından üretilmiştir.\n"
    
    # Dosyaya yaz
    with open(EVALUATION_REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write(rapor_icerik)
    
    print(f"\n💾 Rapor kaydedildi: {EVALUATION_REPORT_PATH}")


def _karmasiklik_matrisi_grafigi(conf_matrix, sinif_isimleri):
    """Karmaşıklık matrisini görsel grafik olarak kaydeder."""
    
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Isı haritası (heatmap)
        im = ax.imshow(conf_matrix, interpolation='nearest', cmap='Blues')
        ax.figure.colorbar(im, ax=ax)
        
        # Etiketler
        ax.set(
            xticks=np.arange(len(sinif_isimleri)),
            yticks=np.arange(len(sinif_isimleri)),
            xticklabels=sinif_isimleri,
            yticklabels=sinif_isimleri,
            ylabel='Gerçek Sınıf',
            xlabel='Tahmin Edilen Sınıf',
            title='Karmaşıklık Matrisi (Confusion Matrix)',
        )
        
        # Eksenleri döndür (okunabilirlik için)
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
        
        # Hücre değerlerini göster
        thresh = conf_matrix.max() / 2.0
        for i in range(len(sinif_isimleri)):
            for j in range(len(sinif_isimleri)):
                ax.text(
                    j, i, format(conf_matrix[i, j], 'd'),
                    ha="center", va="center",
                    color="white" if conf_matrix[i, j] > thresh else "black",
                    fontsize=14, fontweight='bold',
                )
        
        plt.tight_layout()
        
        grafik_yolu = os.path.join(
            os.path.dirname(EVALUATION_REPORT_PATH),
            "confusion_matrix.png"
        )
        plt.savefig(grafik_yolu, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"📊 Karmaşıklık matrisi grafiği kaydedildi: {grafik_yolu}")
        
    except ImportError:
        print("⚠️  matplotlib yüklü değil, grafik oluşturulamadı.")


# ============================================================
# ÇALIŞTIRMA
# ============================================================
if __name__ == "__main__":
    print()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║    🩺 Sağlıkta Yapay Zeka Destekli Tanı Sistemi        ║")
    print("║    📊 Model Değerlendirme Scripti                       ║")
    print("║    👨‍💻 Geliştiren: Ömer Ensar Şahin                     ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()
    
    try:
        sonuclar = modeli_degerlendir()
        
        print(f"\n✅ Değerlendirme tamamlandı!")
        print(f"   Sonuçlar {EVALUATION_REPORT_PATH} dosyasına kaydedildi.")
        
    except FileNotFoundError as e:
        print(f"\n{e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Beklenmeyen hata: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
