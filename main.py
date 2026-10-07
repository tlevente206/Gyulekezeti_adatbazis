import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
                             QWidget, QPushButton, QFrame, QHBoxLayout)
from PyQt6.QtCore import Qt

class GlassWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Hagyományos Windows fejléc (keret) eltüntetése és átlátszó alap
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        layout = QVBoxLayout(self.central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Üveg panel
        self.glass_frame = QFrame()
        self.glass_frame.setObjectName("glassFrame")
        self.glass_frame.setStyleSheet("""
            #glassFrame {
                background-color: rgba(25, 25, 35, 240);
                border: 1px solid rgba(255, 255, 255, 20);
            }
        """)
        
        frame_layout = QVBoxLayout(self.glass_frame)
        frame_layout.setContentsMargins(20, 10, 20, 20)

        # --- Saját felső sáv (Title bar) ---
        top_bar = QHBoxLayout()
        top_bar.setSpacing(8)
        
        title_label = QLabel("Gyülekezeti Adatbázis")
        title_label.setStyleSheet("color: rgba(255, 255, 255, 200); font-size: 16px; font-weight: bold; font-family: 'Segoe UI';")
        
        # Minimalizálás (tálcára rakás) gomb
        self.btn_minimize = QPushButton("—")
        self.btn_minimize.setFixedSize(40, 35)
        self.btn_minimize.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_minimize.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #a6adc8;
                font-weight: bold;
                font-size: 14px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 25);
                color: white;
            }
        """)
        self.btn_minimize.clicked.connect(self.showMinimized)

        # Bezárás gomb
        self.btn_close = QPushButton("✕")
        self.btn_close.setFixedSize(40, 35)
        self.btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_close.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #a6adc8;
                font-weight: bold;
                font-size: 16px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: rgba(220, 50, 50, 200);
                color: white;
            }
        """)
        self.btn_close.clicked.connect(self.close)
        
        top_bar.addWidget(title_label)
        top_bar.addStretch()
        top_bar.addWidget(self.btn_minimize)
        top_bar.addWidget(self.btn_close)
        
        frame_layout.addLayout(top_bar)

        # --- Tartalmi rész ---
        content_layout = QVBoxLayout()
        content_layout.addStretch()
        
        welcome = QLabel("Kezdőképernyő - Készen áll a fejlesztésre")
        welcome.setStyleSheet("color: white; font-size: 28px; font-family: 'Segoe UI';")
        welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(welcome)
        
        content_layout.addStretch()
        frame_layout.addLayout(content_layout)

        layout.addWidget(self.glass_frame)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GlassWindow()
    window.showMaximized()
    sys.exit(app.exec())