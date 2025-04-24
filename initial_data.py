from datetime import date
from models import Product, InventoryItem, Supplier, BOMItem, ManufacturingOrder

# Productos
products = [
    Product(id=1, name="kit_piezas", type="raw"),
    Product(id=2, name="pcb", type="raw"),
    Product(id=3, name="extrusor", type="raw"),
    Product(id=4, name="cables_conexion", type="raw"),
    Product(id=5, name="transformador_24v", type="raw"),
    Product(id=6, name="enchufe_schuko", type="raw"),
    Product(id=7, name="sensor_autonivel", type="raw"),
    Product(id=100, name="P3D-Classic", type="finished"),
    Product(id=101, name="P3D-Pro", type="finished"),
]

# Inventario inicial
inventory = [
    InventoryItem(product_id=1, quantity=30),
    InventoryItem(product_id=2, quantity=20),
    InventoryItem(product_id=3, quantity=15),
    InventoryItem(product_id=4, quantity=50),
    InventoryItem(product_id=5, quantity=20),
    InventoryItem(product_id=6, quantity=25),
    InventoryItem(product_id=7, quantity=10),
]

# Proveedores
suppliers = [
    Supplier(id=1, name="Proveedor A", product_id=1, unit_cost=90.0, lead_time_days=3),
    Supplier(id=2, name="Proveedor B", product_id=2, unit_cost=50.0, lead_time_days=2),
    # Añade más si hace falta
]

# BOM: descomposición de cada impresora
bom = [
    # P3D-Classic
    BOMItem(product_id=100, material_id=1, quantity=1),  # kit_piezas
    BOMItem(product_id=100, material_id=2, quantity=1),  # pcb
    BOMItem(product_id=100, material_id=3, quantity=1),  # extrusor
    BOMItem(product_id=100, material_id=4, quantity=2),  # cables_conexion
    BOMItem(product_id=100, material_id=5, quantity=1),  # transformador
    BOMItem(product_id=100, material_id=6, quantity=1),  # enchufe

    # P3D-Pro
    BOMItem(product_id=101, material_id=1, quantity=1),
    BOMItem(product_id=101, material_id=2, quantity=1),
    BOMItem(product_id=101, material_id=3, quantity=1),
    BOMItem(product_id=101, material_id=4, quantity=3),
    BOMItem(product_id=101, material_id=5, quantity=1),
    BOMItem(product_id=101, material_id=6, quantity=1),
    BOMItem(product_id=101, material_id=7, quantity=1),
]

# Pedidos de fabricación simulados
manufacturing_orders = [
    ManufacturingOrder(id=1, created_at=date(2025, 4, 24), product_id=100, quantity=8, status="pending"),
    ManufacturingOrder(id=2, created_at=date(2025, 4, 25), product_id=100, quantity=5, status="pending"),
    ManufacturingOrder(id=3, created_at=date(2025, 4, 25), product_id=101, quantity=4, status="pending"),
    ManufacturingOrder(id=4, created_at=date(2025, 4, 26), product_id=101, quantity=10, status="pending"),
]
