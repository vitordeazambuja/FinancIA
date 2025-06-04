import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def prepare_data(df, column='Close', window_size=60):
    """
    Pré-processa os dados de preços para treinamento de modelos de séries temporais.

    Parâmetros:
    - df: DataFrame contendo os dados históricos (deve conter a coluna 'Close' ou equivalente)
    - column: nome da coluna com os preços a serem usados
    - window_size: tamanho da janela deslizante (quantidade de dias anteriores usados como entrada)

    Retorno:
    - X: entradas normalizadas (shape: [n amostras, window_size, 1])
    - y: valores alvo (preço do próximo dia)
    - scaler: objeto MinMaxScaler usado (para inverter a normalização depois)
    """

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
        y.append(scaled_data[i, 0])  # valor a ser previsto (o próximo após a janela)

    # 4. Converter para numpy arrays e ajustar shape
    X = np.array(X)
    y = np.array(y)

    # Adiciona o eixo de "características" (1 variável por tempo)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))

    return X, y, scaler