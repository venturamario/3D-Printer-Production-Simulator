import streamlit as st
from simulator import Simulator
from initial_data import products
import simpy
import pandas as pd

# Inicializamos la simulación (solo una vez)
if "sim" not in st.session_state:
    st.session_state.env = simpy.Environment()
    st.session_state.sim = Simulator(st.session_state.env)

sim = st.session_state.sim

st.title("📦 Simulador de Producción de Impresoras 3D")
st.subheader(f"🗓 Día actual: {sim.current_date}")

# Crear un diccionario para mapear product_id a display_name
product_display_names = {product.id: product.display_name for product in products}

# Panel de inventario
st.header("📊 Inventario")

# Convert inventory to a DataFrame for tabular display
inventory_data = [
    {
        "ID Material": pid,
        "Nombre": product_display_names.get(pid, "Nombre desconocido"),
        "Stock Total": qty,
        "Reservado": sim.reserved_materials.get(pid, 0),
        "Stock Resultante": qty - sim.reserved_materials.get(pid, 0)
    }
    for pid, qty in sim.inventory.items()
]
inventory_df = pd.DataFrame(inventory_data)

# Display the inventory as a table
st.table(inventory_df)

# Panel de Compras
st.header("🛒 Compras de Materiales")

# Incluir todos los productos (materias primas y productos terminados)
all_materials = products

if all_materials:
    # Selector de material
    selected_material = st.selectbox(
        "Seleccionar material a comprar",
        all_materials,
        format_func=lambda x: f"{x.display_name} (ID: {x.id})"
    )

    if selected_material:
        # Buscar un proveedor para el material seleccionado
        supplier = next((s for s in sim.suppliers if s.product_id == selected_material.id), None)
        current_stock = sim.inventory.get(selected_material.id, 0)

        col1, col2 = st.columns(2)
        with col1:
            if supplier:
                st.info(f"💰 Precio unitario: {supplier.unit_cost}€")
                st.info(f"⏳ Tiempo de entrega: {supplier.lead_time_days} días")
            else:
                st.warning("⚠️ No hay proveedor disponible para este material.")
            st.info(f"📊 Stock actual: {current_stock} unidades")

        with col2:
            qty_to_order = st.number_input(
                "Cantidad a ordenar",
                min_value=1,
                value=10,
                help="Introduce la cantidad de unidades que deseas comprar"
            )

            if supplier:
                total_cost = qty_to_order * supplier.unit_cost
                st.write(f"💲 Coste total: {total_cost}€")

                if st.button("📦 Crear Orden de Compra"):
                    po = sim.create_purchase_order(selected_material.id, qty_to_order)
                    if po:
                        st.success(
                            f"Orden de compra #{po.id} creada\n" \
                            f"Material: {selected_material.display_name}\n" \
                            f"Cantidad: {qty_to_order} unidades\n" \
                            f"Coste total: {total_cost}€\n" \
                            f"Fecha estimada de entrega: {po.estimated_delivery}"
                        )
            else:
                st.error("No se puede crear una orden de compra sin un proveedor.")

# Mostrar órdenes de compra
if sim.purchase_orders:
    st.subheader("📆 Órdenes de Compra Activas")
    
    # Separar órdenes pendientes y entregadas
    pending_orders = [po for po in sim.purchase_orders if po.status == "pending"]
    delivered_orders = [po for po in sim.purchase_orders if po.status == "delivered"]

    if pending_orders:
        st.write("⏳ Pendientes de entrega:")
        for po in pending_orders:
            supplier = next(s for s in sim.suppliers if s.id == po.supplier_id)
            product_name = product_display_names.get(po.product_id, "Producto desconocido")
            days_left = (po.estimated_delivery - sim.current_date).days
            
            st.info(
                f"OC #{po.id}: {po.quantity} unidades de {product_name}\n" \
                f"Proveedor: {supplier.name}\n" \
                f"Entrega en: {days_left} días ({po.estimated_delivery})"
            )

    if delivered_orders:
        st.write("✅ Entregadas recientemente:")
        # Mostrar solo las últimas 5 órdenes entregadas
        for po in delivered_orders[-5:]:
            supplier = next(s for s in sim.suppliers if s.id == po.supplier_id)
            product_name = product_display_names.get(po.product_id, "Producto desconocido")
            
            st.success(
                f"OC #{po.id}: {po.quantity} unidades de {product_name}\n" \
                f"Proveedor: {supplier.name}\n" \
                f"Entregada el: {po.estimated_delivery}"
            )

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
        if st.button(f"🔒 Reservar materiales #{order.id}"):
            if sim.can_fulfill_order(order):
                sim.reserve_materials(order)
                order.status = "reserved"
                st.success(f"Pedido #{order.id}: Materiales reservados")
            else:
                st.error(f"No hay suficiente stock para el pedido #{order.id}")
    elif order.status == "reserved":
        if st.button(f"✅ Liberar pedido #{order.id}"):
            sim.consume_inventory(order)
            order.status = "completed"
            st.success(f"Pedido #{order.id} completado y materiales consumidos")


# Avanzar día
if st.button("⏭️ Avanzar día"):
    sim.advance_day()

# Eventos del día
st.header("📚 Eventos")
for event in reversed(sim.events[-10:]):
    st.text(f"[{event.date_simulated}] {event.type.upper()}: {event.detail}")
