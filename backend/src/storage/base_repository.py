import logging
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional, Any
from sqlmodel import select
from sqlmodel.sql.expression import SelectOfScalar
from uuid import UUID

from sqlmodel import Session

# Type variable for models
T = TypeVar('T')
TRead = TypeVar('TRead')
TCreate = TypeVar('TCreate')
TUpdate = TypeVar('TUpdate')


class BaseRepository(ABC, Generic[T, TRead, TCreate, TUpdate]):
    """
    Abstract base repository implementing the repository pattern.
    Provides common CRUD operations that can be inherited by specific repositories.
    """

    def __init__(self, session: Session):
        self.session = session
        self.logger = logging.getLogger(__name__)

    @property
    @abstractmethod
    def model(self) -> type[T]:
        """Return the model class for this repository"""
        pass

    @property
    @abstractmethod
    def read_model(self) -> type[TRead]:
        """Return the read model class for this repository"""
        pass

    def create(self, obj: TCreate) -> TRead:
        """Create a new entity"""
        self.logger.debug(f"Creating new {self.model.__name__} entity")

        db_obj = self.model(**obj.model_dump())
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)

        self.logger.info(f"Successfully created {self.model.__name__} with ID: {getattr(db_obj, 'id', 'unknown')}")
        return self.read_model.model_validate(db_obj)

    def get_by_id(self, id: UUID) -> Optional[TRead]:
        """Get an entity by its ID"""
        self.logger.debug(f"Retrieving {self.model.__name__} with ID: {id}")

        db_obj = self.session.get(self.model, id)
        if db_obj:
            self.logger.debug(f"Successfully retrieved {self.model.__name__} with ID: {id}")
            return self.read_model.model_validate(db_obj)
        else:
            self.logger.warning(f"{self.model.__name__} with ID {id} not found")
            return None

    def get_all(self, offset: int = 0, limit: int = 100) -> List[TRead]:
        """Get all entities with pagination"""
        self.logger.debug(f"Retrieving all {self.model.__name__} entities with offset={offset}, limit={limit}")

        statement = select(self.model).offset(offset).limit(limit)
        results = self.session.exec(statement).all()
        entities = [self.read_model.model_validate(obj) for obj in results]

        self.logger.info(f"Retrieved {len(entities)} {self.model.__name__} entities")
        return entities

    def update(self, id: UUID, obj: TUpdate) -> Optional[TRead]:
        """Update an existing entity"""
        self.logger.debug(f"Updating {self.model.__name__} with ID: {id}")

        db_obj = self.session.get(self.model, id)
        if not db_obj:
            self.logger.warning(f"{self.model.__name__} with ID {id} not found for update")
            return None

        update_data = obj.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)

        self.logger.info(f"Successfully updated {self.model.__name__} with ID: {id}")
        return self.read_model.model_validate(db_obj)

    def delete(self, id: UUID) -> bool:
        """Delete an entity by its ID"""
        self.logger.debug(f"Deleting {self.model.__name__} with ID: {id}")

        db_obj = self.session.get(self.model, id)
        if not db_obj:
            self.logger.warning(f"{self.model.__name__} with ID {id} not found for deletion")
            return False

        self.session.delete(db_obj)
        self.session.commit()

        self.logger.info(f"Successfully deleted {self.model.__name__} with ID: {id}")
        return True

    def get_by_filter(self, **kwargs) -> List[TRead]:
        """Get entities by filter criteria"""
        self.logger.debug(f"Retrieving {self.model.__name__} entities with filters: {kwargs}")

        statement = select(self.model)
        for field, value in kwargs.items():
            statement = statement.where(getattr(self.model, field) == value)

        results = self.session.exec(statement).all()
        entities = [self.read_model.model_validate(obj) for obj in results]

        self.logger.info(f"Retrieved {len(entities)} {self.model.__name__} entities with filters: {kwargs}")
        return entities