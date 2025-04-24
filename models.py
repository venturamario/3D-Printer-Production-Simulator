from pydantic import BaseModel
from typing import Literal, List
from datetime import date

# Producto (materia prima o terminado)
class Product(BaseModel):
    id: int
    name: str
    type: Literal["raw", "finished"]

# Inventario
class InventoryItem(BaseModel):
    product_id: int
    quantity: int

# Proveedor
class Supplier(BaseModel):
    id: int
    name: str
    product_id: int  # producto que vende
    unit_cost: float
    lead_time_days: int

# BOM: Bill of Materials
class BOMItem(BaseModel):
    product_id: int  # producto terminado
    material_id: int
    quantity: int

# Pedido de fabricación
class ManufacturingOrder(BaseModel):
    id: int
    created_at: date
    product_id: int
    quantity: int
    status: Literal["pending", "released", "completed"]

# Orden de compra
class PurchaseOrder(BaseModel):
    id: int
    supplier_id: int
    product_id: int
    quantity: int
    issued_at: date
    estimated_delivery: date
    status: Literal["pending", "delivered"]

# Evento (histórico del sistema)
class Event(BaseModel):
    id: int
    type: Literal["production", "purchase", "stock_change", "order_released", "day_end", "stock_shortage"]
    date_simulated: date
    detail: str
