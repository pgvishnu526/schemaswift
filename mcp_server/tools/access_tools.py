import json
from mcp_server.server import mcp
from app.database.connection import SessionLocal
from app.services.access_service import AccessService


@mcp.tool()
def request_access(telegram_id: int, name: str = "Unknown User") -> str:
    """
    Request elevated access privileges for a user.
    Args:
        telegram_id: Telegram user ID requesting access
        name: Name of the user requesting access
    """
    db = SessionLocal()
    try:
        result = AccessService.request_access(db, telegram_id, name)
        return json.dumps({"success": True, "message": result})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})
    finally:
        db.close()