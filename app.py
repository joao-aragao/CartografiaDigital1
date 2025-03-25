from flask import Flask, render_template, jsonify
import pandas as pd
import os

app = Flask(__name__)

current_directory = os.path.dirname(os.path.abspath(__file__))

# Nome do arquivo que você deseja ler
file_name = 'cartografia_db_simples_versao_final.xlsx'

# Caminho completo para o arquivo
file_path = os.path.join(current_directory, file_name)

# Função para carregar dados do Excel
def load_data():
    try:
        # Verifica se o arquivo existe
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Arquivo {file_name} não encontrado no diretório {current_directory}")
        
        # Lendo o arquivo Excel
        df = pd.read_excel(file_path)
        
        # Limpar espaços em branco dos nomes das colunas, caso haja
        df.columns = df.columns.str.strip()

        # Selecionando as colunas relevantes
        data = df[['LATITUDE', 'LONGITUDE', 'NOME', 'TEMA', 'ENDERECO', 
               'DIAS_DE_FUNCIONAMENTO', 'HORARIO_DE_FUNCIONAMENTO', 
               'OUTROS_DIAS_DE_FUNCIONAMENTO', 'OUTROS_HORARIO_DE_FUNCIONAMENTO',
               'ESPECIALIDADES', 'OBSERVAÇÕES', 'TELEFONE', 'NUM', 
                'Fluxo_de_entrada', 'Fluxo_de_saida', 
               'Total_Inf', 'PROGRAMAS','LINK_LOCAL']].dropna()
        

        # Contando a quantidade de aparelhos por categoria
        category_counts = data['TEMA'].value_counts().to_dict()

        return data.to_dict(orient='records'), category_counts
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        return [], {}

@app.route('/')
def index():
    return render_template('map.html')

@app.route('/pins')
def get_pins():
    # Carregar os dados do arquivo Excel
    data, category_counts = load_data()
    
    # Enviar dados e contagem de categorias
    return jsonify({
        'data': data,
        'category_counts': category_counts
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
