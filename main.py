import sys
from datetime import date
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
                             QWidget, QPushButton, QFrame, QHBoxLayout, 
                             QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt6.QtCore import Qt

import database

class GlassWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        database.init_db()
        
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        layout = QVBoxLayout(self.central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
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
        frame_layout.setSpacing(20)

        font_family = "'Century Gothic', 'Bahnschrift', 'Segoe UI', sans-serif"

        # --- Felső sáv ---
        top_bar = QHBoxLayout()
        top_bar.setSpacing(8)
        
        title_label = QLabel("Gyülekezeti Adatbázis")
        title_label.setStyleSheet(f"color: rgba(255, 255, 255, 200); font-size: 17px; font-weight: bold; font-family: {font_family};")
        
        self.btn_minimize = QPushButton("—")
        self.btn_minimize.setFixedSize(40, 35)
        self.btn_minimize.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_minimize.setStyleSheet(f"""
            QPushButton {{ background-color: transparent; color: #a6adc8; font-weight: bold; border: none; border-radius: 4px; font-family: {font_family}; }}
            QPushButton:hover {{ background-color: rgba(255, 255, 255, 25); color: white; }}
        """)
        self.btn_minimize.clicked.connect(self.showMinimized)

        self.btn_close = QPushButton("✕")
        self.btn_close.setFixedSize(40, 35)
        self.btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_close.setStyleSheet(f"""
            QPushButton {{ background-color: transparent; color: #a6adc8; font-weight: bold; border: none; border-radius: 4px; font-family: {font_family}; }}
            QPushButton:hover {{ background-color: rgba(220, 50, 50, 200); color: white; }}
        """)
        self.btn_close.clicked.connect(self.close)
        
        top_bar.addWidget(title_label)
        top_bar.addStretch()
        top_bar.addWidget(self.btn_minimize)
        top_bar.addWidget(self.btn_close)
        frame_layout.addLayout(top_bar)

        # --- Funkciógombok ---
        content_layout = QVBoxLayout()
        content_layout.setSpacing(15)
        
        action_bar = QHBoxLayout()
        action_bar.setSpacing(10)
        
        btn_style = f"""
            QPushButton {{ background-color: rgba(255, 255, 255, 10); color: white; border: 1px solid rgba(255, 255, 255, 30); border-radius: 6px; padding: 8px 16px; font-size: 14px; font-family: {font_family}; }}
            QPushButton:hover {{ background-color: rgba(255, 255, 255, 25); border: 1px solid rgba(255, 255, 255, 60); }}
            QPushButton:pressed {{ background-color: rgba(255, 255, 255, 5); }}
        """
        
        self.btn_add = QPushButton("Hozzáadás")
        self.btn_add.setStyleSheet(btn_style)
        self.btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.btn_edit = QPushButton("Módosítás / Befizetések")
        self.btn_edit.setStyleSheet(btn_style)
        self.btn_edit.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.btn_delete = QPushButton("Törlés")
        self.btn_delete.setStyleSheet(btn_style)
        self.btn_delete.setCursor(Qt.CursorShape.PointingHandCursor)
        
        action_bar.addWidget(self.btn_add)
        action_bar.addWidget(self.btn_edit)
        action_bar.addWidget(self.btn_delete)
        action_bar.addStretch()
        
        content_layout.addLayout(action_bar)
        
        # --- Táblázat ---
        self.table = QTableWidget()
        oszlopok = ["ID", "Vezetéknév", "Keresztnév", "Születési idő", "Életkor", "Szül. hely", 
                    "Település", "Utca", "Házszám", "Neme", "Mióta tag", "Presbitere", 
                    "E. havi járulék", "Megjegyzés"]
        self.table.setColumnCount(len(oszlopok))
        self.table.setHorizontalHeaderLabels(oszlopok)
        
        self.table.setStyleSheet(f"""
            QTableWidget {{ background-color: rgba(20, 20, 30, 150); color: #e0e0e0; gridline-color: rgba(255, 255, 255, 15); border: 1px solid rgba(255, 255, 255, 20); border-radius: 8px; font-size: 13px; font-family: {font_family}; }}
            QHeaderView::section {{ background-color: rgba(40, 40, 55, 200); color: white; padding: 6px; border: none; border-right: 1px solid rgba(255, 255, 255, 15); border-bottom: 1px solid rgba(255, 255, 255, 15); font-weight: bold; font-size: 13px; font-family: {font_family}; }}
            QTableWidget::item:selected {{ background-color: rgba(255, 255, 255, 30); color: white; }}
            QTableWidget::item {{ padding: 5px; }}
        """)
        
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setFrameShape(QFrame.Shape.NoFrame)
        self.table.setShowGrid(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        self.table.setColumnHidden(0, True)

        self.load_dummy_data()
        
        content_layout.addWidget(self.table)
        frame_layout.addLayout(content_layout)
        layout.addWidget(self.glass_frame)

    def load_dummy_data(self):
        # Teszt adatok kibővítve a lakcímmel (Település, Utca, Házszám)
        teszt_tagok = [
            ("1", "Kovács", "János", "1985-05-12", "Debrecen", "Debrecen", "Kossuth utca", "12/B", "Férfi", "2010-01-15", "Tóth Péter", "✔️ Igen", "Aktív tag"),
            ("2", "Nagy", "Éva", "1992-11-23", "Budapest", "Hajdúszoboszló", "Fő utca", "5", "Nő", "2021-08-10", "Szabó Lajos", "❌ Nem", "Késik a fizetéssel")
        ]
        
        self.table.setRowCount(len(teszt_tagok))
        for row_idx, tag in enumerate(teszt_tagok):
            self.table.setItem(row_idx, 0, QTableWidgetItem(tag[0]))
            self.table.setItem(row_idx, 1, QTableWidgetItem(tag[1]))
            self.table.setItem(row_idx, 2, QTableWidgetItem(tag[2]))
            self.table.setItem(row_idx, 3, QTableWidgetItem(tag[3]))
            
            eletkor = database.szamol_eletkor(tag[3])
            self.table.setItem(row_idx, 4, QTableWidgetItem(eletkor))
            
            self.table.setItem(row_idx, 5, QTableWidgetItem(tag[4]))
            self.table.setItem(row_idx, 6, QTableWidgetItem(tag[5]))
            self.table.setItem(row_idx, 7, QTableWidgetItem(tag[6]))
            self.table.setItem(row_idx, 8, QTableWidgetItem(tag[7]))
            self.table.setItem(row_idx, 9, QTableWidgetItem(tag[8]))
            self.table.setItem(row_idx, 10, QTableWidgetItem(tag[9]))
            self.table.setItem(row_idx, 11, QTableWidgetItem(tag[10]))
            
            jarulek_item = QTableWidgetItem(tag[11])
            jarulek_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_idx, 12, jarulek_item)
            
            self.table.setItem(row_idx, 13, QTableWidgetItem(tag[12]))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GlassWindow()
    window.showMaximized()
    sys.exit(app.exec())