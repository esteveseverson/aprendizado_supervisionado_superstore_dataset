from flask import Flask, render_template, request
from datetime import datetime
import pandas as pd
from pypmml import Model

app = Flask(__name__)

# Carregar o modelo PMML
model = Model.load('pmml/pmml_tcd3.pmml')

# Valores mínimos e máximos para normalização (ajuste conforme necessário)
min_values = {
    'Ano_Nascimento': 1893,
    'Escolaridade': 0,
    'Renda': 1730,
    'Criancas_Casa': 0,
    'Adolescentes_Casa': 0,
    'Recencia': 0,
    'Gasto_Vinhos': 0,
    'Gasto_Frutas': 0,
    'Gasto_Carnes': 0,
    'Gasto_Peixes': 0,
    'Gasto_Doces': 0,
    'Gasto_Ouro': 0,
    'Num_Ofertas_Compras': 0,
    'Num_Compras_Web': 0,
    'Num_Compras_Catalogo': 0,
    'Num_Compras_Loja': 0,
    'Num_Visitas_Web_Mes': 0,
}

max_values = {
    'Ano_Nascimento': 2000,
    'Escolaridade': 4,
    'Renda': 667000,
    'Criancas_Casa': 5,
    'Adolescentes_Casa': 5,
    'Recencia': 99,
    'Gasto_Vinhos': 1493,
    'Gasto_Frutas': 199,
    'Gasto_Carnes': 1725,
    'Gasto_Peixes': 259,
    'Gasto_Doces': 263,
    'Gasto_Ouro': 362,
    'Num_Ofertas_Compras': 15,
    'Num_Compras_Web': 27,
    'Num_Compras_Catalogo': 28,
    'Num_Compras_Loja': 13,
    'Num_Visitas_Web_Mes': 20,
}

# Função para normalizar os dados
def normalize_data(data):
    normalized_data = {}
    for key, value in data.items():
        if key in min_values and key in max_values:
            min_val = min_values[key]
            max_val = max_values[key]
            normalized_data[key] = (float(value) - min_val) / (max_val - min_val)
        else:
            normalized_data[key] = float(value)
    return normalized_data

@app.route('/', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        # Receber e processar os dados do formulário
        data = {
            'Ano_Nascimento': request.form['Ano_Nascimento'],
            'Escolaridade': int(request.form['Escolaridade']),
            'Renda': request.form['Renda'],
            'Criancas_Casa': request.form['Criancas_Casa'],
            'Adolescentes_Casa': request.form['Adolescentes_Casa'],
            'Recencia': request.form['Recencia'],
            'Gasto_Vinhos': request.form['Gasto_Vinhos'],
            'Gasto_Frutas': request.form['Gasto_Frutas'],
            'Gasto_Carnes': request.form['Gasto_Carnes'],
            'Gasto_Peixes': request.form['Gasto_Peixes'],
            'Gasto_Doces': request.form['Gasto_Doces'],
            'Gasto_Ouro': request.form['Gasto_Ouro'],
            'Num_Ofertas_Compras': request.form['Num_Ofertas_Compras'],
            'Num_Compras_Web': request.form['Num_Compras_Web'],
            'Num_Compras_Catalogo': request.form['Num_Compras_Catalogo'],
            'Num_Compras_Loja': request.form['Num_Compras_Loja'],
            'Num_Visitas_Web_Mes': request.form['Num_Visitas_Web_Mes']
        }
        
        # Normalizar os dados
        normalized_data = normalize_data(data)
        
        # Fazer a predição
        prediction = model.predict(pd.DataFrame([normalized_data]))
        
        # Renderizar o template de resultado com os dados da predição
        return render_template('resultado.html', resultado=prediction)
    
    return render_template('formulario.html')



if __name__ == '__main__':
    app.run(debug=True)
