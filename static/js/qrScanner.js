const video = document.getElementById("video");
const result = document.getElementById("result");

navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } })
  .then(stream => {
    video.srcObject = stream;
    video.setAttribute("playsinline", true);
    video.play();
    requestAnimationFrame(tick);
  })
  .catch(err => {
    result.textContent = "❌ No se pudo acceder a la cámara: " + err.message;
  });

function tick() {
  if (video.readyState === video.HAVE_ENOUGH_DATA) {
    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const code = jsQR(imageData.data, canvas.width, canvas.height, { inversionAttempts: "dontInvert" });

    if (code) {
      const qrText = code.data.trim();
      result.textContent = "✅ Código detectado: " + qrText;

      // Enviar el valor escaneado al servidor Flask
      fetch("/process_qr", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ qr_text: qrText })
      })
      .then(res => res.json())
      .then(data => {
          if (data.success) {
              window.location.href = data.redirect_url;
          } else {
              alert("Registro no encontrado");
          }
      })
      .catch(err => console.error(err));

      return; // detener escaneo
    }
  }
  requestAnimationFrame(tick);
}