import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:root@localhost:5432/project_db"
    )

    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
    SMTP_EMAIL = os.getenv("SMTP_EMAIL")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
    APP_BASE_URL = os.getenv("APP_BASE_URL", "http://localhost:8000")


settings = Settings()