import streamlit as st
from simulator import Simulator
import simpy

# Inicializamos la simulación (solo una vez)
if "sim" not in st.session_state:
    st.session_state.env = simpy.Environment()
    st.session_state.sim = Simulator(st.session_state.env)

sim = st.session_state.sim

st.title("📦 Simulador de Producción de Impresoras 3D")
st.subheader(f"🗓 Día actual: {sim.current_date}")

# Panel de inventario
st.header("📊 Inventario")
for pid, qty in sim.inventory.items():
    st.write(f"Producto {pid}: {qty} unidades")

# Panel de pedidos
st.header("📝 Pedidos de fabricación")
for order in sim.orders:
    st.write(f"Pedido #{order.id} | Producto: {order.product_id} | Cantidad: {order.quantity} | Estado: {order.status}")
    if order.status == "pending":
        if st.button(f"✅ Liberar pedido #{order.id}"):
            order.status = "released"

# Avanzar día
if st.button("⏭️ Avanzar día"):
    sim.advance_day()

# Eventos del día
st.header("📚 Eventos")
for event in reversed(sim.events[-10:]):
    st.text(f"[{event.date_simulated}] {event.type.upper()}: {event.detail}")
