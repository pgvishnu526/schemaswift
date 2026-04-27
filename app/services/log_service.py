from sqlalchemy.orm import Session
from app.repositories.log_repository import LogRepository
from rag.index_builder import update_user_embeddings as update_embeddings


class LogService:

    @staticmethod
    def log_action(db: Session, telegram_id, action):

        LogRepository.log(
            db,
            telegram_id,
            action
        )

        update_embeddings()

        return "Action logged successfully."

    @staticmethod
    def fetch_activity_logs(db: Session):
        logs = LogRepository.get_recent_logs(db)
        if not logs:
            return "No recent activity found."
        
        result = []
        for log in logs:
            result.append(f"[{log.time_stamp}] User {log.telegram_id}: {log.action}")
            
        return "\n".join(result)