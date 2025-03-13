# Sistema de Identificação de Dados Sensíveis (SIDS)

## Descrição
O **Sistema de Identificação de Dados Sensíveis (SIDS)** é uma aplicação desenvolvida em **Python** com **Flask** para validar documentos, especialmente PDFs, e identificar dados sensíveis conforme os padrões da **Lei Geral de Proteção de Dados (LGPD)**. O sistema verifica a presença de dados como CPF, CNPJ, RG, emails, números de telefone, dados de saúde, religião, e muito mais.

## Funcionalidades
- **Identificação de Dados Sensíveis**: Detecta a presença de dados sensíveis, como CPF, CNPJ, email, telefone, saúde, religião, etc.
- **Geração de Relatório em PDF**: Gera um relatório com a quantidade de dados sensíveis encontrados no documento.
- **Geração de Gráfico**: Exibe um gráfico visualizando a quantidade de dados sensíveis encontrados.
- **Compliância LGPD**: Exibe uma notificação caso o documento contenha dados sensíveis, informando a necessidade de tratamento conforme a LGPD.

## Tecnologias Usadas
- **Python**
- **Flask** para a construção da aplicação web
- **PyPDF2** para extração de texto de documentos PDF
- **FPDF** para geração de PDFs
- **Matplotlib** para criação de gráficos

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seuusuario/SIDS.git
