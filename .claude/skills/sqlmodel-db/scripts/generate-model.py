#!/usr/bin/env python3
# Script to generate a new SQLModel model with CRUD operations

import os
import sys
from pathlib import Path

def generate_model(model_name: str):
    # Create directory structure if it doesn't exist
    os.makedirs("src/models", exist_ok=True)
    os.makedirs("src/services", exist_ok=True)

    # Generate SQLModel model
    model_content = f'''from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime
import uuid

if TYPE_CHECKING:
    from src.models.user import User

class {model_name.title()}Base(SQLModel):
    """Base model for {model_name}."""
    name: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)

class {model_name.title()}({model_name.title()}Base, table=True):
    """SQLModel for {model_name} with database table."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to user
    user: "User" = Relationship(back_populates="{model_name.lower()}s")

class {model_name.title()}Create({model_name.title()}Base):
    """Model for creating a new {model_name}."""
    pass

class {model_name.title()}Update(SQLModel):
    """Model for updating an existing {model_name}."""
    name: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
'''

    with open(f"src/models/{model_name}.py", "w") as f:
        f.write(model_content)

    # Generate CRUD service
    service_content = f'''from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID

from src.models.{model_name} import {model_name.title()}, {model_name.title()}Create, {model_name.title()}Update

def create_{model_name}(
    session: Session,
    {model_name}_data: {model_name.title()}Create,
    user_id: UUID
) -> {model_name.title()}:
    """Create a new {model_name} in the database."""
    {model_name}_db = {model_name.title()}(
        **{model_name}_data.dict(),
        user_id=user_id
    )
    session.add({model_name}_db)
    session.commit()
    session.refresh({model_name}_db)
    return {model_name}_db

def get_{model_name}_by_id(
    session: Session,
    {model_name}_id: UUID
) -> Optional[{model_name.title()}]:
    """Get a {model_name} by its ID."""
    statement = select({model_name.title()}).where({model_name.title()}.id == {model_name}_id)
    return session.exec(statement).first()

def get_{model_name}s_by_user(
    session: Session,
    user_id: UUID
) -> List[{model_name.title()}]:
    """Get all {model_name}s for a specific user."""
    statement = select({model_name.title()}).where({model_name.title()}.user_id == user_id)
    return session.exec(statement).all()

def update_{model_name}(
    session: Session,
    {model_name}_id: UUID,
    {model_name}_data: {model_name.title()}Update
) -> Optional[{model_name.title()}]:
    """Update an existing {model_name}."""
    {model_name}_db = session.get({model_name.title()}, {model_name}_id)
    if {model_name}_db:
        update_data = {model_name}_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr({model_name}_db, field, value)
        session.add({model_name}_db)
        session.commit()
        session.refresh({model_name}_db)
    return {model_name}_db

def delete_{model_name}(
    session: Session,
    {model_name}_id: UUID
) -> bool:
    """Delete a {model_name} by ID."""
    {model_name}_db = session.get({model_name.title()}, {model_name}_id)
    if {model_name}_db:
        session.delete({model_name}_db)
        session.commit()
        return True
    return False
'''

    with open(f"src/services/{model_name}_service.py", "w") as f:
        f.write(service_content)

    print(f"SQLModel for {model_name} created!")
    print(f"- Model: src/models/{model_name}.py")
    print(f"- Service: src/services/{model_name}_service.py")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate-model.py <model-name>")
        sys.exit(1)

    model_name = sys.argv[1]
    generate_model(model_name)