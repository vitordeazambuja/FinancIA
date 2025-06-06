import yfinance as yf
import os
import pandas as pd
import numpy as np

def download_data(ticker, period="6mo", interval="1d"):
    os.makedirs("data/", exist_ok=True)
    file_path = f"data/{ticker}_{period}_{interval}.csv"

    if os.path.exists(file_path):
        print(f"[CACHE] Usando dados salvos: {file_path}")
        df = pd.read_csv(file_path, index_col=0)
        df.index = pd.to_datetime(df.index, format='%Y-%m-%d', errors='coerce')
        df = df.dropna(subset=['Close'])  # remove linhas sem valor de fechamento
        df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
        df = df.dropna(subset=['Close'])  # remove linhas com valor inválido
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.droplevel(1)
        return df

    try:
        data = yf.download(ticker, period=period, interval=interval)
        if data.empty:
            raise ValueError("Dados retornados estão vazios.")
        data.to_csv(file_path)
        print(f"[DOWNLOAD] Dados salvos em: {file_path}")
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.droplevel(1)
        return data
    except Exception as e:
        print(f"[ERRO] Falha ao baixar dados: {e}")
        return pd.DataFrame()

  