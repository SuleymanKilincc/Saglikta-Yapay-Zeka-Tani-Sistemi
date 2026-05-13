import psycopg2
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

# Railway'de DATABASE_URL kullan, yoksa lokal config
DATABASE_URL = os.getenv("DATABASE_URL")

DB_CONFIG = {
    "dbname":   os.getenv("DB_NAME", "saglik_ai"),
    "user":     os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD"),
    "host":     os.getenv("DB_HOST", "localhost"),
    "port":     os.getenv("DB_PORT", "5432")
}

def _baglan():
    """Railway DATABASE_URL varsa onu kullan, yoksa lokal DB_CONFIG."""
    if DATABASE_URL:
        return psycopg2.connect(DATABASE_URL)
    return psycopg2.connect(**DB_CONFIG)


def veritabani_kur():
    """Tablolari ilk calistirmada otomatik olusturur."""
    try:
        conn = _baglan()
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                patient_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                tc_no VARCHAR(11) UNIQUE,
                first_name VARCHAR(50),
                last_name VARCHAR(50),
                birth_date DATE,
                gender CHAR(1),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS studies (
                study_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                patient_id UUID REFERENCES patients(patient_id),
                referring_physician VARCHAR(100),
                department VARCHAR(100),
                study_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS images (
                image_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                study_id UUID REFERENCES studies(study_id),
                file_path VARCHAR(255),
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS ai_diagnoses (
                diagnosis_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                image_id UUID,
                model_name VARCHAR(100),
                prediction_label VARCHAR(50),
                confidence_score FLOAT,
                diagnosed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                report_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                diagnosis_id UUID REFERENCES ai_diagnoses(diagnosis_id),
                report_path VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        conn.commit()
        cur.close()
        conn.close()
        print("Veritabani tablolari hazir.")
        return True
    except Exception as e:
        print(f"Veritabani kurulum hatasi: {e}")
        print("PostgreSQL kurulu ve 'saglik_ai' veritabani olusturulmus olmali!")
        return False


def sonuclari_kaydet(hasta_adi, hasta_soyadi, dogum_tarihi,
                     cinsiyet, doktor_adi, departman,
                     teshis, guven_skoru):
    """Analiz sonuclarini tum alanlariyla veritabanina kaydeder."""
    try:
        conn = _baglan()
        cur = conn.cursor()

        # TC No otomatik uretilir (11 hane rastgele sayi)
        tc_no = str(uuid.uuid4().int)[:11]

        # 1. Hasta kaydı
        cur.execute(
            """INSERT INTO patients (tc_no, first_name, last_name, birth_date, gender)
               VALUES (%s, %s, %s, %s, %s) RETURNING patient_id""",
            (tc_no, hasta_adi, hasta_soyadi or "Belirtilmedi",
             dogum_tarihi or "2000-01-01", cinsiyet or "B")
        )
        patient_id = cur.fetchone()[0]

        # 2. Muayene kaydı
        cur.execute(
            """INSERT INTO studies (patient_id, referring_physician, department)
               VALUES (%s, %s, %s) RETURNING study_id""",
            (patient_id, doktor_adi, departman)
        )
        study_id = cur.fetchone()[0]

        # 3. AI Teshis kaydı
        cur.execute(
            """INSERT INTO ai_diagnoses (image_id, model_name, prediction_label, confidence_score)
               VALUES (NULL, %s, %s, %s)""",
            ("MobileNetV2-v1", teshis, guven_skoru)
        )

        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Veritabani hatasi: {e}")
        return False
