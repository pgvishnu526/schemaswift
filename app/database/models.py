from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, BigInteger, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    telegram_id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    status = Column(String, default="active")
    created_at = Column(TIMESTAMP, server_default=func.now())


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, nullable=False)
    category = Column(String)
    created_by = Column(BigInteger, ForeignKey("users.telegram_id"))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now())


class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger)
    action = Column(String, nullable=False)
    time_stamp = Column(TIMESTAMP, server_default=func.now())


class AccessRequest(Base):
    __tablename__ = "access_requests"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, nullable=False)
    status = Column(String, default="pending")
    requested_at = Column(TIMESTAMP, server_default=func.now())