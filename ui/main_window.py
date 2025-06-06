from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QLineEdit)
from PyQt5.QtCore import Qt
from utils.predictor import prever_proximos_7_dias
from datetime import datetime

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FinancIA")
        self.setMinimumSize(800,600)
        self.init_ui()
        self.predict_btn.clicked.connect(self.predict_stock)
    
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        control_layout = QHBoxLayout()
        main_layout.addLayout(control_layout)

        self.stock_combo = QComboBox()
        self.stock_combo.addItems(["PETR4.SA", "VALE3.SA", "ITUB4.SA"])
        control_layout.addWidget(QLabel("Selecione a ação:"))
        control_layout.addWidget(self.stock_combo)

        self.custom_input = QLineEdit()
        self.custom_input.setPlaceholderText("ou digite um ticker ex: ABEV3.SA")
        control_layout.addWidget(self.custom_input)

        self.predict_btn = QPushButton("Prever")
        control_layout.addWidget(self.predict_btn)

        self.result_label = QLabel("Selecione uma ação e clique em 'Prever'.")
        self.result_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.result_label)
        
    def predict_stock(self):
        ticker = self.custom_input.text().strip() or self.stock_combo.currentText()
        self.result_label.setText(f"Processando {ticker}...")

        try:
            previsoes = prever_proximos_7_dias(ticker)

        # Limpa a caixa de texto depois de clicar
            self.custom_input.clear()

        # Busca o preço atual (último fechamento)
            from utils.finance_data import download_data
            df = download_data(ticker)
            preco_atual = df["Close"].values[-1]

        # Monta o texto de resultado
            resultado_texto = f"Preço Atual: R$ {preco_atual:.2f}\n\n"
            for data, valor in previsoes:
                data_formatada = datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y")
                resultado_texto += f"{data_formatada} : R$ {valor:.2f}\n"

            self.result_label.setText(resultado_texto)

        except Exception as e:
            self.result_label.setText(f"Erro: {str(e)}")

