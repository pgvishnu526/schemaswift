from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from rag.index_builder import update_user_embeddings as update_embeddings


class AuthService:

    @staticmethod
    def register_user(db: Session, telegram_id, name):

        user = UserRepository.get_user(db, telegram_id)

        if user:
            return "User already registered."

        UserRepository.create_user(
            db,
            telegram_id,
            name
        )

        update_embeddings()

        return "User registered successfully."


    @staticmethod
    def get_user_role(db: Session, telegram_id):

        user = UserRepository.get_user(db, telegram_id)

        if not user:
            return None

        return user.role