"""Domain repository interfaces."""

from abc import ABC, abstractmethod
from typing import Optional, List, Generic, TypeVar
from src.domain.entities.base import Entity

T = TypeVar("T", bound=Entity)


class Repository(ABC, Generic[T]):
    """Base repository interface."""

    @abstractmethod
    def get_by_id(self, id: str) -> Optional[T]:
        pass

    @abstractmethod
    def save(self, entity: T) -> T:
        pass

    @abstractmethod
    def delete(self, id: str) -> bool:
        pass

    @abstractmethod
    def list_all(self) -> List[T]:
        pass


class OrderRepository(Repository):
    """Order repository interface."""

    @abstractmethod
    def get_by_customer(self, customer_id: str) -> List:
        pass

    @abstractmethod
    def get_by_status(self, status: str) -> List:
        pass

    @abstractmethod
    def get_pending_orders(self) -> List:
        pass


class DeliveryRepository(Repository):
    """Delivery repository interface."""

    @abstractmethod
    def get_by_order(self, order_id: str) -> Optional:
        pass

    @abstractmethod
    def get_by_tracking(self, tracking_number: str) -> Optional:
        pass

    @abstractmethod
    def get_pending_deliveries(self) -> List:
        pass


class InventoryRepository(Repository):
    """Inventory repository interface."""

    @abstractmethod
    def get_by_product(self, product_id: str) -> List:
        pass

    @abstractmethod
    def get_low_stock(self, threshold: int) -> List:
        pass

    @abstractmethod
    def reserve_quantity(self, product_id: str, warehouse_id: str, quantity: int) -> bool:
        pass
