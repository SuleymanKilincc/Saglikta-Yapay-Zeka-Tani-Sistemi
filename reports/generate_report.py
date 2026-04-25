# ──────────────────────────────────────────
# KÜTÜPHANE İMPORTLARI
# ──────────────────────────────────────────
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
# Windows için Arial fontu kullanılır.
# Türkçe karakterlerin bozulmaması için gereklidir.
FONT_NORMAL = "Arial"
FONT_BOLD = "Arial-Bold"

try:
    pdfmetrics.registerFont(TTFont(FONT_NORMAL, "C:/Windows/Fonts/arial.ttf"))
    pdfmetrics.registerFont(TTFont(FONT_BOLD, "C:/Windows/Fonts/arialbd.ttf"))
except:
    # Eğer Arial bulunamazsa varsayılan font kullanılır.
    FONT_NORMAL = "Helvetica"
    FONT_BOLD = "Helvetica-Bold"


# ──────────────────────────────────────────
# ANA FONKSİYON
# Girdi: hasta_adi, sonuc_yuzdesi, teshis_adi, dosya_adi
# Çıktı: oluşturulan PDF'in dosya yolu
# ──────────────────────────────────────────
def rapor_olustur(
    hasta_adi,
    sonuc_yuzdesi,
    teshis_adi="Pnömoni",
    dosya_adi="rapor.pdf"
):
    """
    Hasta adı ve teşhis yüzdesini alır, PDF rapor üretir.

    Parametreler:
        hasta_adi: Hastanın adı soyadı
        sonuc_yuzdesi: Yapay zeka güven skoru. 0.85 veya 85 şeklinde verilebilir.
        teshis_adi: Teşhis sonucu
        dosya_adi: Oluşturulacak PDF dosyasının adı

    Döndürür:
        dosya_adi: Oluşturulan PDF dosyasının yolu
    """

    # Eğer klasör yolu verilmişse klasörü oluştur
    klasor = os.path.dirname(dosya_adi)
    if klasor:
        os.makedirs(klasor, exist_ok=True)

    # PDF belgesi oluştur
    doc = SimpleDocTemplate(
        dosya_adi,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm
    )

    # Yazı stilleri
    stiller = getSampleStyleSheet()

    baslik_stili = ParagraphStyle(
        "Baslik",
        parent=stiller["Title"],
        fontName=FONT_BOLD,
        fontSize=20,
        textColor=colors.HexColor("#1a3c5e"),
        alignment=1,
        spaceAfter=12
    )

    etiket_stili = ParagraphStyle(
        "Etiket",
        parent=stiller["Normal"],
        fontName=FONT_NORMAL,
        fontSize=10,
        textColor=colors.grey
    )

    deger_stili = ParagraphStyle(
        "Deger",
        parent=stiller["Normal"],
        fontName=FONT_NORMAL,
        fontSize=12,
        textColor=colors.black
    )

    uyari_stili = ParagraphStyle(
        "Uyari",
        parent=stiller["Normal"],
        fontName=FONT_NORMAL,
        fontSize=9,
        textColor=colors.grey
    )

    # Yüzde hesaplama
    # 0.85 gelirse %85 yapar, 85 gelirse olduğu gibi kullanır.
    if sonuc_yuzdesi <= 1:
        yuzde = round(sonuc_yuzdesi * 100, 1)
    else:
        yuzde = round(sonuc_yuzdesi, 1)

    # Risk durumu belirleme
    if yuzde >= 70:
        risk_yazisi = "YÜKSEK RİSK"
        risk_renk = "#c0392b"
    elif yuzde >= 40:
        risk_yazisi = "ORTA RİSK"
        risk_renk = "#e67e22"
    else:
        risk_yazisi = "DÜŞÜK RİSK"
        risk_renk = "#27ae60"

    # PDF içeriği
    icerik = []

    icerik.append(Paragraph("AkciğerAI Tanı Sistemi", baslik_stili))
    icerik.append(HRFlowable(width="100%", thickness=1, color=colors.lightgrey))
    icerik.append(Spacer(1, 0.6 * cm))

    tablo_verisi = [
        [
            Paragraph("Hasta Adı", etiket_stili),
            Paragraph(hasta_adi, deger_stili)
        ],
        [
            Paragraph("Tarih", etiket_stili),
            Paragraph(datetime.now().strftime("%d.%m.%Y %H:%M"), deger_stili)
        ],
        [
            Paragraph("Teşhis", etiket_stili),
            Paragraph(teshis_adi, deger_stili)
        ],
        [
            Paragraph("Güvenilirlik", etiket_stili),
            Paragraph(f"%{yuzde}", deger_stili)
        ],
        [
            Paragraph("Risk Durumu", etiket_stili),
            Paragraph(
                f"<font color='{risk_renk}'><b>{risk_yazisi}</b></font>",
                deger_stili
            )
        ],
    ]

    tablo = Table(tablo_verisi, colWidths=[5 * cm, 12 * cm])

    tablo.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#eaf0fb")),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.grey),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))

    icerik.append(tablo)
    icerik.append(Spacer(1, 1 * cm))

    uyari = Paragraph(
        "Bu rapor yapay zeka tarafından üretilmiştir. "
        "Kesin tanı için uzman doktor görüşü alınız.",
        uyari_stili
    )

    icerik.append(uyari)

    # PDF oluştur
    doc.build(icerik)

    print(f"PDF oluşturuldu: {dosya_adi}")

    return dosya_adi


# ──────────────────────────────────────────
# TEST BLOĞU
# ──────────────────────────────────────────
if __name__ == "__main__":
    rapor_olustur(
        hasta_adi="Ahmet Yılmaz",
        sonuc_yuzdesi=0.85,
        teshis_adi="Pnömoni",
        dosya_adi="test_raporu.pdf"
    )