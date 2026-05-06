import psycopg2
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "dbname": "saglik_ai",
    "user": "postgres",
    "password": os.getenv("DB_PASSWORD"),
    "host": "localhost",
    "port": "5432"
}

def veritabani_kur():
    """
    Uygulama ilk calıstigında tabloları otomatik olusturur.
    Tablolar zaten varsa hata vermez (IF NOT EXISTS).
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
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


def sonuclari_kaydet(hasta_adi, teshis, guven_skoru):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        tc_no = str(uuid.uuid4().int)[:11]
        cur.execute(
            "INSERT INTO patients (tc_no, first_name, last_name, birth_date, gender) VALUES (%s, %s, %s, %s, %s) RETURNING patient_id",
            (tc_no, hasta_adi, "Belirtilmedi", "2000-01-01", "O")
        )
        patient_id = cur.fetchone()[0]

        cur.execute(
            "INSERT INTO studies (patient_id, referring_physician) VALUES (%s, %s) RETURNING study_id",
            (patient_id, "Yapay Zeka Sistemi")
        )
        study_id = cur.fetchone()[0]

        cur.execute(
            "INSERT INTO ai_diagnoses (image_id, model_name, prediction_label, confidence_score) VALUES (NULL, %s, %s, %s)",
            ("X-Ray-CNN-v1", teshis, guven_skoru)
        )

        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Veritabani hatasi: {e}")
        return False
