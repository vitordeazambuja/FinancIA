from utils.finance_data import download_data
from utils.preprocessing import prepare_data
from utils.train_model import train_model, save_model, save_scaler
from utils.train_model import ajustar_hiperparametros
import joblib

ticker = "PETR4.SA"
df = download_data(ticker, period="2y", interval="1d")
print(df.head())
print(df.columns)

if df.empty:
    print("Erro: sem dados para treinamento.")
    exit()

X, y, scaler = prepare_data(df, window_size=60)
print(f"Dados preparados: X.shape={X.shape}, y.shape={y.shape}")

model = ajustar_hiperparametros(X.reshape(X.shape[0], X.shape[1]), y)
print("Modelo treinado.")

save_model(model, path='models/modelo.joblib')
save_scaler(scaler, path='models/scaler.joblib')
print("Modelo e scaler salvos.")

model_loaded = joblib.load('models/modelo.joblib')
scaler_loaded = joblib.load('models/scaler.joblib')

print("Modelo e scaler carregados com sucesso.")