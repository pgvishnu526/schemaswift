from app.repositories.approval_repository import ApprovalRepository
from rag.index_builder import update_user_embeddings as update_embeddings


class ApprovalService:

    @staticmethod
    def approve_user(db, telegram_id, role):

        ApprovalRepository.approve_user(
            db,
            telegram_id,
            role
        )

        update_embeddings()

        return f"User approved as {role}"


    @staticmethod
    def reject_user(db, telegram_id):

        ApprovalRepository.reject_user(
            db,
            telegram_id
        )

        update_embeddings()

        return "User rejected"


    @staticmethod
    def list_pending_requests(db):

        return ApprovalRepository.list_pending_requests(db)