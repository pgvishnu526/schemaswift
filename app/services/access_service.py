from sqlalchemy.orm import Session
from app.repositories.access_repository import AccessRepository
from app.repositories.log_repository import LogRepository
from app.repositories.user_repository import UserRepository
from app.config import settings
from rag.index_builder import update_user_embeddings as update_embeddings

import smtplib
import logging
import threading
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)


def send_admin_notification_email(telegram_id: int, name: str):
    """
    Sends access request email to admin
    """

    approve_viewer_url = (
        f"{settings.APP_BASE_URL}/approve?"
        f"uid={telegram_id}&role=viewer"
    )

    approve_admin_url = (
        f"{settings.APP_BASE_URL}/approve?"
        f"uid={telegram_id}&role=admin"
    )

    reject_url = (
        f"{settings.APP_BASE_URL}/reject?"
        f"uid={telegram_id}"
    )

    body = f"""
New access request from SchemaSwift

Name: {name}
Telegram ID: {telegram_id}

Approve Viewer:
{approve_viewer_url}

Approve Admin:
{approve_admin_url}

Reject:
{reject_url}
"""

    msg = MIMEText(body)

    msg["Subject"] = "New Access Request - SchemaSwift"
    msg["From"] = settings.SMTP_EMAIL
    msg["To"] = settings.ADMIN_EMAIL

    try:
        with smtplib.SMTP_SSL(
            settings.SMTP_SERVER,
            settings.SMTP_PORT
        ) as server:

            server.login(
                settings.SMTP_EMAIL,
                settings.SMTP_PASSWORD
            )

            server.send_message(msg)

    except Exception as e:
        logger.error(f"Email sending failed: {e}")


class AccessService:

    @staticmethod
    def request_access(db: Session, telegram_id: int, name: str):
        """
        Creates access request + logs action + emails admin
        """

        # Ensure user exists before creating access request or logging
        user = UserRepository.get_user(
            db,
            telegram_id
        )

        if not user:
            user = UserRepository.create_user(
                db,
                telegram_id,
                name=name
            )

        # Create request
        request = AccessRepository.request_access(
            db,
            telegram_id
        )

        # Log activity
        LogRepository.log(
            db,
            telegram_id,
            "Requested access upgrade"
        )

        update_embeddings()

        # Send email notification in a background thread to prevent blocking
        threading.Thread(
            target=send_admin_notification_email,
            args=(telegram_id, name),
            daemon=True
        ).start()

        return (
            "Access request sent to the main admin successfully 📩\n"
            "Approval usually takes a few minutes.\n"
            "You can check your role anytime by typing: 'What is my role?'"
        )