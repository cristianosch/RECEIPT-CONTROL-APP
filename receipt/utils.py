import plotly.graph_objs as go
import plotly.io as pio
import io
import base64
from django.shortcuts import render
from django.utils.safestring import mark_safe


def plot_pie_chart_plotly(data, labels):
    fig = go.Figure(data=[go.Pie(labels=labels, values=data)])
    
    # Salvar a imagem em um buffer de memória
    buffer = io.BytesIO()
    pio.write_image(fig, file=buffer, format='png')
    buffer.seek(0)
    
    # Codificar a imagem em base64
    img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    return img_base64