from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QPushButton, QLineEdit, QSizePolicy
)
from PyQt5.QtCore import Qt
import pyqtgraph as pg
from utils.predictor import prever_proximos_7_dias
from datetime import datetime
import numpy as np
from utils.finance_data import download_data
from sklearn.metrics import mean_squared_error, mean_absolute_error
import math

TICKER_NOMES = {
    "PETR4.SA": "Petrobras",
    "VALE3.SA": "Vale",
    "ITUB4.SA": "Itaú Unibanco",
    "B3SA3.SA": "B3",
    "ABEV3.SA": "Ambev",
    "BBAS3.SA": "Banco do Brasil",
    "BBDC4.SA": "Bradesco",
    "WEGE3.SA": "Weg",
    "RENT3.SA": "Localiza",
    "JBSS3.SA": "JBS",
    "BRFS3.SA": "BRF",
    "MGLU3.SA": "Magazine Luiza",
    "LREN3.SA": "Lojas Renner",
    "GGBR4.SA": "Gerdau",
    "CSNA3.SA": "CSN",
    "ELET3.SA": "Eletrobras",
    "SUZB3.SA": "Suzano",
    "EGIE3.SA": "Engie Brasil",
    "HAPV3.SA": "Hapvida",
    "RADL3.SA": "Raia Drogasil"
}

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FinancIA")
        self.setMinimumSize(900, 650)
        self.init_ui()
        self.predict_btn.clicked.connect(self.predict_stock)

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Layout de controle superior
        control_layout = QHBoxLayout()
        main_layout.addLayout(control_layout)

        self.stock_combo = QComboBox()
        self.stock_combo.addItems(list(TICKER_NOMES.keys()))
        control_layout.addWidget(QLabel("Selecione a ação:"))
        control_layout.addWidget(self.stock_combo)

        self.custom_input = QLineEdit()
        self.custom_input.setPlaceholderText("ou digite um ticker ex: ABEV3.SA")
        control_layout.addWidget(self.custom_input)

        self.period_combo = QComboBox()
        self.period_combo.addItems(["5d","7d", "1mo", "3mo", "1y", "2y", "max"])
        control_layout.addWidget(QLabel("Período histórico:"))
        control_layout.addWidget(self.period_combo)

        self.predict_btn = QPushButton("Prever")
        control_layout.addWidget(self.predict_btn)

        # Nome da empresa
        self.empresa_label = QLabel("")
        self.empresa_label.setAlignment(Qt.AlignCenter)
        self.empresa_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 8px;")
        main_layout.addWidget(self.empresa_label)

        # Resultado de previsão
        self.result_label = QLabel("Selecione uma ação e clique em 'Prever'.")
        self.result_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.result_label)

        # Gráfico
        self.graph_widget = pg.PlotWidget()
        main_layout.addWidget(self.graph_widget)
        self.graph_widget.setBackground('#222222')
        self.graph_widget.showGrid(x=True, y=True)
        self.graph_widget.setLabel('left', 'Preço (R$)', color='#CCCCCC')
        self.graph_widget.setLabel('bottom', 'Data ', color='#CCCCCC')
        self.graph_widget.getAxis('bottom').setTextPen('#CCCCCC')
        self.graph_widget.getAxis('left').setTextPen('#CCCCCC')

        # Métricas
        self.metricas_label = QLabel("")
        self.metricas_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.metricas_label)

    def predict_stock(self):
        ticker = self.custom_input.text().strip().upper() or self.stock_combo.currentText()
        nome_empresa = TICKER_NOMES.get(ticker, ticker)
        self.result_label.setText(f"Processando {ticker}...")
        self.empresa_label.setText("")  # limpar
        self.metricas_label.setText("")  # limpar

        try:
            periodo = self.period_combo.currentText()
            df = download_data(ticker, period=periodo, interval="1d")

            if df.empty:
                raise ValueError("Dados históricos não encontrados.")

            previsoes = prever_proximos_7_dias(ticker)

            preco_atual = df["Close"].values[-1]
            resultado_texto = f"Preço Atual: R$ {preco_atual:.2f}\n\n"
            for data, valor in previsoes:
                data_fmt = datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y")
                resultado_texto += f"{data_fmt} : R$ {valor:.2f}\n"
            self.result_label.setText(resultado_texto)
            self.empresa_label.setText(nome_empresa)

            # GRÁFICO
            self.graph_widget.clear()
            self.graph_widget.addLegend()  # adiciona a legenda

            # Histórico
            datas_hist = df.index.to_pydatetime()
            precos_hist = df["Close"].values
            dias_hist = np.array([dt.timestamp() for dt in datas_hist])

            # Previsão
            datas_prev, precos_prev = zip(*previsoes)
            datas_prev_dt = [datetime.strptime(d, "%Y-%m-%d") for d in datas_prev]
            dias_prev = np.array([dt.timestamp() for dt in datas_prev_dt])

            self.graph_widget.plot(
                x=dias_hist, y=precos_hist,
                pen=pg.mkPen(color='cyan', width=2),
                name="Histórico"
            )

            self.graph_widget.plot(
                x=dias_prev, y=precos_prev,
                pen=pg.mkPen(color='magenta', width=2, style=Qt.DashLine),
                symbol='o', symbolBrush='magenta',
                name="Previsão"
            )

            # Ticks do eixo x
            eixo_x = self.graph_widget.getAxis('bottom')
            eixo_x.setTicks([[(ts, datetime.fromtimestamp(ts).strftime('%d/%m')) for ts in
                              np.linspace(dias_hist[0], dias_prev[-1], 10)]])

            self.graph_widget.enableAutoRange('xy', True)

            # MÉTRICAS
            y_true = precos_hist[-len(precos_prev):]
            y_pred = precos_prev[:len(y_true)]

            rmse = math.sqrt(mean_squared_error(y_true, y_pred))
            mae = mean_absolute_error(y_true, y_pred)
            self.metricas_label.setText(f"📈 RMSE: {rmse:.2f} | MAE: {mae:.2f}")

            self.custom_input.clear()

        except Exception as e:
            self.result_label.setText(f"Erro: {str(e)}")
            self.empresa_label.setText("")
            self.metricas_label.setText("")
