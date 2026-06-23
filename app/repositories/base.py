from typing import Generic, TypeVar

from app.models.base import Model

T = TypeVar("T", bound=Model)


class Repository(Generic[T]):
    """
    Generic in-memory repository for storing and managing models.

    This repository provides basic CRUD-style operations for models that
    inherit from the base `Model` class. All models are stored internally
    in a list and are primarily identified by their unique `id`.

    Type Parameters:
        T: A model type that inherits from `Model`.
    """

    def __init__(self) -> None:
        """
        Initialize an empty repository.
        """
        self.items: list[T] = []

    def add(self, item: T) -> None:
        """
        Add a model instance to the repository.

        Args:
            item: The model instance to add.
        """
        self.items.append(item)

    def add_many(self, items: list[T]) -> None:
        """
        Add multiple model instances to the repository.

        Args:
            items: A list of model instances to add.
        """
        self.items.extend(items)

    def get_all(self) -> list[T]:
        """
        Retrieve all items in the repository.

        Returns:
            A copy of the list containing all stored models.
        """
        return self.items.copy()

    def get_by_id(self, model_id: str) -> T | None:
        """
        Retrieve a model by its unique identifier.

        Args:
            model_id: The ID of the model to search for.

        Returns:
            The matching model if found, otherwise None.
        """
        for item in self.items:
            if item.id == model_id:
                return item

        return None

    def get_index_by_id(self, model_id: str) -> int:
        """
        Get the index of a model by its ID.

        Args:
            model_id: The ID of the model to search for.

        Returns:
            The index of the model if found, otherwise -1.
        """
        for index, item in enumerate(self.items):
            if item.id == model_id:
                return index

        return -1

    def exists_by_id(self, model_id: str) -> bool:
        """
        Check whether a model with the given ID exists.

        Args:
            model_id: The ID to check.

        Returns:
            True if a model with the ID exists, otherwise False.
        """
        return self.get_by_id(model_id) is not None

    def remove(self, item: T) -> bool:
        """
        Remove a model instance from the repository.

        Args:
            item: The model instance to remove.

        Returns:
            True if the item was removed, otherwise False.
        """
        if item not in self.items:
            return False

        self.items.remove(item)
        return True

    def remove_by_id(self, model_id: str) -> bool:
        """
        Remove a model from the repository using its ID.

        Args:
            model_id: The ID of the model to remove.

        Returns:
            True if the model was removed, otherwise False.
        """
        item = self.get_by_id(model_id)

        if item is None:
            return False

        self.items.remove(item)
        return True

    def update(self, item: T) -> bool:
        """
        Update an existing model in the repository.

        The model is located using its ID and replaced with the
        provided instance.

        Args:
            item: The updated model instance.

        Returns:
            True if the model was updated, otherwise False.
        """
        index = self.get_index_by_id(item.id)

        if index == -1:
            return False

        self.items[index] = item
        return True

    def clear(self) -> None:
        """
        Remove all items from the repository.
        """
        self.items.clear()

    def count(self) -> int:
        """
        Get the number of items stored in the repository.

        Returns:
            The number of stored models.
        """
        return len(self.items)
