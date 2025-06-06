import os
import joblib
import numpy as np
from tensorflow.keras.models import load_model

def load_model_and_scaler(model_path='models/modelo.joblib',
                          scaler_path='models/scaler.joblib'):

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Modelo não encontrado em {model_path}")
    
    if not os.path.exists(scaler_path):
        raise FileNotFoundError(f"Scaler não encontrado em {scaler_path}")

    if model_path.endswith('.h5'):
        model = keras_load_model(model_path)
    elif model_path.endswith('.joblib'):
        model = joblib.load(model_path)
    else:
        raise ValueError("Formato de modelo não suportado")

    scaler = joblib.load(scaler_path)

    return model, scaler

def prever_acao(ticker):
    from utils.finance_data import download_data
    from utils.preprocessing import prepare_data
    from utils.model_utils import load_model_and_scaler

    # Baixar e preparar os dados
    df = download_data(ticker)
    if df.empty:
        raise ValueError("Erro ao baixar os dados.")

    X, _, scaler = prepare_data(df, window_size=60)

    model, _ = load_model_and_scaler()

    # Prever o próximo valor com os últimos dados
    if len(X) == 0:
        raise ValueError("Dados insuficientes para previsão.")
    
    entrada = X[-1].reshape(1, -1)
    y_pred = model.predict(entrada)

    # Inverter a escala
    y_pred_original = scaler.inverse_transform([[y_pred[0]]])[0][0]
    return y_pred_original