from application import app
from flask import render_template, url_for, request
import pandas as pd
import json
import plotly
import plotly.express as px
import chardet
import plotly.graph_objects as go
import numpy as np
from collections import Counter

import get_categories
import get_price_prod_item
import get_sold
import get_trends

@app.route("/", methods=['GET', 'POST'])
def index():
    
    with open('products_info.csv', 'rb') as f:
        enc = chardet.detect(f.read())  # or readline if the file is large
    
    df= pd.read_csv('products_info.csv', encoding = enc['encoding'])

    df = df.sort_values(by=['sold_quantity'])
    df = df[df.sold_quantity > 3000]

    fig1 = px.bar(df, x="title", y= "sold_quantity", title="")
    fig1.update_layout(
        autosize=False,
        width=950,
        height=424,
        xaxis_title ="Producto",
        yaxis_title = "Cantidad vendida"
        )

    graphJSON1 = json.dumps(fig1, cls =plotly.utils.PlotlyJSONEncoder)

    df2 = df
    df2 = df2.sort_values(by=['rating_average'])
    fig2 = px.pie(df2, values='rating_average', names='rating_average')
    fig2.update_layout(
        autosize=False,
        width=324,
        height=324,
        )
    
    graphJSON2 = json.dumps(fig2, cls =plotly.utils.PlotlyJSONEncoder)

    with open('trends.csv', 'rb') as f:
        enc = chardet.detect(f.read())  # or readline if the file is large
    
    df3= pd.read_csv('trends.csv', encoding = enc['encoding'])

    fig3 = go.Figure(data=[go.Table(
    header=dict(values=list(df3.columns),
                fill_color='#4e73df',
                align='left'),
    cells=dict(values=[df3.keyword, df3.url],
               fill_color='#EFF2FB',
               align='left'))
    ])
    fig3.update_layout(
        autosize=True,
        #width=900,
        height=324,
        title_text=""
        )

    graphJSON3 = json.dumps(fig3, cls =plotly.utils.PlotlyJSONEncoder)

    with open('products_info.csv', 'rb') as f:
        enc = chardet.detect(f.read())  # or readline if the file is large

    df4= pd.read_csv('products_info.csv', encoding = enc['encoding'])

    df4 = df4.sort_values(by=['visits'])
    df4 = df4[df4.visits > 3000]

    fig4 = px.bar(df, x="visits", y= "title", title="", orientation='h')
    fig4.update_layout(
        autosize=False,
        width=900,
        height=724,
        xaxis_title ="Visitas",
        yaxis_title = "Producto"
        )

    graphJSON4 = json.dumps(fig4, cls =plotly.utils.PlotlyJSONEncoder)

    min_1 = df['sold_quantity'].min()
    max_1 = df['sold_quantity'].max()
    mean_1 = df['sold_quantity'].mean()
    std_1 = df['sold_quantity'].std()

    min_2 = df2['rating_average'].min()
    max_2 = df2['rating_average'].max()
    mean_2 = df2['rating_average'].mean()
    std_2 = df2['rating_average'].std()

    series_df3 = np.asarray(df3['keyword'])
    list_words = []

    for x in series_df3:
        words = x.split()
        for w in words:
            list_words.append(w)
        

    word_counts = Counter(list_words)
    info_df3 = word_counts.most_common(5)

    min_4 = df2['visits'].min()
    max_4 = df2['visits'].max()
    mean_4 = df2['visits'].mean()
    std_4 = df2['visits'].std()

    mean_1 = round(mean_1 , 3)
    mean_2 = round(mean_2 , 3)
    mean_4 = round(mean_4 , 3)

    std_1 = round(std_1 , 3)
    std_2 = round(std_2 , 3)
    std_4 = round(std_4 , 3)

    return render_template("index.html", graphJSON1 = graphJSON1, graphJSON2 = graphJSON2, graphJSON3 = graphJSON3, graphJSON4 = graphJSON4,
    min_df1 = min_1, max_df1 = max_1, mean_df1 = mean_1, desv_df1 = std_1, min_df2 = min_2, max_df2 = max_2, mean_df2 = mean_2, desv_df2 = std_2,
    min_df4 = min_4, max_df4 = max_4, mean_df4 = mean_4, desv_df4 = std_4, info_df3 = info_df3)

