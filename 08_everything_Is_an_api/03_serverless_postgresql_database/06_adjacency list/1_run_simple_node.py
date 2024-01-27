from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import Annotated
from simple_node import Node, Base
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

# Get all nodes data by parent node id
@app.get("/all-nodes/{node_id}")
def get_node_with_children(node_id: int, db: Annotated[Session, Depends(get_db)]):
    # Fetch the root node based on node_id or parent_id
    root_node = db.query(Node).filter(Node.id == node_id).first()
    if not root_node:
        return {"error": "Node not found"}

    # Construct the hierarchy
    def construct_hierarchy(node):
        """Recursively construct the hierarchy starting from the given node."""
        hierarchy = {
            "id": node.id,
            "data": node.data,
            "parent_id": node.parent_id,
            "children": [construct_hierarchy(child) for child in node.children]
        }
        return hierarchy

    # Create the hierarchy starting from the root node
    node_hierarchy = construct_hierarchy(root_node)

    return node_hierarchy
