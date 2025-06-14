import os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import GridSearchCV
import joblib

# ---------- 1. Mock de dados ----------
def gerar_dados_exemplo():
    """Em teoria é pra gerar dado simulado aleatório de preço"""
    np.random.seed(42)
    preco_falso = np.cumsum(np.random.randn(200)) + 100
    df = pd.DataFrame({'Close': preco_falso})
    return df

# ---------- 2. Mock da prepare_data ----------
def mock_prepare_data(df, column='Close', window_size=60):
    """
    Simula o comportamento da função prepare_data:
    - Normaliza os dados
    - Cria janelas deslizantes
    - Retorna X e y prontos para treino
    """
    series = df[column].values.reshape(-1, 1)

    # Normalização com MinMaxScaler
    scaler = MinMaxScaler()
    series_scaled = scaler.fit_transform(series).flatten()

    X, y = [], []
    for i in range(len(series_scaled) - window_size):
        X.append(series_scaled[i:i+window_size])
        y.append(series_scaled[i+window_size])

    return np.array(X).reshape(len(X), -1), np.array(y), scaler


# ---------- 3. Implementação de train_model() ----------
def train_model(X, y, n_estimators=50, random_state=42):
    """
    Treina o modelo RandomForestRegressor
    """
    model = RandomForestRegressor(n_estimators=n_estimators, random_state=random_state)
    model.fit(X, y)
    return model

# ---------- 4. Salvamento do modelo ----------
def save_model(model, path='models/modelo.joblib'):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(model, path)

def save_scaler(scaler, path='models/scaler.joblib'):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(scaler, path)

# ---------- 5. Execução de teste ----------
if __name__ == "__main__":
    df = gerar_dados_exemplo()
    X, y, scaler = mock_prepare_data(df, window_size=60)

    print(f"Dados de treino prontos -> X shape: {X.shape}, y shape: {y.shape}")

    model = train_model(X, y)
    save_model(model)
    save_scaler(scaler)

    print("Modelo e scaler treinados e salvos com sucesso.")
    
# ---------- 6. Ajuste de Hiperparâmetros ----------
def ajustar_hiperparametros(X, y):
    """
    Executa busca em grade (GridSearchCV) para encontrar os melhores hiperparâmetros
    do RandomForestRegressor.
    """
    param_grid = {
        'n_estimators': [50, 100, 150],
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5],
        'min_samples_leaf': [1, 2]
    }

    base_model = RandomForestRegressor(random_state=42)
    grid_search = GridSearchCV(
        base_model,
        param_grid,
        cv=3,
        scoring='neg_mean_squared_error',
        verbose=1,
        n_jobs=-1
    )

    print("[INFO] Iniciando ajuste de hiperparâmetros com GridSearchCV...")
    grid_search.fit(X, y)
    print(f"[RESULTADO] Melhor combinação: {grid_search.best_params_}")

    return grid_search.best_estimator_