import qrcode
import io
import os
from uuid import uuid4
from pathlib import Path

TEMP_DIR = "temp_qrcodes"

def generate_qrcode_image_in_memory(data: str):
    
    qr = qrcode.QRCode(
        version=1, 
        error_correction=qrcode.constants.ERROR_CORRECT_L, 
        box_size=10, 
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    
    return buffer

def generate_qrcode_image_file(data: str):
    """Generate QR code and save to file, return file path"""
    # Ensure temp directory exists
    temp_dir = Path(TEMP_DIR)
    temp_dir.mkdir(exist_ok=True)
    
    # Generate unique filename
    filename = f"qr_{uuid4().hex}.png"
    filepath = temp_dir / filename
    
    qr = qrcode.QRCode(
        version=1, 
        error_correction=qrcode.constants.ERROR_CORRECT_L, 
        box_size=10, 
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save to file
    img.save(filepath, format="PNG")
    
    return str(filepath)