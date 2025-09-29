import asyncio
from fastapi_mail import FastMail, MessageSchema, MessageType
from pathlib import Path
from typing import Dict
from io import BytesIO
from config import mail_config
from utils.qrcode_utils import generate_qrcode_image_in_memory
from models import sale_model

async def send_confirmation_email_async(recipient_email: str, email_data: Dict, qrcode_buffer: BytesIO):
    html_content = Path("templates/email_confirmation.html").read_text(encoding="utf-8")
    
    attachment_data = qrcode_buffer.read()
    
    message = MessageSchema(
        subject="Seu Ingresso Uai-Festas!",
        recipients=[recipient_email],
        body=html_content.format(**email_data),
        subtype=MessageType.html,
        attachments=[{
            "file": attachment_data,
            "headers": {
                "Content-ID": "<qrcode_image>",
                "Content-Disposition": "inline; filename=\"qrcode.png\""
            },
            "mime_type": "image",
            "mime_subtype": "png"
        }]
    )
    
    fm = FastMail(mail_config)
    await fm.send_message(message)

def send_confirmation_email_sync(recipient_email: str, email_data: Dict, qrcode_buffer: BytesIO):
    asyncio.run(send_confirmation_email_async(recipient_email, email_data, qrcode_buffer))

def formated_email_to_send(sale: sale_model.Sale):
    try:
        qrcode_buffer = generate_qrcode_image_in_memory(str(sale.unique_code))
            
        formatted_date = sale.product.event.event_date.strftime("%d de %B de %Y às %H:%M")
            
        formatted_price = f"R$ {sale.product.price:.2f}".replace('.', ',')
            
        email_data = {
            "buyer_name": sale.buyer_name,
            "event_name": sale.product.event.name,
            "product_name": sale.product.name,
            "event_date": formatted_date,
            "event_location": f"{sale.product.event.street}, {sale.product.event.number} - {sale.product.event.city}",
            "product_price": formatted_price
        }
        
        send_confirmation_email_sync(
            recipient_email=sale.buyer_email,
            email_data=email_data,
            qrcode_buffer=qrcode_buffer
        )
    except Exception as e:
        print(f"ERRO AO ENVIAR EMAIL: {e}")