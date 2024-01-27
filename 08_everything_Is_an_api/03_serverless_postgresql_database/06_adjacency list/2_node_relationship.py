from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import Annotated

from node_relationship import Node, Base
from get_db import engine, get_db

app = FastAPI()

Base.metadata.create_all(engine)

@app.get("/")
def read_root():
    return {"Hello": "World"}

# Add parent node
@app.post("/nodes")
def create_node_endpoint(data: str, db: Annotated[Session, Depends(get_db)]):
    node = Node(data=data)
    db.add(node)
    db.commit()
    db.refresh(node)
    return node

# Add child node
@app.post("/nodes/{parent_id}")
def create_child_node_endpoint(parent_id: int, data: str, db: Annotated[Session, Depends(get_db)]):
    parent_node = db.query(Node).filter(Node.id == parent_id).first()
    if not parent_node:
        return {"error": "Parent node not found"}
    child_node = Node(data=data, parent_id=parent_id)
    db.add(child_node)
    db.commit()
    db.refresh(child_node)
    return child_node

@app.get("/nodes/{node_id}/parent")
def get_node_parent(node_id: int, db: Annotated[Session, Depends(get_db)]):
    node = db.query(Node).filter(Node.id == node_id).first()
    
    if node is None:
        return {"error": "Node not found"}
    
    if node.parent is None:
        return {"message": "This node has no parent."}

    parent = {
        "id": node.parent.id,
        "data": node.parent.data,
        "parent_id": node.parent.parent_id  # This can be None if the parent is a root node
    }
    
    return parent
