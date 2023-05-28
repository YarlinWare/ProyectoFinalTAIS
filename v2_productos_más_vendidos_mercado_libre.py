# -*- coding: utf-8 -*-
"""v2 Productos más vendidos mercado libre.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SImqhURDApXALeThia9EQRxBhOlE0Gel

# Top 15 de los productos más vendidos por año en Colombia

Productos 15 más vendidos de cada año de los últimos 3 años en MercadoLibre

Integrantes: 

*   Cristhian Mauricio Yara Pardo -20181020081
*   Laurent David Chaverra Córdoba - 20171020082
"""

# Importando librerias
import requests
import pandas as pd

# Variables de configuración
token = 'N6opXnSFgJRcqNLwUY4kI3rzM8Fuxz4q'  # Reemplaza con tu propio token de acceso a la API de Mercado Libre
anio_actual = 2023  # Año actual
ultimos_anios = 3  # Cantidad de años anteriores a considerar

# Obtener la lista de categorías de tecnología en Mercado Libre
url_categorias = 'https://api.mercadolibre.com/sites/MLA/categories'
response = requests.get(url_categorias)
categorias = response.json()

# Obtener los productos más vendidos por categoría y año
productos_mas_vendidos = []

for categoria in categorias:
    categoria_id = categoria['id']
    
    for anio in range(anio_actual - ultimos_anios, anio_actual + 1):
        url_productos = f'https://api.mercadolibre.com/sites/MLA/search?category={categoria_id}&sort=sold_quantity_desc&limit=15&buying_mode=buy_it_now&currency=ARS&date_from={anio}-01-01T00:00:00.000-00:00&date_to={anio}-12-31T23:59:59.999-00:00&access_token={token}'
        response = requests.get(url_productos)
        data = response.json()
        
        for producto in data['results']:
            detalles_producto = {
                'Año': anio,
                'Categoría': categoria['name'],
                'Producto': producto['title'],
                'Precio': producto['price'],
                'Moneda': producto['currency_id'],
                'Condición': producto['condition'],
                'Cantidad Vendida': producto['sold_quantity']
            }
            productos_mas_vendidos.append(detalles_producto)

# Convertir los datos en un DataFrame de Pandas
df_productos_mas_vendidos = pd.DataFrame(productos_mas_vendidos)

# Guardar el resultado en un archivo CSV
df_productos_mas_vendidos.to_csv('productos_mas_vendidos.csv', index=False)

print("Dataset generado exitosamente.")