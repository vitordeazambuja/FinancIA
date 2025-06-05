import os
import joblib
from tensorflow.keras.models import load_model

def load_model_and_scaler(model_path='trained_models/modelo_lstm.h5',
                          scaler_path='trained_models/scaler.pkl'):
    """
    Carrega o modelo treinado e o objeto MinMaxScaler salvo.

    Parâmetros:
    - model_path: caminho para o arquivo do modelo (.h5)
    - scaler_path: caminho para o arquivo do scaler (.pkl)

    Retorno:
    - model: modelo carregado
    - scaler: scaler carregado
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Modelo não encontrado em {model_path}")
    
    if not os.path.exists(scaler_path):
        raise FileNotFoundError(f"Scaler não encontrado em {scaler_path}")

    model = load_model(model_path)
    scaler = joblib.load(scaler_path)

    return model, scaler