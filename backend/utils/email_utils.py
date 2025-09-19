import asyncio
from fastapi_mail import FastMail, MessageSchema, MessageType
from pathlib import Path
from typing import Dict
from io import BytesIO
from config import mail_config

async def send_confirmation_email_async(recipient_email: str, email_data: Dict, qrcode_filepath: str):
    html_content = Path("templates/email_confirmation.html").read_text(encoding=("utf-8"))
    
    attachment = {
        "file": qrcode_filepath,  
        "headers": {
            "Content-ID": "<qrcode_image>",
            "Content-Disposition": f"inline; filename=\"qrcode.png\""
        },
        "mime_type": "image",
        "mime_subtype": "png"
    }
    
    message = MessageSchema(
        subject="Seu Ingresso Uai-Festas!",
        recipients=[recipient_email],
        body=html_content.format(**email_data),
        subtype=MessageType.html,
        attachments=[attachment]
    )
    
    fm = FastMail(mail_config)
    await fm.send_message(message)

def send_confirmation_email_sync(recipient_email: str, email_data: Dict, qrcode_buffer: BytesIO):
    asyncio.run(send_confirmation_email_async(recipient_email, email_data, qrcode_buffer))
