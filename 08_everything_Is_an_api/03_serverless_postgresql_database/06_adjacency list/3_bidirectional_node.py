from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from bidirectional_node import Node, Base
from get_db import engine, get_db

app = FastAPI()

Base.metadata.create_all(engine)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/nodes/{parent_id}/add_child")
def add_child(parent_id: int, child_data: str, db: Annotated[Session, Depends(get_db)]):
    """
    1. Adding a New Child Node
    This endpoint creates a new child node for a given parent node. 
    It demonstrates how adding to the children collection automatically sets the parent relationship.
    """
    parent_node = db.query(Node).filter(Node.id == parent_id).first()
    if not parent_node:
        raise HTTPException(status_code=404, detail="Parent node not found")

    child_node = Node(data=child_data)
    parent_node.children.append(child_node)  # Automatically sets child_node.parent
    db.add(child_node)
    db.commit()
    db.refresh(child_node)
    return {"message": "Child added successfully", "child_id": child_node.id, "parent_id": parent_node.id}

@app.get("/nodes/{node_id}")
def get_node_with_relations(node_id: int, db: Annotated[Session, Depends(get_db)]):
    """
    2. Retrieving a Node with Its Parent and Children
    This endpoint fetches a node by its ID, including information about its 
    parent and its children, showcasing the bidirectional relationship functionality.
    """
    
    node = db.query(Node).filter(Node.id == node_id).first()
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")

    parent_id = node.parent.id if node.parent else None
    children_ids = [child.id for child in node.children]
    return {
        "node_id": node.id,
        "data": node.data,
        "parent_id": parent_id,
        "children_ids": children_ids
    }
