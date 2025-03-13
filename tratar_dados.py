import pandas as pd
import os  # Importar módulo para manipulação de diretórios

def tratar_dados(file_path):
    # Carregar os dados
    df = pd.read_csv(file_path, sep=";", encoding="utf-8")

    # Remover duplicatas
    df = df.drop_duplicates()

    # Padronizar formatos de datas
    def corrigir_data(data):
        formatos = ["%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d", "%d-%m-%Y", "%Y.%m.%d"]
        for formato in formatos:
            try:
                return pd.to_datetime(data, format=formato)
            except ValueError:
                continue
        return None  # Se nenhum formato funcionar, retorna None

    # Aplicar a função para corrigir as datas inválidas
    if "data_venda" in df.columns:
        df["data_venda"] = df["data_venda"].apply(corrigir_data)

    # Preencher valores ausentes de preco_unitario com base no mesmo modelo de veículo
    if "preco_unitario" in df.columns and "modelo" in df.columns:
        def preencher_preco_unitario(row):
            if pd.isna(row["preco_unitario"]):
                preco_existente = df.loc[df["modelo"] == row["modelo"], "preco_unitario"].dropna()
                if not preco_existente.empty:
                    return preco_existente.iloc[0]  # Pega o primeiro valor encontrado
            return row["preco_unitario"]

        df["preco_unitario"] = df.apply(preencher_preco_unitario, axis=1)

    # Substituir valores ausentes na coluna quantidade por zero
    if "quantidade" in df.columns:
        df["quantidade"] = df["quantidade"].fillna(0)

    # Criar a pasta 'dados' caso não exista
    output_dir = "dados"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Salvar os dados limpos
    output_file = os.path.join(output_dir, "dados_producao_limpos.csv")
    df.to_csv(output_file, index=False)
    print(f"Arquivo salvo: {output_file}")
