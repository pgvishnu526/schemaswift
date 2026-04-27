from mcp_server.server import mcp
from app.database.connection import SessionLocal
from app.services.approval_service import ApprovalService


@mcp.tool()
def approve_user(telegram_id: int, role: str):

    db = SessionLocal()
    try:
        result = ApprovalService.approve_user(
            db,
            telegram_id,
            role
        )
        return {"success": True, "message": result}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        db.close()


@mcp.tool()
def reject_user(telegram_id: int):

    db = SessionLocal()
    try:
        result = ApprovalService.reject_user(
            db,
            telegram_id
        )
        return {"success": True, "message": result}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        db.close()


@mcp.tool()
def list_pending_requests():

    db = SessionLocal()
    try:
        requests = ApprovalService.list_pending_requests(db)
        return {
            "success": True,
            "pending": [
                r.telegram_id for r in requests
            ]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        db.close()