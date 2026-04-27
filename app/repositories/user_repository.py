from sqlalchemy.orm import Session
from app.database.models import User


class UserRepository:

    @staticmethod
    def get_user(db: Session, telegram_id):
        return db.query(User).filter(
            User.telegram_id == telegram_id
        ).first()

    @staticmethod
    def create_user(db: Session, telegram_id, name, role="viewer"):
        user = User(
            telegram_id=telegram_id,
            name=name,
            role=role
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user