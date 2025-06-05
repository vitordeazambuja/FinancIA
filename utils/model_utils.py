import os
import joblib
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