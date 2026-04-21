function analizBaslat() {
    const patientName = document.getElementById('patient-name').value;
    const fileInput = document.getElementById('xray-upload');
    
    if (patientName.trim() === "") { alert("Lütfen hasta adını girin!"); return; }
    if (fileInput.files.length === 0) { alert("Lütfen bir röntgen seçin!"); return; }

    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('result-section').classList.add('hidden');

    setTimeout(() => {
        document.getElementById('loading').classList.add('hidden');
        sonucGoster(patientName, "Pnömoni (Zatürre) Şüphesi", 87.5);
    }, 2000);
}

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