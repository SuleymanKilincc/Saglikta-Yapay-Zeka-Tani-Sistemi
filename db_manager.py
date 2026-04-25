import psycopg2
from psycopg2.extras import RealDictCursor
import uuid

# Esmanur'un PostgreSQL bağlantı bilgileri (Burayı kendi şifrenle güncelle)
DB_CONFIG = {
    "dbname": "saglik_ai",
    "user": "postgres",
    "password": "YOUR_PASSWORD", # Süleyman buraya kendi şifreni yaz
    "host": "localhost",
    "port": "5432"
}

def sonuclari_kaydet(hasta_adi, teshis, guven_skoru):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        # 1. Önce hastayı ekleyelim (Basitlik için her seferinde yeni hasta gibi veya TC ile kontrol edilebilir)
        # Esmanur'un şemasına göre TC No gerekli. Şimdilik rastgele bir TC atayalım.
        tc_no = str(uuid.uuid4().int)[:11]
        cur.execute(
            "INSERT INTO patients (tc_no, first_name, last_name, birth_date, gender) VALUES (%s, %s, %s, %s, %s) RETURNING patient_id",
            (tc_no, hasta_adi, "Belirtilmedi", "2000-01-01", "O")
        )
        patient_id = cur.fetchone()[0]

        # 2. Muayene (Study) kaydı
        cur.execute(
            "INSERT INTO studies (patient_id, referring_physician) VALUES (%s, %s) RETURNING study_id",
            (patient_id, "Yapay Zeka Sistemi")
        )
        study_id = cur.fetchone()[0]

        # 3. AI Teşhis kaydı
        cur.execute(
            "INSERT INTO ai_diagnoses (image_id, model_name, prediction_label, confidence_score) VALUES (NULL, %s, %s, %s)",
            ("X-Ray-CNN-v1", teshis, guven_skoru)
        )

        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Veritabanı hatası: {e}")
        return False
