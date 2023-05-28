# -*- coding: utf-8 -*-
"""Productos peor valorados en mercado libre.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11pBmj9q4jv0iPlun9NEN28Tgg_0qxhhC

# Productos Más Vendidos Peor Valorados

Los 15 productos de tecnología más vendidos de cada años de los últimos 3 años en Colombia, con sus detalles, peor valorado por los usuarios en MercadoLibre.


Integrantes: 

*   Cristhian Mauricio Yara Pardo -20181020081
*   Laurent David Chaverra Córdoba - 20171020082
"""

import requests
import json
import pandas as pd
import time

# Definir variables para hacer la consulta a la API de Mercado Libre
pais = "MCO"  # Código de país para Colombia
limite = 15   # Límite de productos por año
categorias = ["MCO1055", "MCO1648"]#, "MCO1000", "MCO1039", "MCO1649"]  # Categorías de productos de tecnología
anios = [2018, 2019, 2020, 2021, 2022]

# Verificamos que la lista de categorías sea la indicada
for categoria in categorias:
    url = f"https://api.mercadolibre.com/categories/{categoria}"
    response = requests.get(url)
    if response.status_code == 200:
        categoria_data = response.json()
        categoria_nombre = categoria_data.get("name")
        print(f"Categoría {categoria}: {categoria_nombre}")
    else:
        print(f"Error al obtener la categoría {categoria}: {response.status_code}")

client_id = '5052533537567494'
client_secret = 'N6opXnSFgJRcqNLwUY4kI3rzM8Fuxz4q'

# Obtener token de desarrollador para poder realizar consultas
def obtener_token(client_id, client_secret):
    url = 'https://api.mercadolibre.com/oauth/token'
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        return '&%$QWETERSDF##"$DSFSEFD'

token = obtener_token(client_id, client_secret)

def buscar_productos(categoria, pais, anio):
    url = f"https://api.mercadolibre.com/sites/{pais}/search?category={categoria}&sold_quantity={anio}-01-01,{anio}-12-31&sort=sold_quantity_desc"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Definir la función para hacer consultas a la API de Mercado Libre
def consultar_productos_por_anio(anio):
    # Hacer una consulta a la API de Mercado Libre para obtener los productos más vendidos de cada categoría en el año especificado
    # url = f"https://api.mercadolibre.com/sites/{pais}/search?category={','.join(categorias)}&sort=sold_quantity_desc&deal_ids=MLC{anio}"
    url = f"https://api.mercadolibre.com/sites/MCO/search?category=MCO1055&&sort=sold_quantity_desc&deal_ids=MLC{anio}"
    headers = {'Authorization': 'Bearer ' + token}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error al consultar productos para el año {anio}: {response.status_code}")
        return []
    
    # Extraer la información de los productos y calcular su calificación más baja
    print(response.json())
    productos = response.json()["results"][:limite]
    for producto in productos:
        # Hacer una consulta a la API de Mercado Libre para obtener los detalles del producto
        url_producto = f"https://api.mercadolibre.com/items/{producto['id']}/reviews"
        response_producto = requests.get(url_producto)
        if response_producto.status_code != 200:
            print(f"Error al consultar detalles del producto {producto['id']}: {response_producto.status_code}")
            continue
        if response_producto.json() and response_producto.json()["reviews"]:
          # Calcular la calificación más baja del producto
          calificaciones = response_producto.json()["reviews"]
          calificaciones.sort(key=lambda c: c["rating"], reverse=True)
          calificacion_mas_baja = calificaciones[-1]["rating"] if calificaciones else None
          
          # Agregar la información de los detalles y la calificación más baja al diccionario del producto
          producto["calificacion_mas_baja"] = calificacion_mas_baja
          producto.update(response_producto.json())
    return productos



# Crear una lista de diccionarios con la información de los productos de los últimos 3 años
productos_totales = []
for anio in anios:
    productos_por_anio = consultar_productos_por_anio(anio)
    productos_totales.extend(productos_por_anio)
    print(productos_por_anio)
    print(productos_totales)
    time.sleep(1)  # Esperar 1 segundo entre consultas para evitar superar el límite de consultas permitido

# Crear un dataframe de pandas con la información de los productos
df_productos = pd.DataFrame(productos_totales)

# Guardar el dataframe en un archivo CSV
df_productos.to_csv("productos.csv", index=False)

print(df_productos)