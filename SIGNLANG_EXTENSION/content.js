console.log("SignLang: Integration Active");

const overlay = document.createElement('div');
overlay.style.cssText = `
    position: fixed; top: 20px; left: 50%; transform: translateX(-50%);
    background: rgba(0, 0, 0, 0.8); color: #00FF00; padding: 20px;
    border-radius: 10px; font-size: 30px; font-weight: bold;
    z-index: 999999; border: 3px solid #00FF00; display: none;
`;
document.body.appendChild(overlay);

async function poll() {
    try {
        // Fetching from localhost often works better than 127.0.0.1 in Chrome
        const res = await fetch('http://localhost:5000/gesture');
        const data = await res.json();
        
        if (data.gesture && data.gesture !== "NONE" && data.gesture !== "WAITING") {
            overlay.style.display = "block";
            overlay.innerText = "Signing: " + data.gesture;
        } else {
            overlay.style.display = "none";
        }
    } catch (err) {
        console.log("SignLang: Backend not reached yet...");
    }
}
setInterval(poll, 500);