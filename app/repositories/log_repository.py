from sqlalchemy.orm import Session
from app.database.models import ActivityLog


class LogRepository:

    @staticmethod
    def log(db: Session, telegram_id, action):

        log_entry = ActivityLog(
            telegram_id=telegram_id,
            action=action
        )

        db.add(log_entry)
        db.commit()

    @staticmethod
    def get_recent_logs(db: Session, limit: int = 20):
        return db.query(ActivityLog).order_by(ActivityLog.time_stamp.desc()).limit(limit).all()