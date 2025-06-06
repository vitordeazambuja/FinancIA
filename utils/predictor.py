import numpy as np
from utils.finance_data import download_data
from utils.preprocessing import prepare_data
from utils.train_model import train_model
from datetime import datetime, timedelta

def prever_proximos_7_dias(ticker, window_size=90):
    df = download_data(ticker, period="6mo", interval="1d")
    if df.empty or 'Close' not in df.columns:
        raise ValueError("Dados inválidos para previsão.")

    # Prepara os dados
    X, y, scaler = prepare_data(df, window_size=window_size)

    if len(X) == 0:
        raise ValueError("Dados insuficientes para previsão.")

    # Treina modelo na hora
    X_2D = X.reshape(X.shape[0], X.shape[1])
    model = train_model(X_2D, y)

    # Previsão a partir da última sequência
    input_seq = X[-1].flatten()  # última janela deslizante
    predictions_scaled = []

    for _ in range(7):
        pred_scaled = model.predict(input_seq.reshape(1, -1))[0]
        predictions_scaled.append(pred_scaled)
        input_seq = np.append(input_seq[1:], pred_scaled)

    predictions_scaled_np = np.array(predictions_scaled).reshape(-1, 1)
    predictions = scaler.inverse_transform(predictions_scaled_np).flatten()

    # Datas futuras
    ult_data = df.index[-1]
    datas_prev = [(ult_data + timedelta(days=i+1)).strftime("%Y-%m-%d") for i in range(7)]

    return list(zip(datas_prev, predictions))
