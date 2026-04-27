import json
from mcp_server.server import mcp
from app.database.connection import SessionLocal
from app.services.product_service import ProductService


@mcp.tool()
def insert_product(telegram_id: int, product_name: str, category: str = "") -> str:
    """
    Insert a product into the database. Only admins are allowed.
    Args:
        telegram_id: Telegram user ID of the requester
        product_name: Name of the product to insert
        category: Optional product category
    """
    db = SessionLocal()
    try:
        result = ProductService.insert_product(
            db, telegram_id, product_name, category
        )
        return json.dumps({"success": True, "message": result})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})
    finally:
        db.close()


@mcp.tool()
def fetch_products(telegram_id: int = 0) -> str:
    """
    Fetch all available products from the database.
    Args:
        telegram_id: Telegram user ID (optional, for logging)
    """
    db = SessionLocal()
    try:
        products = ProductService.fetch_products(db)

        if isinstance(products, str):
            return json.dumps({"success": True, "message": products})

        product_list = [
            {
                "id": p.id,
                "name": p.product_name,
                "category": p.category or "Uncategorized"
            }
            for p in products
        ]
        return json.dumps({"success": True, "products": product_list})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})
    finally:
        db.close()


@mcp.tool()
def delete_product(telegram_id: int, product_id: int = 0, product_name: str = "") -> str:
    """
    Delete a product by its ID or by its name. Only admins are allowed.
    Use product_id if the user specifies a number, or product_name if they specify a name.
    Args:
        telegram_id: Telegram user ID of the requester
        product_id: ID of the product to delete (use this if user gives a number)
        product_name: Name of the product to delete (use this if user gives a name)
    """
    db = SessionLocal()
    try:
        if product_id and product_id > 0:
            result = ProductService.delete_product(
                db, telegram_id, product_id
            )
        elif product_name and product_name.strip():
            result = ProductService.delete_product_by_name(
                db, telegram_id, product_name.strip()
            )
        else:
            return json.dumps({"success": False, "message": "Please specify a product ID or name to delete."})

        return json.dumps({"success": True, "message": result})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})
    finally:
        db.close()


@mcp.tool()
def search_products(product_name: str) -> str:
    """
    Search for products by name (partial match).
    Args:
        product_name: Part of the product name to search for
    """
    db = SessionLocal()
    try:
        products = ProductService.search_products(db, product_name)
        if isinstance(products, str):
            return json.dumps({"success": True, "message": products})

        product_list = [
            {
                "id": p.id,
                "name": p.product_name,
                "category": p.category or "Uncategorized"
            }
            for p in products
        ]
        return json.dumps({"success": True, "products": product_list})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})
    finally:
        db.close()


@mcp.tool()
def check_product_exists(product_name: str) -> str:
    """
    Check if a product with an exact name exists in the database.
    Args:
        product_name: Exact name of the product to check
    """
    db = SessionLocal()
    try:
        result = ProductService.check_product_exists(db, product_name)
        return json.dumps({"success": True, "message": result})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})
    finally:
        db.close()