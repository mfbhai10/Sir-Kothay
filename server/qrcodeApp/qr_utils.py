"""Shared QR image generation (URL payload + optional center logo)."""
from io import BytesIO

import qrcode
from django.contrib.staticfiles import finders
from PIL import Image


def compose_qr_png_with_center_logo(url_to_encode: str) -> BytesIO:
    """Return a PNG buffer: QR encoding ``url_to_encode`` with optional center logo (high ECC)."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url_to_encode)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white').convert('RGBA')

    logo_path = finders.find('images/qr/inside-qr.png')
    if logo_path:
        logo = Image.open(logo_path).convert('RGBA')
        qr_width, qr_height = img.size
        logo_max = min(qr_width, qr_height) // 4
        lw, lh = logo.size
        scale = logo_max / max(lw, lh)
        nw, nh = max(1, int(lw * scale)), max(1, int(lh * scale))
        logo = logo.resize((nw, nh), Image.LANCZOS)
        overlay = Image.new('RGBA', img.size, (255, 255, 255, 0))
        pos = ((qr_width - nw) // 2, (qr_height - nh) // 2)
        overlay.paste(logo, pos, logo)
        img = Image.alpha_composite(img, overlay)

    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return buffer
