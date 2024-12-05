from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Email configuration from environment variables
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')





def send_email(recipient: str, subject: str, body: str):
    try:
        # Create message
        message = MIMEMultipart()
        message['From'] = SENDER_EMAIL
        message['To'] = recipient
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        # Establish secure connection
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(message)
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

# Example .env file contents
# SMTP_SERVER=smtp.gmail.com
# SMTP_PORT=587
# SENDER_EMAIL=your_email@gmail.com
# SENDER_PASSWORD=your_app_password