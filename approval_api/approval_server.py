from fastapi import FastAPI
from app.database.connection import SessionLocal
from app.services.approval_service import ApprovalService

app = FastAPI()


@app.get("/approve")
def approve(uid: int, role: str):

    db = SessionLocal()
    try:
        ApprovalService.approve_user(
            db,
            uid,
            role
        )
        return {"status": "approved"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        db.close()


@app.get("/reject")
def reject(uid: int):

    db = SessionLocal()
    try:
        ApprovalService.reject_user(
            db,
            uid
        )
        return {"status": "rejected"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        db.close()