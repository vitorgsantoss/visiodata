from google import genai
from dotenv import load_dotenv
import os
import pandas as pd  # type:ignore

# Carrega variáveis de ambiente
load_dotenv('dotenv_files/.env')
API_KEY = os.getenv('API_KEY')

# Inicializa o cliente da IA
client = genai.Client(api_key=API_KEY)

def analisar_planilha(caminho_arquivo):
    # Carrega a planilha
    df = pd.read_csv(caminho_arquivo)
    
    # Converte os dados para string para enviar à IA
    dados_str = df.to_string()  # Envia apenas as primeiras 20 linhas para evitar excesso de dados
    
    prompt = f"""
    Aqui está um trecho dos dados de vendas da Ford do Brasil:
    {dados_str}
    
    Sabendo que deve retornar apenas o conteúdo do HTML, iniciando com <html> e 
    terminando com </html> para renderização na aplicação, analise os dados e forneça 
    insights relevantes, incluindo padrões de vendas, modelos mais vendidos, variações 
    sazonais, concessionárias com melhor desempenho (informe qual o percentual de vendas 
    das concessionárias com relação a todas as vendas da Ford em uma tabela HTML), tendências ao longo do 
    tempo e qualquer outra informação útil. Se possível, identifique oportunidades de 
    melhoria ou desafios para a empresa. Apresente os resultados de maneira objetiva.
    """
    
    # Chama a IA
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    
    # Retorna a resposta da IA (presumivelmente HTML formatado)
    template = extrair_html(response.text)
    return template


def extrair_html(texto):
    if '<html>' in texto:
        inicio = texto.find('<html')
        fim = texto.find('</html>')
        template = texto[inicio:fim]+'</html>'
        return template
    return f'Houve um problema ao gerar insights, tente novamente'



