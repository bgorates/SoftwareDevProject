import hashlib
import string
import secrets
from passlib.context import CryptContext
import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
SECRET_KEY = os.getenv("KEY")
algorithm = "HS256"
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 2525))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")



def hash_password(password: str) -> str:
    prehash = hashlib.sha256(password.encode()).digest()
    return pwd_context.hash(prehash)


def verify_password(password: str, hash: str) -> bool:
    prehash = hashlib.sha256(password.encode()).digest()
    return pwd_context.verify(prehash, hash)

def generate_temporary_password():
    alphabet = string.ascii_letters + string.digits + string.punctuation
    temporary = ''.join(secrets.choice(alphabet) for _ in range(12))
    return temporary
