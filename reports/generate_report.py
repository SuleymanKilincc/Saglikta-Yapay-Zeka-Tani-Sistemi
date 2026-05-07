# -*- coding: utf-8 -*-
"""
============================================================
  Sağlıkta Yapay Zeka Destekli Tanı Sistemi
  Raporlama Modülü
  
  Geliştiren: Zeynep Karataş
  Modül: reports/generate_report.py
============================================================
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph,
    Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import os

# ──────────────────────────────────────────
# TÜRKÇE KARAKTER DESTEKLİ FONT AYARI
# ──────────────────────────────────────────
FONT_NORMAL = "Arial"
FONT_BOLD = "Arial-Bold"

try:
    # Windows için varsayılan Arial yolları
    pdfmetrics.registerFont(TTFont(FONT_NORMAL, "C:/Windows/Fonts/arial.ttf"))
    pdfmetrics.registerFont(TTFont(FONT_BOLD, "C:/Windows/Fonts/arialbd.ttf"))
except:
    # Eğer font bulunamazsa standart fontlara döner (Türkçe karakter sorunu olabilir)
    FONT_NORMAL = "Helvetica"
    FONT_BOLD = "Helvetica-Bold"

def rapor_olustur(hasta_adi, sonuc_yuzdesi, teshis_adi="Belirlenmedi",
                  dosya_adi="rapor.pdf", doktor_adi="Belirtilmedi",
                  departman="Radyoloji", goruntu_adi="Belirtilmedi",
                  doktor_notu="", model_surumu="MobileNetV2"):
    """
    Hasta bilgilerini ve AI sonuçlarını alarak PDF rapor üretir.
    """
    # Klasör yoksa oluştur
    klasor = os.path.dirname(dosya_adi)
    if klasor:
        os.makedirs(klasor, exist_ok=True)

    doc = SimpleDocTemplate(
        dosya_adi,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm
    )

    stiller = getSampleStyleSheet()
    
    # Özel Stiller
    baslik_stili = ParagraphStyle(
        "Baslik", parent=stiller["Title"], fontName=FONT_BOLD, fontSize=20,
        textColor=colors.HexColor("#1a3c5e"), alignment=1, spaceAfter=12
    )

    etiket_stili = ParagraphStyle(
        "Etiket", parent=stiller["Normal"], fontName=FONT_NORMAL, fontSize=10, textColor=colors.grey
    )

    deger_stili = ParagraphStyle(
        "Deger", parent=stiller["Normal"], fontName=FONT_NORMAL, fontSize=12, textColor=colors.black
    )

    # Yüzdeyi ayarla
    yuzde = round(sonuc_yuzdesi * 100, 1) if sonuc_yuzdesi <= 1 else round(sonuc_yuzdesi, 1)

    # Risk Durumu
    if teshis_adi == "Normal":
        risk_yazisi, risk_renk = "SAĞLIKLI (RİSK YOK)", "#27ae60"
    else:
        if yuzde >= 70:
            risk_yazisi, risk_renk = "YÜKSEK RİSK", "#c0392b"
        elif yuzde >= 40:
            risk_yazisi, risk_renk = "ORTA RİSK", "#e67e22"
        else:
            risk_yazisi, risk_renk = "DÜŞÜK RİSK", "#27ae60"

    icerik = []
    icerik.append(Paragraph("AkciğerAI Tanı Sistemi - Analiz Raporu", baslik_stili))
    icerik.append(HRFlowable(width="100%", thickness=1, color=colors.lightgrey))
    icerik.append(Spacer(1, 0.6 * cm))

    # Bilgi Tablosu
    tablo_verisi = [
        [Paragraph("Hasta Adı", etiket_stili),        Paragraph(hasta_adi, deger_stili)],
        [Paragraph("Doktor", etiket_stili),            Paragraph(doktor_adi, deger_stili)],
        [Paragraph("Departman", etiket_stili),         Paragraph(departman, deger_stili)],
        [Paragraph("Görüntü", etiket_stili),           Paragraph(goruntu_adi, deger_stili)],
        [Paragraph("Model", etiket_stili),             Paragraph(model_surumu, deger_stili)],
        [Paragraph("Tarih", etiket_stili),             Paragraph(datetime.now().strftime("%d.%m.%Y %H:%M"), deger_stili)],
        [Paragraph("Teşhis", etiket_stili),            Paragraph(teshis_adi, deger_stili)],
        [Paragraph("Güvenilirlik Skoru", etiket_stili), Paragraph(f"%{yuzde}", deger_stili)],
        [Paragraph("Risk Durumu", etiket_stili),       Paragraph(f"<font color='{risk_renk}'><b>{risk_yazisi}</b></font>", deger_stili)],
    ]

    tablo = Table(tablo_verisi, colWidths=[5 * cm, 12 * cm])
    tablo.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#eaf0fb")),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.grey),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))

    icerik.append(tablo)
    icerik.append(Spacer(1, 1 * cm))
    if doktor_notu:
        icerik.append(Paragraph("Doktor Notu", ParagraphStyle(
            "NotBaslik", fontName=FONT_BOLD, fontSize=11, textColor=colors.HexColor("#1a3c5e")
        )))
        icerik.append(Paragraph(doktor_notu, deger_stili))
        icerik.append(Spacer(1, 0.5 * cm))

    icerik.append(Paragraph("NOT: Bu rapor yapay zeka tarafından üretilmiştir. Kesin tanı için doktor görüşü alınız.", 
                            ParagraphStyle("Uyari", fontName=FONT_NORMAL, fontSize=9, textColor=colors.grey)))

    doc.build(icerik)
    return dosya_adi

if __name__ == "__main__":
    rapor_olustur("Ahmet Yılmaz", 0.85, "Pnömoni", "reports/ornek_rapor.pdf")
