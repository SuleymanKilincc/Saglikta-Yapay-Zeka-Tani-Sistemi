-- 1. Uzantıları Etkinleştir (UUID üretimi için)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 2. Hastalar Tablosu
CREATE TABLE patients (
    patient_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tc_no VARCHAR(11) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    birth_date DATE NOT NULL,
    gender CHAR(1) CHECK (gender IN ('M', 'F', 'O')),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Çalışmalar/Muayeneler Tablosu
CREATE TABLE studies (
    study_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id UUID REFERENCES patients(patient_id) ON DELETE CASCADE,
    study_date TIMESTAMPTZ DEFAULT NOW(),
    modality VARCHAR(10) DEFAULT 'X-RAY',
    accession_number VARCHAR(20) UNIQUE,
    referring_physician VARCHAR(100)
);

-- 4. Görüntü Meta Verileri Tablosu
CREATE TABLE images (
    image_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    study_id UUID REFERENCES studies(study_id) ON DELETE CASCADE,
    file_path TEXT NOT NULL,
    image_type VARCHAR(50),
    resolution_x INTEGER,
    resolution_y INTEGER,
    dicom_metadata JSONB,
    uploaded_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. Yapay Zeka Teşhis Sonuçları Tablosu
CREATE TABLE ai_diagnoses (
    diagnosis_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    image_id UUID REFERENCES images(image_id) ON DELETE CASCADE,
    model_name VARCHAR(50) NOT NULL,
    prediction_label VARCHAR(100),
    confidence_score DECIMAL(5, 4),
    bounding_boxes JSONB,
    processed_at TIMESTAMPTZ DEFAULT NOW()
);

-- 6. Raporlar Tablosu
CREATE TABLE reports (
    report_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    study_id UUID REFERENCES studies(study_id) ON DELETE CASCADE,
    content TEXT,
    is_approved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 7. İndeksler
CREATE INDEX idx_patients_tc ON patients(tc_no);
CREATE INDEX idx_studies_patient_id ON studies(patient_id);
CREATE INDEX idx_images_study_id ON images(study_id);
CREATE INDEX idx_ai_results_image_id ON ai_diagnoses(image_id);
CREATE INDEX idx_images_metadata_gin ON images USING GIN (dicom_metadata);
