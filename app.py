import pandas as pd
import plotly.express as px
import streamlit as st

# Cargar los datos
car_data = pd.read_csv("vehicles_us.csv")

# Limpiar los datos
car_data.columns = car_data.columns.str.strip()
car_data['model_year'] = pd.to_numeric(car_data['model_year'], errors='coerce')
car_data['price'] = pd.to_numeric(car_data['price'], errors='coerce')
car_data['odometer'] = pd.to_numeric(car_data['odometer'], errors='coerce')

# Reemplazar valores nulos
car_data['model_year'] = car_data['model_year'].fillna(-1).astype('Int64')
car_data['price'] = car_data['price'].fillna(-1)
car_data['odometer'] = car_data['odometer'].fillna(-1)
car_data = car_data.fillna("N/A")  # Resto de columnas categóricas

# Extraer la marca del coche (asumiendo que la marca es la primera palabra en el nombre del modelo)
car_data['brand'] = car_data['model'].str.split().str[0]

# Lista de marcas base para el filtro
base_brands = ['acura', 'bmw', 'buick', 'cadillac', 'chevrolet', 'chrysler', 'dodge', 'ford', 'gmc', 'honda', 
               'hyundai', 'jeep', 'kia', 'mercedes-benz', 'nissan', 'ram', 'subaru', 'toyota', 'volkswagen']

# Título principal
st.title("Análisis Dinámico de Venta de Coches")


# Filtros dinámicos
st.sidebar.header("Filtrar datos")

# Filtro para seleccionar marca
selected_brand = st.sidebar.selectbox("Selecciona una marca", options=['Todas las marcas'] + base_brands)

# Rango de precios
valid_prices = car_data[car_data['price'] > 0]['price']
min_price, max_price = int(valid_prices.min()), int(valid_prices.max())
price_range = st.sidebar.slider("Rango de precios", min_price, max_price, (min_price, max_price))

# Rango de años
valid_years = car_data[car_data['model_year'] > 0]['model_year']
min_year, max_year = int(valid_years.min()), int(valid_years.max())
year_range = st.sidebar.slider("Rango de año del modelo", min_year, max_year, (min_year, max_year))

# Rango de kilometraje
valid_odometer = car_data[car_data['odometer'] > 0]['odometer']
min_km, max_km = int(valid_odometer.min()), int(valid_odometer.max())
odometer_range = st.sidebar.slider("Rango de kilometraje", min_km, max_km, (min_km, max_km))

# Condición
conditions = car_data['condition'].unique()
selected_condition = st.sidebar.selectbox("Condición del coche", options=conditions)

# Filtrar los datos según los criterios seleccionados
filtered_data = car_data[
    (car_data['price'].between(*price_range)) &
    (car_data['model_year'].between(*year_range)) &
    (car_data['odometer'].between(*odometer_range)) &
    (car_data['condition'] == selected_condition)
]

# Si se seleccionó una marca, filtrar por esa marca también
if selected_brand != 'Todas las marcas':
    filtered_data = filtered_data[filtered_data['brand'].str.lower() == selected_brand]

st.subheader("Datos filtrados")
st.write(f"Mostrando coches con condición '{selected_condition}', entre los años {year_range[0]} y {year_range[1]}, precios entre ${price_range[0]} y ${price_range[1]}, y kilometraje entre {odometer_range[0]} y {odometer_range[1]} km.")
st.dataframe(filtered_data)  # Mostrar los datos filtrados

# Gráficos con colores personalizados

# Histograma de precios por marca
fig_price = px.histogram(
    filtered_data, 
    x="price", 
    title="Distribución de precios por Marca", 
    color="brand",  # Agrupamos por marca
    color_discrete_sequence=px.colors.qualitative.Set3  # Colores diferenciados para cada marca
)
st.plotly_chart(fig_price, use_container_width=True)

# Gráfico de dispersión año vs precio por marca
fig_scatter = px.scatter(
    filtered_data, 
    x="model_year", 
    y="price", 
    title="Año del modelo vs Precio por Marca", 
    color="brand",  # Agrupamos por marca
    color_discrete_sequence=px.colors.qualitative.Set3
)
st.plotly_chart(fig_scatter, use_container_width=True)

# Histograma de kilometraje por marca
fig_odometer = px.histogram(
    filtered_data, 
    x="odometer", 
    title="Distribución de kilometraje por Marca", 
    color="brand",  # Agrupamos por marca
    color_discrete_sequence=px.colors.qualitative.Set3
)
st.plotly_chart(fig_odometer, use_container_width=True)

# Distribución global de condiciones por marca
cond_df = car_data.groupby(['condition', 'brand']).size().reset_index(name='Cantidad')
fig_condition = px.bar(
    cond_df, 
    x='brand', 
    y='Cantidad', 
    color='brand', 
    title="Distribución de condiciones por Marca",
    color_discrete_sequence=px.colors.qualitative.Set3
)
st.plotly_chart(fig_condition, use_container_width=True)

