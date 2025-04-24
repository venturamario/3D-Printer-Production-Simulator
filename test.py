import streamlit as st
from simulator import Simulator
from initial_data import products
import simpy

# Inicializamos la simulación (solo una vez)
if "sim" not in st.session_state:
    st.session_state.env = simpy.Environment()
    st.session_state.sim = Simulator(st.session_state.env)

sim = st.session_state.sim

st.title("📦 Simulador de Producción de Impresoras 3D")
st.subheader(f"🗓 Día actual: {sim.current_date}")

# Crear un diccionario para mapear product_id a display_name
product_display_names = {product.id: product.display_name for product in products}

# Panel de inventario y compras
st.header("📊 Inventario y Compras")

# Mostrar inventario actual
for pid, qty in sim.inventory.items():
    display_name = product_display_names.get(pid, "Nombre desconocido")
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.write(f"Producto {pid}: {display_name}. {qty} unidades")
    
    # Solo mostrar botón de compra si es materia prima y tiene proveedor
    product = next((p for p in products if p.id == pid), None)
    supplier = next((s for s in sim.suppliers if s.product_id == pid), None)
    
    if product and product.type == "raw" and supplier:
        with col2:
            qty_to_order = st.number_input(f"Cantidad {pid}", min_value=1, value=10, key=f"qty_{pid}")
        with col3:
            if st.button(f"🛒 Comprar", key=f"buy_{pid}"):
                po = sim.create_purchase_order(pid, qty_to_order)
                if po:
                    st.success(f"Orden de compra #{po.id} creada. Llegará en {supplier.lead_time_days} días")

# Mostrar órdenes de compra pendientes
if sim.purchase_orders:
    st.subheader("📦 Órdenes de Compra")
    for po in sim.purchase_orders:
        status_emoji = "⏳" if po.status == "pending" else "✅"
        supplier = next(s for s in sim.suppliers if s.id == po.supplier_id)
        product_name = product_display_names.get(po.product_id, "Producto desconocido")
        st.write(f"{status_emoji} OC #{po.id}: {po.quantity} {product_name} de {supplier.name}. "
                f"Estado: {po.status}. Entrega estimada: {po.estimated_delivery}")

# Información sobre materiales necesarios para un producto
st.header("📋 Materiales necesarios para producción")
product_id = st.selectbox("Selecciona un producto terminado:", [100, 101])  # IDs de productos terminados
quantity = st.number_input("Cantidad a producir:", min_value=1, value=1)

if st.button("🔍 Mostrar materiales necesarios"):
    bom = sim.get_bom(product_id, quantity)
    st.subheader(f"Materiales necesarios para producir {quantity} unidades del producto {product_id}:")
    for material_id, qty in bom.items():
        st.write(f"Material {material_id}: {qty} unidades")


# Panel de pedidos
st.header("📝 Pedidos de fabricación")
for order in sim.orders:
    st.write(f"Pedido #{order.id} | Producto: {order.product_id} | Cantidad: {order.quantity} | Estado: {order.status}")
    if order.status == "pending":
        if st.button(f"✅ Liberar pedido #{order.id}"):
            if sim.can_fulfill_order(order):
                sim.consume_inventory(order)
                order.status = "released"
                st.success(f"Pedido #{order.id} liberado y materiales reservados")
            else:
                st.error(f"No hay suficiente stock para liberar el pedido #{order.id}")


# Avanzar día
if st.button("⏭️ Avanzar día"):
    sim.advance_day()

# Eventos del día
st.header("📚 Eventos")
for event in reversed(sim.events[-10:]):
    st.text(f"[{event.date_simulated}] {event.type.upper()}: {event.detail}")
