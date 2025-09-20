import qrcode
import io
import os
from uuid import uuid4

TEMP_DIR = "temp_qrcodes"

def generate_qrcode_image_in_memory(data: str):
    os.makedirs(TEMP_DIR, exist_ok=True)
    
    qr = qrcode.QRCode(
        version=1, 
        error_correction=qrcode.constants.ERROR_CORRECT_L, 
        box_size=10, 
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    filename = f"{str(uuid4())}.png"
    filepath = os.path.join(TEMP_DIR, filename)
    
    img.save(filepath)
    
    return filepath