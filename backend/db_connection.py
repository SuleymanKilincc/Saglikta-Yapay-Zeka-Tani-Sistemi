from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Bağlantı Bilgileri (Localhost üzerinde PostgreSQL kurulu olmalı)
DB_USER = "postgres"
DB_PASS = "sifreniz" # Burayı Esmanur kendi şifresiyle değiştirmeli
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "xray_db"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Engine Oluşturma
engine = create_engine(DATABASE_URL)

# Session Sınıfı
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Veritabanı Modelleri için Base Sınıf
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        print("Veritabanına başarıyla bağlanıldı (SQLAlchemy).")
        return db
    except Exception as e:
        print(f"Bağlantı hatası oluştu: {e}")
    finally:
        db.close()

# Test için:
if __name__ == "__main__":
    db = get_db()
