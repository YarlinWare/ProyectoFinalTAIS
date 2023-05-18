from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import io

app = Flask(__name__)

@app.route('/')
def home():
    return "¡Hola! Por favor, visita la ruta '/grafico' para ver el diagrama."

@app.route('/grafico')
def grafico():
    # Leer el archivo CSV utilizando pandas
    data = pd.read_csv('productos_mas_vendidos.csv')
    # Obtener los valores necesarios para el diagrama
    categorias = data['categoria']
    ventas = data['ventas']
    # Generar el diagrama
    plt.bar(categorias, ventas)
    plt.xlabel('Categorías')
    plt.ylabel('Ventas')
    plt.title('Ventas por Categoría')
    plt.xticks(rotation=45)
    # Guardar el diagrama en un objeto 'io.BytesIO'
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    # Convertir el objeto 'io.BytesIO' en datos base64 para mostrarlo en HTML
    image_base64 = buffer.getvalue().hex()
    # Renderizar la plantilla HTML y pasar los datos del diagrama
    return render_template('grafico.html', image_base64=image_base64)

if __name__ == '__main__':
    app.run()