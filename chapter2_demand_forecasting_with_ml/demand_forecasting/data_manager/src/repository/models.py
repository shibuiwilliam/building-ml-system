from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.sql.sqltypes import Integer
from src.db.db import Base


class StoreMaster(Base):
    __tablename__ = "stores_master"

    id = Column(
        String(36),
        nullable=False,
        primary_key=True,
    )
    name = Column(
        String(6),
        nullable=False,
        unique=True,
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=current_timestamp(),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=current_timestamp(),
        nullable=False,
    )


class ItemMaster(Base):
    __tablename__ = "items_master"

    id = Column(
        String(36),
        nullable=False,
        primary_key=True,
    )
    name = Column(
        String(6),
        nullable=False,
        unique=True,
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=current_timestamp(),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=current_timestamp(),
        nullable=False,
    )


class ItemPrice(Base):
    __tablename__ = "item_prices"

    id = Column(
        String(36),
        nullable=False,
        primary_key=True,
    )
    item_id = Column(
        String(36),
        ForeignKey("items_master.id"),
        nullable=False,
    )
    price = Column(
        Integer,
        nullable=False,
        unique=True,
    )
    applied_from = Column(
        Date,
        nullable=False,
    )
    applied_to = Column(
        Date,
        nullable=True,
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=current_timestamp(),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=current_timestamp(),
        nullable=False,
    )


class ItemStock(Base):
    __tablename__ = "item_stocks"

    id = Column(
        String(36),
        nullable=False,
        primary_key=True,
    )
    item_id = Column(
        String(36),
        ForeignKey("items_master.id"),
        nullable=False,
    )
    stock = Column(
        Integer,
        nullable=False,
    )
    recorded_at = Column(
        Date,
        nullable=False,
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=current_timestamp(),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=current_timestamp(),
        nullable=False,
    )


class ItemStockPerStore(Base):
    __tablename__ = "item_stocks_per_store"

    id = Column(
        String(36),
        nullable=False,
        primary_key=True,
    )
    item_id = Column(
        String(36),
        ForeignKey("items_master.id"),
        nullable=False,
    )
    store_id = Column(
        String(36),
        ForeignKey("stores_master.id"),
        nullable=False,
    )
    stock = Column(
        Integer,
        nullable=False,
    )
    recorded_at = Column(
        Date,
        nullable=False,
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=current_timestamp(),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=current_timestamp(),
        nullable=False,
    )


class ItemSale(Base):
    __tablename__ = "item_sales"

    id = Column(
        String(36),
        nullable=False,
        primary_key=True,
    )
    item_id = Column(
        String(36),
        ForeignKey("items_master.id"),
        nullable=False,
    )
    item_price_id = Column(
        String(36),
        ForeignKey("item_prices.id"),
        nullable=False,
    )
    quantity = Column(
        Integer,
        nullable=False,
    )
    sold_at = Column(
        DateTime(timezone=True),
        nullable=False,
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=current_timestamp(),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=current_timestamp(),
        nullable=False,
    )
