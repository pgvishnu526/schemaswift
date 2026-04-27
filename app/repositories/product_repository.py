from sqlalchemy.orm import Session
from app.database.models import Product


class ProductRepository:

    @staticmethod
    def create(db: Session, product_name, category, created_by):
        product = Product(
            product_name=product_name,
            category=category,
            created_by=created_by
        )

        db.add(product)
        db.commit()
        db.refresh(product)

        return product

    @staticmethod
    def get_all(db: Session):
        return db.query(Product).all()

    @staticmethod
    def delete(db: Session, product_id):
        product = db.query(Product).filter(Product.id == product_id).first()

        if product:
            db.delete(product)
            db.commit()
            return True

        return False

    @staticmethod
    def delete_by_name(db: Session, product_name):
        product = db.query(Product).filter(
            Product.product_name.ilike(product_name)
        ).first()

        if product:
            name = product.product_name
            db.delete(product)
            db.commit()
            return name

        return None

    @staticmethod
    def search_by_name(db: Session, product_name):
        return db.query(Product).filter(
            Product.product_name.ilike(f"%{product_name}%")
        ).all()

    @staticmethod
    def exists(db: Session, product_name):
        return db.query(Product).filter(
            Product.product_name.ilike(product_name)
        ).first() is not None