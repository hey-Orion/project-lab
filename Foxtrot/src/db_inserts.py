from src.database import SessionLocal
from models.sqlalchemy_models import Cart, Product


def load_carts(records: list[dict]) -> None:

    session = SessionLocal()

    try:

        for record in records:

            cart = Cart(
                id=record["id"],
                total=record["total"],
                discounted_total=record["discountedTotal"],
                total_products=record["totalProducts"],
                total_quantity=record["totalQuantity"]
            )

            session.add(cart)

            for product_record in record["products"]:

                product = Product(
                    product_id=product_record["id"],
                    cart_id=record["id"],
                    title=product_record["title"],
                    price=product_record["price"],
                    quantity=product_record["quantity"],
                    total=product_record["total"],
                    discount_percentage=product_record["discountPercentage"],
                    discounted_total=product_record["discountedTotal"],
                    thumbnail=product_record["thumbnail"]
                )

                session.add(product)

        session.commit()

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()