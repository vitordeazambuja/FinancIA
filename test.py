from utils.finance_data import download_data

df = download_data("PETR4.SA")
print(df.head())