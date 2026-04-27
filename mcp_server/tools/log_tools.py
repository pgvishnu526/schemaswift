import json
from mcp_server.server import mcp
from app.database.connection import SessionLocal
from app.services.log_service import LogService


@mcp.tool()
def log_action(telegram_id: int, action: str = "", message: str = "") -> str:
    """
    Log an activity event for audit purposes.
    Args:
        telegram_id: Telegram user ID performing the action
        action: Description of the action performed
        message: Fallback description of the action performed (if action is missing)
    """
    final_action = action if action else message
    if not final_action:
        final_action = "Unknown user activity"

    db = SessionLocal()
    try:
        result = LogService.log_action(db, telegram_id, final_action)
        return json.dumps({"success": True, "message": result})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})
    finally:
        db.close()


@mcp.tool()
def fetch_activity_logs() -> str:
    """
    Fetch the most recent system activity logs.
    """
    db = SessionLocal()
    try:
        result = LogService.fetch_activity_logs(db)
        return json.dumps({"success": True, "logs": result})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})
    finally:
        db.close()