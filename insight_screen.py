from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, 
    QMessageBox, QHBoxLayout, QFileDialog, QSizePolicy
)


class InsightsScreen(QWidget):
    """ Tela que exibe os insights gerados após o processamento dos dados """
    def __init__(self, insights_html, parent=None):
        super().__init__()
        self.parent_window = parent  # Guarda a referência da tela de upload
        self.insights_html = insights_html  # Armazena os insights como HTML
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Insights Gerados")
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(400, 300)

        layout = QVBoxLayout()

        title_label = QLabel("📊 Insights Gerados")
        title_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        title_label.setMaximumHeight(50) 

        # Widget de renderização HTML
        self.web_view = QWebEngineView()
        self.web_view.setHtml(self.insights_html)  # Renderiza o HTML dentro do widget

        # Layout de botões (Fechar e Baixar PDF)
        button_layout = QHBoxLayout()

        # Botão de fechar
        close_button = QPushButton("Fechar")
        close_button.setFont(QFont("Arial", 12))
        close_button.setStyleSheet("background-color: #2F4CEC; color: white; padding: 8px; border-radius: 5px;")
        close_button.clicked.connect(self.redirect_upload_screen)

        # Botão de baixar PDF
        save_pdf_button = QPushButton("Baixar Relatório")
        save_pdf_button.setFont(QFont("Arial", 12))
        save_pdf_button.setStyleSheet("background-color: #28a745; color: white; padding: 8px; border-radius: 5px;")
        save_pdf_button.clicked.connect(self.save_pdf)

        button_layout.addWidget(close_button)
        button_layout.addWidget(save_pdf_button)

        # Adiciona os widgets ao layout
        layout.addWidget(title_label)
        layout.addWidget(self.web_view)  # Adiciona a visualização HTML
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def redirect_upload_screen(self):
        """ Retorna para a tela de upload mantendo o tamanho correto """
        from upload_arquivos import UploadScreen

        # Captura o estado da janela atual
        window_is_maximized = self.isMaximized()
        window_geometry = self.geometry()

        # Criar a tela de upload e ajustar o tamanho
        self.second_window = UploadScreen()

        if window_is_maximized:
            self.second_window.showMaximized()
        else:
            self.second_window.setGeometry(window_geometry)  # Aplica o mesmo tamanho e posição

        self.second_window.show()
        self.close()


    def save_pdf(self):
        """ Gera um PDF a partir do HTML renderizado """
        file_path, _ = QFileDialog.getSaveFileName(self, "Salvar Relatório", "", "PDF Files (*.pdf)")
        if file_path:
            self.web_view.page().printToPdf(file_path)
            QMessageBox.information(self, "Sucesso", "Relatório salvo com sucesso!")


    def showEvent(self, event):
        """ Fecha a tela de upload ao abrir a tela de insights """
        if self.parent_window:
            self.parent_window.close()
