import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def prepare_data(df, column='Close', window_size=60):
    # 1. Extrair a coluna de interesse como array numpy
    data = df[[column]].values

    # 2. Normalizar com MinMaxScaler
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)

    # 3. Criar as janelas deslizantes
    X = []
    y = []
    for i in range(window_size, len(scaled_data)):
        X.append(scaled_data[i - window_size:i, 0])
        y.append(scaled_data[i, 0])

    # 4. Converter para numpy arrays e ajustar shape
    X = np.array(X)
    y = np.array(y)

    # Adiciona o eixo de "características" (1 variável por tempo)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))

    return X, y, scaler