"""Application use cases."""

from datetime import datetime
from typing import List, Optional

from src.domain.entities.logistica import Order, OrderStatus, Delivery
from src.domain.services import OrderDomainService, DeliveryDomainService
from src.application.dto import CreateOrderDTO, OrderDTO, DeliveryDTO


class CreateOrderUseCase:
    """Use case for creating an order."""

    def __init__(self, order_repository, inventory_service):
        self.order_repository = order_repository
        self.inventory_service = inventory_service
        self.domain_service = OrderDomainService()

    def execute(self, dto: CreateOrderDTO) -> OrderDTO:
        order = Order(
            id=self._generate_id(),
            customer_id=dto.customer_id,
            order_date=dto.order_date,
            status=OrderStatus.PENDING,
            total_amount=sum(item["price"] * item["quantity"] for item in dto.items),
            delivery_address=dto.delivery_address,
            priority=dto.priority,
            notes=dto.notes,
        )

        saved_order = self.order_repository.save(order)

        return self._to_dto(saved_order)

    def _generate_id(self) -> str:
        return f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    def _to_dto(self, order: Order) -> OrderDTO:
        return OrderDTO(
            id=order.id,
            customer_id=order.customer_id,
            order_date=order.order_date,
            status=order.status.value,
            total_amount=order.total_amount,
            shipping_cost=order.shipping_cost,
            discount=order.discount,
            final_amount=order.final_amount,
            delivery_address=order.delivery_address,
            priority=order.priority.value if hasattr(order.priority, "value") else order.priority,
            created_at=order.created_at,
            updated_at=order.updated_at,
        )


class ProcessOrderUseCase:
    """Use case for processing an order."""

    def __init__(self, order_repository, delivery_repository, inventory_service):
        self.order_repository = order_repository
        self.delivery_repository = delivery_repository
        self.inventory_service = inventory_service
        self.domain_service = OrderDomainService()

    def execute(self, order_id: str) -> OrderDTO:
        order = self.order_repository.get_by_id(order_id)

        if not order:
            raise ValueError(f"Order not found: {order_id}")

        if not order.can_ship():
            raise ValueError(f"Order cannot be shipped: {order_id}")

        order.status = OrderStatus.PROCESSING
        order.mark_updated("system")

        saved_order = self.order_repository.save(order)

        return self._to_dto(saved_order)

    def _to_dto(self, order: Order) -> OrderDTO:
        return OrderDTO(
            id=order.id,
            customer_id=order.customer_id,
            order_date=order.order_date,
            status=order.status.value,
            total_amount=order.total_amount,
            shipping_cost=order.shipping_cost,
            discount=order.discount,
            final_amount=order.final_amount,
            delivery_address=order.delivery_address,
            priority=order.priority.value if hasattr(order.priority, "value") else order.priority,
            created_at=order.created_at,
            updated_at=order.updated_at,
        )


class ShipOrderUseCase:
    """Use case for shipping an order."""

    def __init__(self, order_repository, delivery_repository):
        self.order_repository = order_repository
        self.delivery_repository = delivery_repository

    def execute(
        self, order_id: str, carrier_id: str, tracking_number: str, estimated_delivery: datetime
    ) -> DeliveryDTO:
        order = self.order_repository.get_by_id(order_id)

        if not order:
            raise ValueError(f"Order not found: {order_id}")

        if not order.can_ship():
            raise ValueError(f"Order cannot be shipped: {order_id}")

        order.status = OrderStatus.SHIPPED
        order.mark_updated("system")
        self.order_repository.save(order)

        delivery = Delivery(
            id=f"DEL-{order_id}",
            order_id=order_id,
            carrier_id=carrier_id,
            tracking_number=tracking_number,
            shipped_at=datetime.now(),
            delivered_at=None,
            current_status="shipped",
            estimated_delivery=estimated_delivery,
        )

        saved_delivery = self.delivery_repository.save(delivery)

        return self._to_dto(saved_delivery)

    def _to_dto(self, delivery: Delivery) -> DeliveryDTO:
        return DeliveryDTO(
            id=delivery.id,
            order_id=delivery.order_id,
            carrier_id=delivery.carrier_id,
            tracking_number=delivery.tracking_number,
            shipped_at=delivery.shipped_at,
            delivered_at=delivery.delivered_at,
            current_status=delivery.current_status,
            estimated_delivery=delivery.estimated_delivery,
        )


class GetDeliveryStatusUseCase:
    """Use case for getting delivery status."""

    def __init__(self, delivery_repository):
        self.delivery_repository = delivery_repository

    def execute(self, order_id: str) -> Optional[DeliveryDTO]:
        delivery = self.delivery_repository.get_by_order(order_id)

        if not delivery:
            return None

        return self._to_dto(delivery)

    def _to_dto(self, delivery: Delivery) -> DeliveryDTO:
        return DeliveryDTO(
            id=delivery.id,
            order_id=delivery.order_id,
            carrier_id=delivery.carrier_id,
            tracking_number=delivery.tracking_number,
            shipped_at=delivery.shipped_at,
            delivered_at=delivery.delivered_at,
            current_status=delivery.current_status,
            estimated_delivery=delivery.estimated_delivery,
        )
