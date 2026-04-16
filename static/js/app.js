async function generateMusic() {
    const prompt = document.getElementById('prompt').value;
    const voice = document.getElementById('voiceSelect').value;
    const style = document.getElementById('styleSelect').value;

    try {
        let t = await fetch("/api/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                model: "FUZZ-0.8",
                prompt: prompt,
                voice: voice,
                style: style
            })
        });
        
        const res = await t.json();
        if(res.status === 'success') {
            addToLibrary(res);
        }
    } catch (e) {
        console.error("Invisible guardrail: Request handled gracefully.", e);
    }
}

function addToLibrary(item) {
    const list = document.getElementById('libraryList');
    const div = document.createElement('div');
    div.className = 'library-item';
    div.innerHTML = `<span>${item.id}</span> <a href="${item.url}" download>Download MP3/WAV</a>`;
    list.appendChild(div);
}

function surpriseMe() {
    const styles = ['Cyberpunk', 'Heavy Metal', 'Classical Chill', 'Tropical House'];
    document.getElementById('styleSelect').value = styles[Math.floor(Math.random() * styles.length)];
    generateMusic();
}

async function edit(action) {
    // Implementation for extension, cover, or vocal-swapping
    console.log("Editing action:", action);
}