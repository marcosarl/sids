from flask import Flask, request, render_template_string, send_file
import PyPDF2
import re
import os
from fpdf import FPDF
import matplotlib.pyplot as plt

app = Flask(__name__)

# Extrai texto diretamente do arquivo
def extrair_texto_pdf(arquivo):
    texto = ""
    reader = PyPDF2.PdfReader(arquivo)
    for page in reader.pages:
        texto += page.extract_text() + '\n'
    return texto

# Valida dados e retorna contagens
def validar_dados(texto):
    padroes = {
        "CPFs encontrados": r'\d{3}\.\d{3}\.\d{3}-\d{2}',
        "CNPJs encontrados": r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}',
        "Emails encontrados": r'[\w\.-]+@[\w\.-]+\.\w+',
        "RGs encontrados": r'\d{2}\.\d{3}\.\d{3}-\d{1}',
        "Telefones encontrados": r'\(\d{2}\) \d{4,5}-\d{4}',
        "Raça encontrados": r'\b(?:branca|negra|parda|amarela|indígena)\b',
        "Religião encontrados": r'\b(?:católica|protestante|budista|muçulmana|espírita|ateu)\b',
        "Política encontrados": r'\b(?:direita|esquerda|centro)\b',
        "Saúde encontrados": r'\b(?:diabetes|hipertensão|alergia|câncer|asmático)\b',
        "Orientação sexual encontrados": r'\b(?:heterossexual|homossexual|bissexual|pansexual)\b',
        "Dados Biométricos encontrados": r'\b(?:biometria|impressão digital|reconhecimento facial)\b'
    }
    resultado = {k: re.findall(v, texto) for k, v in padroes.items()}
    return resultado

# Gera PDF com resultados
def gerar_pdf(resultado):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Relatório de Validação LGPD", ln=True, align='C')
    pdf.ln(10)
    for chave, valores in resultado.items():
        pdf.cell(0, 10, f'{chave}: {len(valores)} encontrado(s)', ln=True)
    pdf_path = "relatorio.pdf"
    pdf.output(pdf_path)
    return pdf_path

# Gera gráfico de barras com resultados
def gerar_grafico(resultado):
    categorias = resultado.keys()
    contagens = [len(v) for v in resultado.values()]
    plt.figure(figsize=(8, 6))
    plt.bar(categorias, contagens, color='skyblue')
    plt.xticks(rotation=45, ha="right")
    plt.title('Resultados da Validação')
    plt.tight_layout()
    grafico_path = "grafico.png"
    plt.savefig(grafico_path)
    plt.close()
    return grafico_path

# Rota principal
html_template = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <title>Validador de Documentos</title>
    <style>
        .resultados {
            font-family: Arial, sans-serif;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 8px;
            background-color: #f8f9fa;
        }
        .resultados .linha {
            font-size: 14px; /* Font size reduced */
            color: #495057;
            margin-bottom: 10px;
        }
        .resultados .titulo {
            font-weight: bold;
            color: #007bff;
            margin-bottom: 15px; /* Espaço entre título e resultados */
        }
        .aviso {
            background-color: #f8d7da;
            color: #721c24;
            padding: 15px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 20px;
            border-radius: 5px;
        }
        .aviso-lgpd {
            background-color: #fff3cd;
            color: #856404;
            padding: 15px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 20px;
            border-radius: 5px;
        }
        .botao-container {
            margin-top: 20px; /* Adicionando espaço superior */
            margin-bottom: 30px; /* Adicionando espaço inferior */
        }
    </style>
    <script>
        function limparResultados() {
            window.location.href = "/";
        }
    </script>
</head>
<body class="container mt-5">
    <h1 class="text-center"> SIDS | Sistema de Identificação de Dados Sensíveis </h1>
    <form method="POST" enctype="multipart/form-data" class="text-center my-4">
        <input type="file" name="file" accept="application/pdf" required class="form-control-file mb-2">
        <button type="submit" class="btn btn-primary">Validar</button>
        <button type="button" class="btn btn-secondary" onclick="limparResultados()">Limpar</button>
    </form>

    {% if resultado %}
        {% set dados_sensiveis = resultado | selectattr('0', 'ne', '') | list %}
        {% if dados_sensiveis %}
            <div class="aviso">
                <strong>Atenção!</strong> O documento contém dados sensíveis.
            </div>
            <div class="aviso-lgpd">
                Este documento deve ser tratado conforme a LGPD | Lei Geral de Proteção de Dados (13.709/2018).
            </div>
        {% endif %}
        <div class="resultados">
            <div class="titulo">Resultados da Validação:</div>
            {% for chave, valores in resultado.items() %}
                <div class="linha">
                    <strong>{{ chave }}:</strong> {{ valores | length }} encontrado(s)
                </div>
            {% endfor %}
        </div>
        <div class="text-center botao-container">
            <a href="/download_pdf" class="btn btn-success">Baixar Relatório PDF</a>
            <a href="/download_grafico" class="btn btn-info">Ver Gráfico</a>
        </div>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    if request.method == 'POST':
        arquivo = request.files['file']
        if arquivo and arquivo.filename.endswith('.pdf'):
            texto = extrair_texto_pdf(arquivo)
            resultado = validar_dados(texto)
            gerar_pdf(resultado)
            gerar_grafico(resultado)
    return render_template_string(html_template, resultado=resultado)

@app.route('/download_pdf')
def download_pdf():
    return send_file("relatorio.pdf", as_attachment=True)

@app.route('/download_grafico')
def download_grafico():
    return send_file("grafico.png", as_attachment=False)

if __name__ == '__main__':
    app.run(debug=True)

