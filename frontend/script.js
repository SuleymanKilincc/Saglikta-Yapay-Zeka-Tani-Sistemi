// ============================================================
//  AI X-Ray Tanı Sistemi — Frontend JavaScript
//  app.py /analiz_et route'u ile tam uyumlu
// ============================================================

// Dosya seçimi olayını dinle
document.addEventListener('DOMContentLoaded', function () {
    const fileInput = document.getElementById('xray-upload');
    const uploadArea = document.getElementById('upload-area');
    const uploadText = document.getElementById('upload-text');
    const analyzeBtn = document.getElementById('analyze-btn');
    const patientInput = document.getElementById('patient-name');

    // Dosya seçilince upload alanını güncelle
    fileInput.addEventListener('change', function () {
        if (this.files.length > 0) {
            const f = this.files[0];
            uploadText.textContent = `✅ ${f.name} (${(f.size / 1024).toFixed(1)} KB)`;
            uploadArea.classList.add('has-file');
            kontrolEt();
        }
    });

    // Hasta adı girilince butonu etkinleştir
    patientInput.addEventListener('input', kontrolEt);

    // Drag & Drop desteği
    uploadArea.addEventListener('dragover', (e) => { e.preventDefault(); uploadArea.style.borderColor = 'var(--blue)'; });
    uploadArea.addEventListener('dragleave', () => { uploadArea.style.borderColor = ''; });
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '';
        if (e.dataTransfer.files.length > 0) {
            fileInput.files = e.dataTransfer.files;
            const f = e.dataTransfer.files[0];
            uploadText.textContent = `✅ ${f.name} (${(f.size / 1024).toFixed(1)} KB)`;
            uploadArea.classList.add('has-file');
            kontrolEt();
        }
    });

    function kontrolEt() {
        const dolu = patientInput.value.trim() !== '' && fileInput.files.length > 0;
        analyzeBtn.disabled = !dolu;
    }
});

// ── Durum Yönetimi ──────────────────────────────────────────
function durumGoster(id) {
    ['idle-state', 'loading-state', 'result-state', 'error-state'].forEach(s => {
        document.getElementById(s).classList.add('hidden');
    });
    document.getElementById(id).classList.remove('hidden');
}

function tekrarDene() {
    durumGoster('idle-state');
}

// ── Yükleniyor Adım Animasyonu ───────────────────────────────
let stepTimer = null;
function adimAnimasyonBaslat() {
    const steps = ['step-1', 'step-2', 'step-3'];
    let i = 0;
    steps.forEach(s => {
        const el = document.getElementById(s);
        el.classList.remove('active', 'done');
    });
    document.getElementById('step-1').classList.add('active');
    i = 1;
    stepTimer = setInterval(() => {
        if (i > 0) document.getElementById(steps[i - 1]).classList.replace('active', 'done');
        if (i < steps.length) {
            document.getElementById(steps[i]).classList.add('active');
            i++;
        } else {
            clearInterval(stepTimer);
        }
    }, 1800);
}

function adimAnimasyonDurdur() {
    if (stepTimer) clearInterval(stepTimer);
}

// ── Ana Analiz Fonksiyonu ─────────────────────────────────────
async function analizBaslat() {
    const patientName = document.getElementById('patient-name').value.trim();
    const fileInput = document.getElementById('xray-upload');

    // Validasyon
    if (!patientName) { alert('Lütfen hasta adını girin!'); return; }
    if (fileInput.files.length === 0) { alert('Lütfen bir röntgen görüntüsü seçin!'); return; }

    // Yükleniyor durumu
    durumGoster('loading-state');
    adimAnimasyonBaslat();

    // Buton devre dışı
    const btn = document.getElementById('analyze-btn');
    btn.disabled = true;
    btn.classList.add('loading');
    document.getElementById('btn-text').textContent = 'Analiz Ediliyor...';

    // FormData — app.py'deki alan adlarıyla TAM uyumlu:
    //   request.files['xray_file']
    //   request.form.get('hasta_adi')
    const formData = new FormData();
    formData.append('xray_file', fileInput.files[0]);   // app.py L27: request.files['xray_file']
    formData.append('hasta_adi', patientName);           // app.py L28: request.form.get('hasta_adi')

    try {
        const response = await fetch('/analiz_et', {
            method: 'POST',
            body: formData
            // Content-Type header'ı EKLEME: multipart/form-data boundary'yi
            // tarayıcı otomatik ayarlar, elle eklerseniz boundary eksik kalır.
        });

        adimAnimasyonDurdur();

        if (!response.ok) {
            throw new Error(`Sunucu HTTP ${response.status} döndürdü.`);
        }

        const data = await response.json();

        if (data.basari) {
            sonucGoster(patientName, data);
        } else {
            hataGoster(data.hata || 'Sunucudan bilinmeyen hata döndü.');
        }

    } catch (error) {
        adimAnimasyonDurdur();
        const mesaj = error.message.includes('Failed to fetch')
            ? 'Flask sunucusuna ulaşılamadı. app.py\'nin çalıştığından emin olun (python app.py).'
            : error.message;
        hataGoster(mesaj);
        console.error('[AI Tanı]', error);
    } finally {
        btn.disabled = false;
        btn.classList.remove('loading');
        document.getElementById('btn-text').textContent = 'Analiz Et';
    }
}

// ── Sonuç Göster ─────────────────────────────────────────────
function sonucGoster(hastaAdi, data) {
    durumGoster('result-state');

    // Hasta adı
    document.getElementById('result-patient-name').textContent = hastaAdi;

    // Hastalık & ikon
    const hastalik = data.hastalik || '—';
    document.getElementById('diagnosis-name').textContent = hastalik;
    document.getElementById('diagnosis-desc').textContent = data.aciklama || '';

    // Renk sınıfı
    const diagName = document.getElementById('diagnosis-name');
    diagName.className = 'diagnosis-name';
    if (hastalik === 'Normal') { diagName.classList.add('diag-normal'); document.getElementById('result-icon').textContent = '✅'; }
    else if (hastalik === 'Pnömoni') { diagName.classList.add('diag-pnemoni'); document.getElementById('result-icon').textContent = '⚠️'; }
    else { diagName.classList.add('diag-tuberculoz'); document.getElementById('result-icon').textContent = '🔴'; }

    // Güven skoru
    const guven = data.guven_skoru || 0;
    const guvenYuzde = (guven * 100).toFixed(1);
    document.getElementById('confidence-value').textContent = `%${guvenYuzde}`;
    setTimeout(() => {
        document.getElementById('confidence-bar').style.width = `${guvenYuzde}%`;
        // Renk
        const bar = document.getElementById('confidence-bar');
        if (guven >= 0.7) bar.style.background = 'linear-gradient(90deg, #10b981, #059669)';
        else if (guven >= 0.4) bar.style.background = 'linear-gradient(90deg, #f59e0b, #d97706)';
        else bar.style.background = 'linear-gradient(90deg, #ef4444, #dc2626)';
    }, 100);

    // Demo uyarısı
    const demoWarning = document.getElementById('demo-warning');
    if (data.demo_modu) demoWarning.classList.remove('hidden');
    else demoWarning.classList.add('hidden');

    // PDF raporu
    const downloadBtn = document.getElementById('download-btn');
    if (data.rapor_url) {
        downloadBtn.href = data.rapor_url;
        downloadBtn.classList.remove('hidden');
    } else {
        downloadBtn.classList.add('hidden');
    }
}

// ── Hata Göster ──────────────────────────────────────────────
function hataGoster(mesaj) {
    durumGoster('error-state');
    document.getElementById('error-msg').textContent = mesaj;
}
