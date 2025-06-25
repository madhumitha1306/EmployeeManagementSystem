from email.message import EmailMessage
import aiosmtplib
import ssl

SMTP_HOST = "smtp.mailtrap.io"
SMTP_PORT = 587
SMTP_USERNAME = "d11f69d5096a19"
SMTP_PASSWORD = "3a9dd85b125a40"
FROM_EMAIL = "noreply@example.com"

async def send_email(to_email: str, subject: str, body: str):
    message = EmailMessage()
    message["From"] = FROM_EMAIL
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(body)

    # Create SSL context that skips certificate verification
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    await aiosmtplib.send(
        message,
        hostname=SMTP_HOST,
        port=SMTP_PORT,
        username=SMTP_USERNAME,
        password=SMTP_PASSWORD,
        start_tls=True,
        tls_context=context,  # <-- Add this line
    )
