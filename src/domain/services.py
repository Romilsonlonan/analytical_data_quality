"""Domain services - business logic."""

from datetime import datetime, timedelta
from typing import List

from src.domain.entities.logistica import Order, Delivery, Inventory


class OrderDomainService:
    """Domain service for order operations."""

    def calculate_delivery_date(self, order: Order, sla_days: int) -> datetime:
        """Calculate expected delivery date based on SLA."""
        return order.order_date + timedelta(days=sla_days)

    def apply_discount(self, order: Order, discount_percentage: float) -> Order:
        """Apply discount to order."""
        if discount_percentage < 0 or discount_percentage > 100:
            raise ValueError("Desconto inválido")

        discount_value = order.total_amount * (discount_percentage / 100)
        order.discount = discount_value
        return order

    def can_fulfill_order(self, inventory: List[Inventory], required_quantity: int) -> bool:
        """Check if order can be fulfilled from inventory."""
        total_available = sum(inv.available_quantity for inv in inventory)
        return total_available >= required_quantity

    def calculate_priority_score(self, order: Order) -> int:
        """Calculate priority score for order."""
        score = 0

        if order.priority == "urgent":
            score += 100
        elif order.priority == "high":
            score += 50

        days_old = (datetime.now() - order.order_date).days
        score += min(days_old * 5, 50)

        return score


class DeliveryDomainService:
    """Domain service for delivery operations."""

    def is_delivery_late(self, delivery: Delivery, sla_hours: int) -> bool:
        """Check if delivery is late."""
        if delivery.delivered_at:
            actual_hours = (delivery.delivered_at - delivery.shipped_at).total_seconds() / 3600
            return actual_hours > sla_hours
        elif delivery.estimated_delivery:
            return datetime.now() > delivery.estimated_delivery
        return False

    def calculate_delivery_performance(self, deliveries: List[Delivery]) -> dict:
        """Calculate delivery performance metrics."""
        total = len(deliveries)
        if total == 0:
            return {"on_time": 0, "late": 0, "rate": 0}

        on_time = sum(1 for d in deliveries if not self.is_delivery_late(d, 48))

        return {"on_time": on_time, "late": total - on_time, "rate": (on_time / total) * 100}


class InventoryDomainService:
    """Domain service for inventory operations."""

    def calculate_reorder_quantity(
        self, inventory: Inventory, lead_time_days: int, daily_demand: int
    ) -> int:
        """Calculate optimal reorder quantity."""
        safety_stock = daily_demand * lead_time_days
        reorder_point = safety_stock + (daily_demand * 7)

        return max(0, reorder_point - inventory.available_quantity)

    def get_low_stock_products(self, inventories: List[Inventory]) -> List[Inventory]:
        """Get products that need reorder."""
        return [inv for inv in inventories if inv.needs_reorder]

    def allocate_inventory(self, inventories: List[Inventory], quantity: int) -> dict:
        """Allocate inventory from multiple warehouses."""
        allocated = {}
        remaining = quantity

        for inv in sorted(inventories, key=lambda x: x.available_quantity, reverse=True):
            if remaining <= 0:
                break

            to_allocate = min(inv.available_quantity, remaining)
            allocated[inv.warehouse_id] = to_allocate
            remaining -= to_allocate

        return allocated
