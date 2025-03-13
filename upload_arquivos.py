from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QMessageBox
from PyQt6.QtGui import QFont, QColor, QPalette, QIcon
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from tratar_dados import tratar_dados
from gerar_insights import analisar_planilha
from insight_screen import InsightsScreen
import os

class ProcessThread(QThread):
    """ Thread para processar os insights sem travar a UI """
    finished = pyqtSignal(str)  # Sinal emitido ao finalizar o processamento
    error = pyqtSignal(str)  # Sinal para capturar erros

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def run(self):
        try:
            tratar_dados(self.file_path)
            output_file = "dados/dados_producao_limpos.csv"
            insights_html = analisar_planilha(output_file)
            self.finished.emit(insights_html)  # Envia os insights para a UI
        except Exception as e:
            self.error.emit(str(e))  # Envia erro para a UI

class UploadScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.file_path = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("VisioData - Upload de Arquivo")
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(400, 300)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#d5d5d5"))
        self.setPalette(palette)

        layout = QVBoxLayout()

        title_label = QLabel("VisioData")
        title_label.setFont(QFont("Arial", 30, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #2F4CEC;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle_label = QLabel("Transformando dados em visão estratégica")
        subtitle_label.setFont(QFont("Arial", 20))
        subtitle_label.setStyleSheet("color: black;")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        help_label = QLabel("Como podemos ajudar:")
        help_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        help_label.setStyleSheet("color: black;")
        help_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        description_label = QLabel("Oferecemos tratamento de dados da sua planilha e insights das informações, facilitando o planejamento estratégico da sua empresa")
        description_label.setFont(QFont("Arial", 16))
        description_label.setStyleSheet("color: black;")
        description_label.setWordWrap(True)
        description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.upload_button = QPushButton(" Faça o upload do seu arquivo")
        self.upload_button.setFont(QFont("Arial", 10))
        self.upload_button.setStyleSheet("color: black; background-color: white; border-radius: 5px; padding: 10px;")
        self.upload_button.setIcon(QIcon.fromTheme("document-open"))
        self.upload_button.clicked.connect(self.upload_file)

        self.loading_label = QLabel("") # Inicia a mensagem de carregamento vazia
        self.loading_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.loading_label.setStyleSheet("color: #2F4CEC;")
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.send_file_button = QPushButton("Enviar")
        self.send_file_button.setFont(QFont("Arial", 14))
        self.send_file_button.setStyleSheet("color: black;background-color: white; border-radius: 5px; padding: 5px;")
        self.send_file_button.clicked.connect(self.process_file)

        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)
        layout.addWidget(help_label)
        layout.addWidget(description_label)
        layout.addWidget(self.upload_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.loading_label)
        layout.addWidget(self.send_file_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def upload_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Selecione um arquivo", "", "Planilhas (*.csv *.xls *.xlsx)")
        if file_path:
            self.file_path = file_path
            file_name = os.path.basename(file_path)
            self.upload_button.setText(f"{file_name}")

    def process_file(self):
        if self.file_path:
            self.loading_label.setText("Carregando Insights... Aguarde.")
            self.send_file_button.setEnabled(False)  # Desativa o botão enquanto processa

            # Criar e iniciar a Thread
            self.thread = ProcessThread(self.file_path)
            self.thread.finished.connect(self.on_processing_finished)
            self.thread.error.connect(self.on_processing_error)
            self.thread.start()

        else:
            QMessageBox.warning(self, "Nenhum Arquivo", "Por favor, selecione um arquivo antes de enviar.")

    def on_processing_finished(self, insights_html):
        """ Callback quando o processamento termina """
        self.loading_label.setText("")
        self.send_file_button.setEnabled(True)  # Reativa o botão

        # Captura o estado e tamanho da janela antes de abrir insights
        is_maximized = self.isMaximized()
        window_geometry = self.geometry()

        # Criar a tela de insights e ajustar tamanho
        self.insights_window = InsightsScreen(insights_html, parent=self)
        self.insights_window.setGeometry(window_geometry)  # Aplica o mesmo tamanho da tela anterior

        # Garante que a janela esteja visível e não minimizada
        # self.insights_window.setWindowState(self.insights_window.windowState() & ~Qt.WindowState.WindowMinimized)
        # self.insights_window.activateWindow()
        # self.insights_window.raise_()  
        self.insights_window.show()

        self.close()  # Fecha a tela de upload


    def on_processing_error(self, error_message):
        """ Callback para exibir erros """
        self.loading_label.setText("")
        self.send_file_button.setEnabled(True)  # Reativa o botão
        QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao processar o arquivo:\n{error_message}")
