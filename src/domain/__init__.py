"""Domain layer - Business logic and entities."""

from src.domain.entities.base import Entity, AuditableEntity
from src.domain.entities.logistica import (
    Order,
    Delivery,
    Inventory,
    Warehouse,
    Carrier,
    OrderStatus,
    DeliveryPriority,
)
from src.domain.value_objects import Address, CNPJ, CPF, Money, DateRange, TrackingNumber
from src.domain.repositories import (
    Repository,
    OrderRepository,
    DeliveryRepository,
    InventoryRepository,
)
from src.domain.services import OrderDomainService, DeliveryDomainService, InventoryDomainService

__all__ = [
    "Entity",
    "AuditableEntity",
    "Order",
    "Delivery",
    "Inventory",
    "Warehouse",
    "Carrier",
    "OrderStatus",
    "DeliveryPriority",
    "Address",
    "CNPJ",
    "CPF",
    "Money",
    "DateRange",
    "TrackingNumber",
    "Repository",
    "OrderRepository",
    "DeliveryRepository",
    "InventoryRepository",
    "OrderDomainService",
    "DeliveryDomainService",
    "InventoryDomainService",
]
