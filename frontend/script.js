async function analizBaslat() {
    const patientName = document.getElementById('patient-name').value;
    const fileInput = document.getElementById('xray-upload');

    if (patientName.trim() === "") { alert("Lütfen hasta adını girin!"); return; }
    if (fileInput.files.length === 0) { alert("Lütfen bir röntgen seçin!"); return; }

    // Yükleniyor animasyonunu göster
    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('result-section').classList.add('hidden');

    // Sunucuya (app.py) gönderilecek paketi hazırla
    const formData = new FormData();
    formData.append('xray_file', fileInput.files[0]); 
    formData.append('patient_name', patientName);

    try {
        // Flask sunucusuna POST isteği atıyoruz
        const response = await fetch('/analiz_et', {
            method: 'POST',
            body: formData
        });

        // Sunucudan gelen cevabı al
        const data = await response.json();
        
        // Yükleniyor yazısını gizle
        document.getElementById('loading').classList.add('hidden');

        if (data.basari) {
            // Ömer'in modelinden dönen GERÇEK sonucu ekrana bas
            sonucGoster(patientName, data.hastalik, (data.guven_skoru * 100).toFixed(1));
        } else {
            alert("Sunucu Hatası: " + data.hata);
        }
    } catch (error) {
        document.getElementById('loading').classList.add('hidden');
        alert("Sunucuya ulaşılamadı! app.py dosyasının çalıştığından emin olun.");
        console.error(error);
    }
}

// sonucGoster fonksiyonuna DOKUNMA, o Cumali'nin bıraktığı gibi kalsın
function sonucGoster(hastaAdi, hastalikTeshisi, guvenOrani) {
    const resultSection = document.getElementById('result-section');
    const resultContent = document.getElementById('result-content');

    resultContent.innerHTML = `
        <p><strong>Hasta:</strong> ${hastaAdi}</p>
        <p><strong>Tespit:</strong> ${hastalikTeshisi}</p>
        <p><strong>AI Güven Oranı:</strong> %${guvenOrani}</p>
    `;
    resultSection.classList.remove('hidden');
}
