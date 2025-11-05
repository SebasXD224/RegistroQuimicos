import qrcode
import os

# Ruta base donde se guardarán los QR
QR_FOLDER = os.path.join("static", "img", "QR_Codes")


def generate_qr(record_id):
    # Aquí usa tu dominio o localhost
    base_url = "http://localhost:5000/"
    qr_data = f"{base_url}#record-{record_id}"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    os.makedirs(QR_FOLDER, exist_ok=True)
    qr_filename = f"qr_{record_id}.png"
    qr_path = os.path.join(QR_FOLDER, qr_filename)
    img.save(qr_path)

    return f"img/QR_Codes/{qr_filename}"
