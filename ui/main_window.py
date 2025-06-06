from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton)
from PyQt5.QtCore import Qt
from utils.model_utils import prever_acao

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

        # Controles superiores
        control_layout = QHBoxLayout()
        main_layout.addLayout(control_layout)

        self.stock_combo = QComboBox()
        self.stock_combo.addItems(["PETR4.SA", "VALE3.SA", "ITUB4.SA"])  # Exemplo
        control_layout.addWidget(QLabel("Selecione a ação:"))
        control_layout.addWidget(self.stock_combo)

        self.predict_btn = QPushButton("Prever")
        control_layout.addWidget(self.predict_btn)

        self.chart_placeholder = QLabel("[Gráfico Placeholder]")
        self.chart_placeholder.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.chart_placeholder)

        self.info_label = QLabel("Selecione uma ação e clique em 'Prever'.")
        self.info_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.info_label)
        
    def predict_stock(self):
        selected_stock = self.stock_combo.currentText()
        self.info_label.setText(f"Processando {selected_stock}...")
        
        try:
            resultado = prever_acao(selected_stock)
            self.info_label.setText(f"Valor previsto para amanhã: R$ {resultado:.2f}")
        except Exception as e:
            self.info_label.setText(f"Erro: {str(e)}")