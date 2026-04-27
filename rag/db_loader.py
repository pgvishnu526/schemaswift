from app.database.connection import SessionLocal
from app.database.models import User, AccessRequest, ActivityLog


def load_users():

    db = SessionLocal()

    users = db.query(User).all()
    requests = db.query(AccessRequest).all()
    logs = db.query(ActivityLog).all()

    db.close()

    docs = []
    
    for u in users:
        docs.append(f"User {u.name} has role {u.role}")
        
    for r in requests:
        docs.append(f"Access Request from telegram_id {r.telegram_id} is {r.status}")
        
    for l in logs:
        docs.append(f"Activity Log: telegram_id {l.telegram_id} performed action '{l.action}' at {l.time_stamp}")

    return docs