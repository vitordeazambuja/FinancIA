import yfinance as yf
import os
import pandas as pd

def download_data(ticker, period="2y", interval="1d"):
    """
    Baixa os dados históricos da ação especificada usando yfinance.
    Salva em cache local na pasta data/historical_data para evitar downloads repetidos.
    """
    os.makedirs("data/historical_data", exist_ok=True)
    file_path = f"data/historical_data/{ticker}_{period}_{interval}.csv"

    # Se já existe, usa cache
    if os.path.exists(file_path):
        print(f"[CACHE] Usando dados salvos: {file_path}")
        return pd.read_csv(file_path, index_col=0, parse_dates=True)

    try:
        data = yf.download(ticker, period=period, interval=interval)
        if data.empty:
            raise ValueError("Dados retornados estão vazios.")
        data.to_csv(file_path)
        print(f"[DOWNLOAD] Dados salvos em: {file_path}")
        return data
    except Exception as e:
        print(f"[ERRO] Falha ao baixar dados: {e}")
        return pd.DataFrame()
