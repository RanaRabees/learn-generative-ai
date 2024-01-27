from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Boolean, ForeignKey

from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class Node(Base):
    __tablename__ = "node"
    id = mapped_column(Integer, primary_key=True)
    parent_id = mapped_column(Integer, ForeignKey("node.id"))
    data = mapped_column(String(50))
    children = relationship("Node", back_populates="parent")
    parent = relationship("Node", back_populates="children", remote_side=[id])
