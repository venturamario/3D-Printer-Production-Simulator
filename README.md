# 3D-Printer-Production-Simulator
Simulador de Producción de Impresoras 3D

## 1. Objetivo del reto
Desarrollar un software que permita simular, día a día, el ciclo completo de una planta que
fabrica impresoras 3D. El enfoque está en la gestión de inventarios, las compras y la
planificación de la producción. El alumno/usuario juega el papel de planificador: decide qué
fabricar y qué comprar.

## 2. Alcance y requisitos
### 2.1 Requisitos funcionales mínimos
Definición de condiciones iniciales: Se determina el plan de producción (materiales
necesarios para la fabricación de cada tipo de impresora y tiempo en la cadena de
montaje), catalogo proveedores ( Productos a la venta, precios x cantidades - ejemplo
precio: por palet de 1000 unidades, precio por caja de 20 unidades - tiempo de
entrega/lead time) , capacidad de almacen ( para simplificar 1 unidad de cualquier
material = 1 unidad almacenaje).
1. Generación de demanda: al iniciar cada día se crean aleatoriamente pedidos de
fabricación (parámetros: media y varianza configurables).
2. Tablero de control: muestra los pedidos pendientes, la lista de materiales (BOM/Bill of
Materials) de cada pedido y el nivel de inventario.
3. Decisiones del usuario:
Liberar pedidos a producción.
Emitir órdenes de compra (elegir producto, proveedor, cantidad y fecha).
4. Simulación de eventos:
Consumo de materias primas y fabricación limitada por capacidad diaria.
Llegada de compras según el lead time del proveedor.
5. Avance de calendario: un botón “Avanzar día” ejecuta las 24 h de simulación.
6. Registro de eventos para históricos y gráficas.
7. Exportación / importación JSON de inventario y eventos.
8. API REST: Toda funcionalidad / información presentada por la interfaz de usuario debe
ser accesible desde una api REST documentada con SWAGGER / OpenAPI

### 2.2 Requisitos no funcionales
- Código claro, comentado y versionado con Git.
- Interfaz web sencilla; ninguna instalación compleja en el cliente
- Compatible con Windows, macOS y Linux.

## 3. Pila tecnológica propuesta
Capa || Herramienta || Motivo

Lenguaje Python 3.11/ 3.12 Ampliamente usado, sintaxis simple.

Simulación SimPy Motor de eventos discretos fácil de usar.

Persistencia SQLite y/o archivo JSON. Ligeros y portables.

Back‑end/API Fastapi + Pydantic Solo si Streamlit no cubre todas las vistas.

Interfaz Streamlit Construcción rápida de dashboards.

Gráficas matplotlib Integración directa en Streamlit.

Control de versiones con Git + GitHub Flujo estándar.

**Para ejecutar la simulación:**  
```bash
streamlit run app.py
