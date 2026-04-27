from sqlalchemy.orm import Session
from app.database.models import User, AccessRequest


class ApprovalRepository:

    @staticmethod
    def approve_user(db: Session, telegram_id, role):

        user = db.query(User).filter(
            User.telegram_id == telegram_id
        ).first()

        if user:
            user.role = role

        request = db.query(AccessRequest).filter(
            AccessRequest.telegram_id == telegram_id
        ).first()

        if request:
            request.status = "approved"

        db.commit()


    @staticmethod
    def reject_user(db: Session, telegram_id):

        request = db.query(AccessRequest).filter(
            AccessRequest.telegram_id == telegram_id
        ).first()

        if request:
            request.status = "rejected"

        db.commit()


    @staticmethod
    def list_pending_requests(db: Session):

        return db.query(AccessRequest).filter(
            AccessRequest.status == "pending"
        ).all()