from app.database.connection import SessionLocal
from app.database.models import User


def seed_admin():

    db = SessionLocal()

    try:

        admin_id = int(input("Enter admin Telegram ID: "))
        admin_name = input("Enter admin name: ")

        existing = db.query(User).filter(
            User.telegram_id == admin_id
        ).first()

        if existing:
            print("Admin already exists.")
            return

        admin = User(
            telegram_id=admin_id,
            name=admin_name,
            role="admin"
        )

        db.add(admin)
        db.commit()

        print("Admin user created successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    seed_admin()