import json
from mcp_server.server import mcp
from app.database.connection import SessionLocal
from app.services.auth_service import AuthService


@mcp.tool()
def register_user(telegram_id: int, name: str) -> str:
    """
    Register a new Telegram user in the database.
    Args:
        telegram_id: Telegram user ID
        name: Display name of the user
    """
    db = SessionLocal()
    try:
        result = AuthService.register_user(db, telegram_id, name)
        return json.dumps({"success": True, "message": result})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})
    finally:
        db.close()


@mcp.tool()
def get_user_role(telegram_id: int) -> str:
    """
    Get the role of a registered user.
    Args:
        telegram_id: Telegram user ID
    """
    db = SessionLocal()
    try:
        role = AuthService.get_user_role(db, telegram_id)
        if role is None:
            return json.dumps({"success": False, "message": "User not found."})
        return json.dumps({"success": True, "role": role})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})
    finally:
        db.close()