import asyncio
from fastapi_mail import FastMail, MessageSchema, MessageType
from pathlib import Path
from typing import Dict
from config import mail_config
from models import sale_model

async def send_confirmation_email_async(recipient_email: str, email_data: Dict, qrcode_file_path: str):
    import os
    
    try:
        print(f"📧 Preparando mensagem de email para {recipient_email}")
        
        html_content = Path("templates/email_confirmation.html").read_text(encoding="utf-8")
        print(f"✅ Template HTML carregado")
        
        # Verificar se o arquivo QR code existe
        if not os.path.exists(qrcode_file_path):
            raise FileNotFoundError(f"Arquivo QR code não encontrado: {qrcode_file_path}")
        
        print(f"✅ QR Code encontrado em {qrcode_file_path}")
        
        message = MessageSchema(
            subject="Seu Ingresso Uai-Festas!",
            recipients=[recipient_email],
            body=html_content.format(**email_data),
            subtype=MessageType.html,
            attachments=[{
                "file": qrcode_file_path,
                "headers": {
                    "Content-ID": "<qrcode_image>",
                    "Content-Disposition": "inline; filename=\"qrcode.png\""
                },
                "mime_type": "image",
                "mime_subtype": "png"
            }]
        )
        print(f"✅ Mensagem preparada com sucesso")
        
        fm = FastMail(mail_config)
        print(f"📤 Enviando email via FastMail...")
        await fm.send_message(message)
        print(f"✅ Email enviado com sucesso via FastMail!")
        
    except Exception as e:
        print(f"❌ Erro no envio assíncrono: {e}")
        import traceback
        traceback.print_exc()
        raise

def send_confirmation_email_sync(recipient_email: str, email_data: Dict, qrcode_file_path: str):
    asyncio.run(send_confirmation_email_async(recipient_email, email_data, qrcode_file_path))

def formated_email_to_send(sale: sale_model.Sale):
    from .qrcode_utils import generate_qrcode_image_file
    import os
    
    qrcode_file_path = None
    try:
        print(f"📧 Iniciando envio de email para venda {sale.id}")
        print(f"📧 Email do comprador: {sale.buyer_email}")
        print(f"📧 Código único: {sale.unique_code}")
        
        qrcode_file_path = generate_qrcode_image_file(str(sale.unique_code))
        print(f"✅ QR Code gerado e salvo em {qrcode_file_path}")
            
        formatted_date = sale.product.event.event_date.strftime("%d de %B de %Y às %H:%M")
        print(f"📅 Data formatada: {formatted_date}")
            
        formatted_price = f"R$ {sale.product.price:.2f}".replace('.', ',')
        print(f"💰 Preço formatado: {formatted_price}")
            
        email_data = {
            "buyer_name": sale.buyer_name,
            "event_name": sale.product.event.name,
            "product_name": sale.product.name,
            "event_date": formatted_date,
            "event_location": f"{sale.product.event.street}, {sale.product.event.number} - {sale.product.event.city}",
            "product_price": formatted_price
        }
        
        print(f"📧 Dados do email preparados: {email_data}")
        
        send_confirmation_email_sync(
            recipient_email=sale.buyer_email,
            email_data=email_data,
            qrcode_file_path=qrcode_file_path
        )
        print(f"✅ Email enviado com sucesso para {sale.buyer_email}")
    except Exception as e:
        print(f"❌ ERRO AO ENVIAR EMAIL: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Limpar arquivo do QR code
        if qrcode_file_path and os.path.exists(qrcode_file_path):
            try:
                os.remove(qrcode_file_path)
                print(f"🧹 Arquivo QR Code {qrcode_file_path} removido")
            except Exception as cleanup_error:
                print(f"⚠️ Erro ao remover arquivo QR Code: {cleanup_error}")