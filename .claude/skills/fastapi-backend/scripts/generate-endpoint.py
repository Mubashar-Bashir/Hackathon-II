#!/usr/bin/env python3
# Script to generate a new FastAPI endpoint with Pydantic models

import os
import sys
from pathlib import Path

def generate_endpoint(endpoint_name: str):
    # Create directory structure if it doesn't exist
    os.makedirs("src/api", exist_ok=True)
    os.makedirs("src/models", exist_ok=True)

    # Generate Pydantic models
    model_content = f'''from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

class {endpoint_name.title()}Base(BaseModel):
    """Base model for {endpoint_name}."""
    name: str
    description: Optional[str] = None

class {endpoint_name.title()}Create({endpoint_name.title()}Base):
    """Model for creating a new {endpoint_name}."""
    pass

class {endpoint_name.title()}Update(BaseModel):
    """Model for updating an existing {endpoint_name}."""
    name: Optional[str] = None
    description: Optional[str] = None

class {endpoint_name.title()}Response({endpoint_name.title()}Base):
    """Response model for {endpoint_name} with ID."""
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
'''

    with open(f"src/models/{endpoint_name}.py", "w") as f:
        f.write(model_content)

    # Generate API endpoint
    api_content = f'''from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import Session, select

from src.models.{endpoint_name} import (
    {endpoint_name.title()}Response,
    {endpoint_name.title()}Create,
    {endpoint_name.title()}Update
)
from src.core.database import get_session
from src.models.user import User
from src.core.security import get_current_user

router = APIRouter(prefix="/{endpoint_name}", tags=["{endpoint_name}"])

@router.get("/", response_model=List[{endpoint_name.title()}Response])
def get_{endpoint_name}s(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get all {endpoint_name}s for the current user."""
    # Add your query logic here
    pass

@router.post("/", response_model={endpoint_name.title()}Response)
def create_{endpoint_name}(
    {endpoint_name}_data: {endpoint_name.title()}Create,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new {endpoint_name}."""
    # Add your creation logic here
    pass

@router.get("/{{item_id}}", response_model={endpoint_name.title()}Response)
def get_{endpoint_name}(
    item_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get a specific {endpoint_name} by ID."""
    # Add your retrieval logic here
    pass

@router.put("/{{item_id}}", response_model={endpoint_name.title()}Response)
def update_{endpoint_name}(
    item_id: uuid.UUID,
    {endpoint_name}_data: {endpoint_name.title()}Update,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update an existing {endpoint_name}."""
    # Add your update logic here
    pass

@router.delete("/{{item_id}}")
def delete_{endpoint_name}(
    item_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a {endpoint_name}."""
    # Add your deletion logic here
    pass
'''

    with open(f"src/api/{endpoint_name}.py", "w") as f:
        f.write(api_content)

    print(f"FastAPI endpoint for {endpoint_name} created!")
    print(f"- Model: src/models/{endpoint_name}.py")
    print(f"- API: src/api/{endpoint_name}.py")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate-endpoint.py <endpoint-name>")
        sys.exit(1)

    endpoint_name = sys.argv[1]
    generate_endpoint(endpoint_name)