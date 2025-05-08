from datetime import date
from models import Product, InventoryItem, Supplier, BOMItem, ManufacturingOrder

# Productos
products = [
    Product(id=1, name="kit_piezas", type="raw", display_name="Kit de piezas"),
    Product(id=2, name="pcb", type="raw", display_name="PCB"),
    Product(id=3, name="extrusor", type="raw", display_name="Extrusor"),
    Product(id=4, name="cables_conexion", type="raw", display_name="Cables de conexión"),
    Product(id=5, name="transformador_24v", type="raw", display_name="Transformador 24V"),
    Product(id=6, name="enchufe_schuko", type="raw", display_name="Enchufe Schuko"),
    Product(id=7, name="sensor_autonivel", type="raw", display_name="Sensor de autonivelación"),
    Product(id=8, name="P3D-Classic", type="finished", display_name="Impresora 3D Classic"),
    Product(id=9, name="P3D-Pro", type="finished", display_name="Impresora 3D Pro"),
    Product(id=10, name="P3D-Pro-Plus", type="finished", display_name="Impresora 3D Pro Plus"),
    Product(id=11, name="P3D-Pro-XL", type="finished", display_name="Impresora 3D Pro XL")
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
    InventoryItem(product_id=8, quantity=3),  # P3D-Classic
    InventoryItem(product_id=9, quantity=6),  # P3D-Pro
    InventoryItem(product_id=10, quantity=45),  # P3D-Pro-Plus
    InventoryItem(product_id=11, quantity=8),  # P3D-Pro-XL
]

# Proveedores
suppliers = [
    Supplier(id=1, name="Proveedor A", product_id=1, unit_cost=90.0, lead_time_days=3),  # kit_piezas
    Supplier(id=2, name="Proveedor B", product_id=2, unit_cost=50.0, lead_time_days=2),  # pcb
    Supplier(id=3, name="Proveedor C", product_id=3, unit_cost=120.0, lead_time_days=4),  # extrusor
    Supplier(id=4, name="Proveedor D", product_id=4, unit_cost=15.0, lead_time_days=1),  # cables_conexion
    Supplier(id=5, name="Proveedor E", product_id=5, unit_cost=60.0, lead_time_days=3),  # transformador_24v
    Supplier(id=6, name="Proveedor F", product_id=6, unit_cost=10.0, lead_time_days=2),  # enchufe_schuko
    Supplier(id=7, name="Proveedor G", product_id=7, unit_cost=25.0, lead_time_days=3),  # sensor_autonivel
    Supplier(id=8, name="Proveedor H", product_id=8, unit_cost=300.0, lead_time_days=5),  # P3D-Classic
    Supplier(id=9, name="Proveedor I", product_id=9, unit_cost=500.0, lead_time_days=6),  # P3D-Pro
    Supplier(id=10, name="Proveedor J", product_id=10, unit_cost=700.0, lead_time_days=7),  # P3D-Pro-Plus
    Supplier(id=11, name="Proveedor K", product_id=11, unit_cost=1000.0, lead_time_days=8),  # P3D-Pro-XL
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
