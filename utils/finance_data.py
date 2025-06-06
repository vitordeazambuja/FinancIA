import yfinance as yf
import os
import pandas as pd
import numpy as np
from utils.model_utils import load_model_and_scaler

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

def predict_next_days(ticker, days=7, window_size=60):
    """
    Gera previsão de preços para os próximos dias.
    """
    # 1. Baixa os dados mais recentes
    df = download_data(ticker, period="2y", interval="1d")
    if df.empty or 'Close' not in df.columns:
        raise ValueError("Dados inválidos para previsão.")

    # 2. Carrega modelo e scaler
    model, scaler = load_model_and_scaler()

    # 3. Pega os últimos 'window_size' dias para iniciar a previsão
    close_data = df['Close'].values[-window_size:]
    input_seq = close_data.reshape(-1, 1)
    input_scaled = scaler.transform(input_seq).flatten()

    predictions = []
    for _ in range(days):
        # Cria entrada com shape (1, 60)
        input_array = np.array(input_scaled[-window_size:]).reshape(1, -1)
        pred_scaled = model.predict(input_array)[0]
        predictions.append(pred_scaled)
        input_scaled = np.append(input_scaled, pred_scaled)  # adiciona a previsão

    # Inverte a normalização das previsões
    predictions_np = np.array(predictions).reshape(-1, 1)
    predictions_unscaled = scaler.inverse_transform(predictions_np).flatten()

    return predictions_unscaled
  