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
    # Explicit Many-to-One Relationship: 
    # By adding remote_side=[id], you explicitly define the parent relationship as many-to-one, 
    # clearly indicating that the id column is on the "remote" side of the relationship. 
    # This makes the parent_id column the "local" side, directly supporting the notion that 
    # multiple nodes can have the same parent 
    # (many children to one parent).
    parent = relationship("Node", remote_side=[id])