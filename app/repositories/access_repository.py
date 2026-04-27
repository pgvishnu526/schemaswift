from sqlalchemy.orm import Session
from app.database.models import AccessRequest


class AccessRepository:

    @staticmethod
    def request_access(db: Session, telegram_id):

        request = AccessRequest(
            telegram_id=telegram_id
        )

        db.add(request)
        db.commit()
        db.refresh(request)

        return request