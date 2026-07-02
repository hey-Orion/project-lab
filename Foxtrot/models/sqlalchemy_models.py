from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, Integer, Float, String, ForeignKey


class Base(DeclarativeBase):
    pass


class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True)

    total = Column(
        Float,
        nullable=False
    )

    discounted_total = Column(
        Float,
        nullable=False
    )

    total_products = Column(
        Integer,
        nullable=False
    )

    total_quantity = Column(
        Integer,
        nullable=False
    )

    products = relationship(
        "Product",
        back_populates="cart",
        cascade="all, delete-orphan"
    )


class Product(Base):
    __tablename__ = "products"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    # Product ID from API
    product_id = Column(
        Integer,
        nullable=False
    )

    cart_id = Column(
        Integer,
        ForeignKey("carts.id"),
        nullable=False
    )

    title = Column(
        String(255),
        nullable=False
    )

    price = Column(
        Float,
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False
    )

    total = Column(
        Float,
        nullable=False
    )

    discount_percentage = Column(
        Float,
        nullable=False
    )

    discounted_total = Column(
        Float,
        nullable=False
    )

    thumbnail = Column(
        String(500),
        nullable=False
    )

    cart = relationship(
        "Cart",
        back_populates="products"
    )