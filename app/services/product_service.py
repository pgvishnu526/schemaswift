from sqlalchemy.orm import Session
from app.repositories.product_repository import ProductRepository
from app.repositories.user_repository import UserRepository
from app.repositories.log_repository import LogRepository
from rag.index_builder import update_user_embeddings as update_embeddings


class ProductService:

    @staticmethod
    def insert_product(db: Session, telegram_id, product_name, category):

        user = UserRepository.get_user(db, telegram_id)

        if not user:
            return "User not registered."

        if user.role != "admin":
            return "Only admins can insert products."

        # Title-case the category for consistency
        if category and category.strip():
            category = category.strip().title()
        else:
            category = "Uncategorized"

        product = ProductRepository.create(
            db,
            product_name,
            category,
            telegram_id
        )

        LogRepository.log(
            db,
            telegram_id,
            f"Inserted product: {product_name}"
        )

        update_embeddings()

        return f"Product '{product.product_name}' added to [{category}]."


    @staticmethod
    def fetch_products(db: Session):

        products = ProductRepository.get_all(db)

        if not products:
            return "No products found."

        return products


    @staticmethod
    def delete_product(db: Session, telegram_id, product_id):

        user = UserRepository.get_user(db, telegram_id)

        if not user:
            return "User not registered."

        if user.role != "admin":
            return "Only admins can delete products."

        deleted = ProductRepository.delete(db, product_id)

        if deleted:
            LogRepository.log(
                db,
                telegram_id,
                f"Deleted product ID: {product_id}"
            )

            update_embeddings()

            return "Product deleted successfully."

        return "Product not found."

    @staticmethod
    def delete_product_by_name(db: Session, telegram_id, product_name):

        user = UserRepository.get_user(db, telegram_id)

        if not user:
            return "User not registered."

        if user.role != "admin":
            return "Only admins can delete products."

        deleted_name = ProductRepository.delete_by_name(db, product_name)

        if deleted_name:
            LogRepository.log(
                db,
                telegram_id,
                f"Deleted product: {deleted_name}"
            )

            update_embeddings()

            return f"Product '{deleted_name}' deleted successfully."

        return f"Product '{product_name}' not found."

    @staticmethod
    def search_products(db: Session, product_name):
        products = ProductRepository.search_by_name(db, product_name)
        if not products:
            return f"No products found matching '{product_name}'."
        return products

    @staticmethod
    def check_product_exists(db: Session, product_name):
        exists = ProductRepository.exists(db, product_name)
        if exists:
            return f"Yes, '{product_name}' exists in the database."
        return f"No, '{product_name}' was not found."