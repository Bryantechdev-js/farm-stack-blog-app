import os
import random
import string
from datetime import datetime, timedelta
from app.db.mongo import db
import asyncio
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "")
SENDER_NAME = os.getenv("SENDER_NAME", "Blog System")

async def generate_otp() -> str:
    """Generate a 6-digit OTP"""
    return ''.join(random.choices(string.digits, k=6))

async def send_otp_email(email: str) -> str:
    """
    Generate OTP and send it via email.
    Falls back to console logging if email is not configured.
    """
    try:
        otp = await generate_otp()
        
        # Store OTP in database with 10-minute expiration
        await db.otp_tokens.update_one(
            {"email": email},
            {
                "$set": {
                    "email": email,
                    "otp": otp,
                    "created_at": datetime.utcnow(),
                    "expires_at": datetime.utcnow() + timedelta(minutes=10)
                }
            },
            upsert=True
        )
        
        print(f"[EMAIL] OTP generated for {email}: {otp}")
        
        # Try to send email if configured
        if SMTP_USER and SMTP_PASSWORD and SENDER_EMAIL:
            try:
                await send_email(
                    to_email=email,
                    subject="Password Reset OTP",
                    body=f"""
                    <html>
                        <body style="font-family: Arial, sans-serif;">
                            <h2>Password Reset Request</h2>
                            <p>You requested to reset your password. Use the OTP below:</p>
                            <h1 style="color: #007bff; letter-spacing: 5px;">{otp}</h1>
                            <p>This OTP will expire in 10 minutes.</p>
                            <p>If you didn't request this, please ignore this email.</p>
                            <hr>
                            <p style="color: #666; font-size: 12px;">Do not share this OTP with anyone.</p>
                        </body>
                    </html>
                    """
                )
                print(f"[EMAIL] OTP email sent to {email}")
            except Exception as e:
                print(f"[EMAIL] Failed to send email: {str(e)}")
                print(f"[EMAIL] OTP for testing: {otp}")
        else:
            print(f"[EMAIL] Email not configured. OTP for testing: {otp}")
        
        return otp
    except Exception as e:
        print(f"[EMAIL] Error generating OTP: {str(e)}")
        raise

async def send_email(to_email: str, subject: str, body: str) -> bool:
    """Send email using SMTP (runs in thread pool to avoid blocking)"""
    try:
        import smtplib
        
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
        message["To"] = to_email
        
        # Attach HTML body
        part = MIMEText(body, "html")
        message.attach(part)
        
        # Run SMTP in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        
        def send_smtp():
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_USER, SMTP_PASSWORD)
                server.sendmail(SENDER_EMAIL, to_email, message.as_string())
        
        await loop.run_in_executor(None, send_smtp)
        return True
    except Exception as e:
        print(f"[EMAIL] SMTP Error: {str(e)}")
        raise

async def verify_otp(email: str, otp: str) -> bool:
    """Verify OTP and check if it's not expired"""
    try:
        otp_record = await db.otp_tokens.find_one({"email": email})
        
        if not otp_record:
            return False
        
        # Check if OTP matches
        if otp_record.get("otp") != otp:
            return False
        
        # Check if OTP is expired
        if datetime.utcnow() > otp_record.get("expires_at"):
            return False
        
        return True
    except Exception as e:
        print(f"[EMAIL] Error verifying OTP: {str(e)}")
        return False

async def delete_otp(email: str):
    """Delete OTP after successful verification"""
    try:
        await db.otp_tokens.delete_one({"email": email})
    except Exception as e:
        print(f"[EMAIL] Error deleting OTP: {str(e)}")
