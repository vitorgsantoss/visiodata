import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt6.QtGui import QFont, QColor, QPalette
from PyQt6.QtCore import Qt
from upload_arquivos import UploadScreen  # Importando a segunda tela

class Home(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("VisioData")
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(400, 300)
        self.setWindowFlag(Qt.WindowType.Window)
        
        # Background color
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#D5D5D5"))
        self.setPalette(palette)
        
        layout = QVBoxLayout()
        
        # Title Label
        title_label = QLabel("VisioData")
        title_label.setFont(QFont("Arial", 30, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #2F4CEC;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Subtitle Label
        subtitle_label = QLabel("Transformando dados em visão estratégica")
        subtitle_label.setFont(QFont("Arial", 18))
        subtitle_label.setStyleSheet("color: black;")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Button
        start_button = QPushButton("Iniciar Sistema")
        start_button.setFont(QFont("Arial", 14))
        start_button.setStyleSheet("color: black;background-color: white; border-radius: 5px; padding: 5px;")
        start_button.clicked.connect(self.start_system)
        
        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)
        layout.addWidget(start_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.setLayout(layout)
    
    
    def start_system(self):
    # Captura o estado da janela
        window_is_maximized = self.isMaximized()
        window_geometry = self.geometry()  # Obtém a geometria da janela

        # Cria a segunda janela e ajusta o tamanho
        self.second_window = UploadScreen()

        if window_is_maximized:
            self.second_window.showMaximized()
        else:
            self.second_window.setGeometry(window_geometry)  # Aplica o mesmo tamanho e posição

        self.second_window.show()
        self.close()

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Home()
    window.show()
    sys.exit(app.exec())
