import os
from dotenv import load_dotenv

# Carrega as variáveis de segurança do arquivo .env
load_dotenv()

IMAP_SERVER = os.getenv("EMAIL_HOST")
EMAIL_ACCOUNT = os.getenv("EMAIL_USER")
PASSWORD = os.getenv("EMAIL_PASS")

# Proteção de falha rápida (Fail-fast)
if not all([IMAP_SERVER, EMAIL_ACCOUNT, PASSWORD]):
    raise ValueError("ERRO CRÍTICO: Configure o arquivo .env com suas credenciais.")
