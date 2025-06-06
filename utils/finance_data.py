import yfinance as yf
import os
import pandas as pd

def download_data(ticker, period="2y", interval="1d"):
    os.makedirs("data/", exist_ok=True)
    file_path = f"data/{ticker}_{period}_{interval}.csv"

    # Se já existe, usa cache
    if os.path.exists(file_path):
        print(f"[CACHE] Usando dados salvos: {file_path}")
        df = pd.read_csv(file_path, index_col=0, parse_dates=True)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.droplevel(1)
        return df

    try:
        data = yf.download(ticker, period=period, interval=interval)
        if data.empty:
            raise ValueError("Dados retornados estão vazios.")
        data.to_csv(file_path)
        print(f"[DOWNLOAD] Dados salvos em: {file_path}")
        data.columns = data.columns.droplevel(1) if isinstance(data.columns, pd.MultiIndex) else data.columns
        return data
    except Exception as e:
        print(f"[ERRO] Falha ao baixar dados: {e}")
        return pd.DataFrame()