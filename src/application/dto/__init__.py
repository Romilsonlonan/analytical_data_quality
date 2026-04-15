"""Data Transfer Objects for the application layer."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from enum import Enum


class OrderStatusDTO(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


@dataclass
class CreateOrderDTO:
    """DTO for creating an order."""

    customer_id: str
    order_date: datetime
    items: List[dict]
    delivery_address: str
    priority: str = "normal"
    notes: Optional[str] = None


@dataclass
class OrderDTO:
    """DTO for order data."""

    id: str
    customer_id: str
    order_date: datetime
    status: str
    total_amount: float
    shipping_cost: float
    discount: float
    final_amount: float
    delivery_address: str
    priority: str
    created_at: datetime
    updated_at: datetime


@dataclass
class DeliveryDTO:
    """DTO for delivery data."""

    id: str
    order_id: str
    carrier_id: str
    tracking_number: Optional[str]
    shipped_at: Optional[datetime]
    delivered_at: Optional[datetime]
    current_status: str
    estimated_delivery: Optional[datetime]


@dataclass
class InventoryDTO:
    """DTO for inventory data."""

    id: str
    product_id: str
    warehouse_id: str
    quantity: int
    reserved_quantity: int
    available_quantity: int
    needs_reorder: bool


@dataclass
class PipelineExecutionDTO:
    """DTO for pipeline execution."""

    dag_id: str
    execution_date: datetime
    status: str
    duration_seconds: int
    tasks_total: int
    tasks_success: int
    tasks_failed: int


@dataclass
class DataQualityDTO:
    """DTO for data quality metrics."""

    dataset: str
    total_records: int
    valid_records: int
    invalid_records: int
    null_percentage: float
    quality_score: float
    checked_at: datetime
