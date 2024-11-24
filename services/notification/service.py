import smtplib, os, json
from email.message import EmailMessage
from dotenv import load_dotenv
from email.mime.text import MIMEText


load_dotenv()


# Email configuration from environment variables
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')

def notification(message):
    try:
        message = json.loads(message)
        receiver_address = message["email"]
        subject = message["subject"]
        body = message["body"]
        other = message["other"]

        print("SMTP_SERVER: ", SMTP_SERVER)
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        
        # Compose the email message
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = receiver_address

        server.sendmail(SENDER_EMAIL, receiver_address, msg.as_string())
        server.quit()

        print("Mail Sent")
    except Exception as e:
        print(f"Failed to send email: {e}")