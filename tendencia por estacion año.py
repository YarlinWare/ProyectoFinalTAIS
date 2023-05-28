import pandas as pd

# Cargar los datos de visitas de productos y su clasificación por categoría del último año
datos_visitas = pd.read_csv('datos_visitas.csv')
datos_categorias = pd.read_csv('datos_categorias.csv')

# Combinar los datos de visitas y categorías por algún campo en común (por ejemplo, el ID del producto)
datos_combinados = pd.merge(datos_visitas, datos_categorias, on='product_id')

# Convertir la columna de fecha a formato de fecha en Pandas
datos_combinados['fecha'] = pd.to_datetime(datos_combinados['fecha'])

# Extraer el año y la estación de la fecha
datos_combinados['año'] = datos_combinados['fecha'].dt.year
datos_combinados['estacion'] = datos_combinados['fecha'].dt.quarter.apply(lambda x: 'Primavera' if x == 1 else 'Verano' if x == 2 else 'Otoño' if x == 3 else 'Invierno')

# Agrupar los datos por categoría, año y estación, y obtener los productos con más visitas por tendencia en cada grupo
productos_mas_visitados = datos_combinados.groupby(['categoria', 'año', 'estacion'])['visitas'].nlargest(1).reset_index()

# Guardar el resultado en un archivo CSV
productos_mas_visitados.to_csv('productos_mas_visitados.csv', index=False)