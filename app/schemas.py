from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ── User ──────────────────────────────────────────────
class UserOut(BaseModel):
    telegram_id: int
    name: str
    role: str
    status: str
    created_at: Optional[datetime]

    class Config:
        from_attributes = True


# ── Product ───────────────────────────────────────────
class ProductOut(BaseModel):
    id: int
    product_name: str
    category: Optional[str]
    created_by: Optional[int]
    created_at: Optional[datetime]

    class Config:
        from_attributes = True


# ── Tool responses (returned by MCP tools as JSON) ────
class ToolResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    data: Optional[dict | list] = None
    error: Optional[str] = None