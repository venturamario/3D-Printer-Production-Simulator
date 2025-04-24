import simpy
from datetime import date, timedelta
from typing import List
from models import InventoryItem, ManufacturingOrder, BOMItem, Event, PurchaseOrder
from initial_data import inventory, manufacturing_orders, bom, suppliers

class Simulator:
    def __init__(self, env, capacity_per_day=10):
        self.env = env
        self.capacity_per_day = capacity_per_day
        self.current_date = date(2025, 4, 24)
        self.inventory = {item.product_id: item.quantity for item in inventory}
        self.orders = manufacturing_orders
        self.bom = bom
        self.suppliers = suppliers
        self.purchase_orders: List[PurchaseOrder] = []
        self.events: List[Event] = []
        self.order_id_counter = len(self.orders) + 1
        self.purchase_order_counter = 1
        self.event_id_counter = 1

    def advance_day(self):
        print(f"\n=== Día {self.current_date} ===")
        self.process_orders()
        self.process_purchase_orders()
        self.record_event("day_end", f"Fin del día {self.current_date}")
        self.current_date += timedelta(days=1)
        self.env.timeout(1)

    def process_orders(self):
        completed_today = 0

        for order in self.orders:
            if order.status == "released" and completed_today < self.capacity_per_day:
                if self.can_fulfill_order(order):
                    self.consume_inventory(order)
                    order.status = "completed"
                    completed_today += 1
                    self.record_event("production", f"Pedido {order.id} completado ({order.quantity} unidades)")
                else:
                    self.record_event("stock_shortage", f"No hay suficiente stock para pedido {order.id}")

    def can_fulfill_order(self, order):
        required = self.get_bom(order.product_id, order.quantity)
        return all(self.inventory.get(pid, 0) >= qty for pid, qty in required.items())

    def consume_inventory(self, order):
        required = self.get_bom(order.product_id, order.quantity)
        for pid, qty in required.items():
            self.inventory[pid] -= qty
            self.record_event("stock_change", f"-{qty} de producto {pid}")

    def get_bom(self, product_id, quantity):
        items = [b for b in self.bom if b.product_id == product_id]
        return {item.material_id: item.quantity * quantity for item in items}

    def create_purchase_order(self, product_id: int, quantity: int) -> PurchaseOrder:
        # Find supplier for this product
        supplier = next((s for s in self.suppliers if s.product_id == product_id), None)
        if not supplier:
            self.record_event("purchase_error", f"No se encontró proveedor para el producto {product_id}")
            return None

        # Create purchase order
        po = PurchaseOrder(
            id=self.purchase_order_counter,
            supplier_id=supplier.id,
            product_id=product_id,
            quantity=quantity,
            issued_at=self.current_date,
            estimated_delivery=self.current_date + timedelta(days=supplier.lead_time_days),
            status="pending"
        )
        
        self.purchase_orders.append(po)
        self.purchase_order_counter += 1
        
        cost = supplier.unit_cost * quantity
        self.record_event("purchase", 
            f"Orden de compra #{po.id} creada: {quantity} unidades de {product_id} " \
            f"a {supplier.name} por {cost}€. Entrega estimada: {po.estimated_delivery}")
        
        return po

    def process_purchase_orders(self):
        for po in self.purchase_orders:
            if po.status == "pending" and po.estimated_delivery <= self.current_date:
                # Deliver the order
                self.inventory[po.product_id] = self.inventory.get(po.product_id, 0) + po.quantity
                po.status = "delivered"
                
                self.record_event("stock_change", 
                    f"+{po.quantity} unidades de {po.product_id} recibidas de orden de compra #{po.id}")

    def record_event(self, type, detail):
        self.events.append(Event(
            id=self.event_id_counter,
            type=type,
            date_simulated=self.current_date,
            detail=detail
        ))
        self.event_id_counter += 1
        print(f"[EVENT] {type}: {detail}")
