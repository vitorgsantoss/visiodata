
# VisioData

VisioData é uma aplicação desenvolvida para facilitar o upload, processamento e visualização de dados, permitindo a geração de insights de forma eficiente e intuitiva.

## Funcionalidades

- **Upload de Arquivos**: Permite o envio de arquivos de dados para serem processados e analisados.
- **Processamento de Dados**: Realiza o tratamento e a limpeza dos dados enviados, preparando-os para análise.
- **Geração de Insights**: Analisa os dados processados e gera insights significativos.
- **Visualização de Insights**: Exibe os insights gerados de maneira clara e interativa.

## Estrutura do Projeto

- **dados/**: Diretório destinado ao armazenamento dos arquivos de dados enviados.
- **dotenv_files/**: Contém arquivos de configuração e variáveis de ambiente.
- **.gitignore**: Especifica quais arquivos ou pastas devem ser ignorados pelo Git.
- **README.md**: Arquivo que você está lendo atualmente, contendo informações sobre o projeto.
- **gerar_insights.py**: Script responsável pela análise dos dados e geração de insights.
- **home.py**: Script que gerencia a interface principal da aplicação.
- **insight_screen.py**: Script que controla a exibição dos insights gerados.
- **requirements.txt**: Lista de dependências e bibliotecas necessárias para a execução da aplicação.
- **tratar_dados.py**: Script dedicado ao tratamento e limpeza dos dados enviados.
- **upload_arquivos.py**: Script que gerencia o processo de upload dos arquivos de dados.

## Tecnologias Utilizadas

- **Python**: Linguagem principal utilizada no desenvolvimento da aplicação.

## Instalação e Execução

1. Clone o repositório:

   ```bash
   git clone https://github.com/vitorgsantoss/visiodata.git
   ```

2. Navegue até o diretório do projeto:

   ```bash
   cd visiodata
   ```

3. Crie um ambiente virtual:

   ```bash
   python -m venv venv
   ```

4. Ative o ambiente virtual:

   - No Windows:

     ```bash
     venv\Scripts\activate
     ```

   - No macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

5. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

6. Execute a aplicação:

   ```bash
   python home.py
   ```
