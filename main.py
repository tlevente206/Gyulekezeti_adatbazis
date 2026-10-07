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
        
        # Alapértelmezett nézet
        self.current_view = "tagok"  # Lehet "tagok" vagy "presbiterek"
        
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

        self.font_family = "'Century Gothic', 'Bahnschrift', 'Segoe UI', sans-serif"

        # --- Felső sáv ---
        top_bar = QHBoxLayout()
        top_bar.setSpacing(8)
        
        self.title_label = QLabel("Gyülekezeti Adatbázis - Tagok")
        self.title_label.setStyleSheet(f"color: rgba(255, 255, 255, 200); font-size: 17px; font-weight: bold; font-family: {self.font_family};")
        
        self.btn_minimize = QPushButton("—")
        self.btn_minimize.setFixedSize(40, 35)
        self.btn_minimize.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_minimize.setStyleSheet(f"""
            QPushButton {{ background-color: transparent; color: #a6adc8; font-weight: bold; border: none; border-radius: 4px; font-family: {self.font_family}; }}
            QPushButton:hover {{ background-color: rgba(255, 255, 255, 25); color: white; }}
        """)
        self.btn_minimize.clicked.connect(self.showMinimized)

        self.btn_close = QPushButton("✕")
        self.btn_close.setFixedSize(40, 35)
        self.btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_close.setStyleSheet(f"""
            QPushButton {{ background-color: transparent; color: #a6adc8; font-weight: bold; border: none; border-radius: 4px; font-family: {self.font_family}; }}
            QPushButton:hover {{ background-color: rgba(220, 50, 50, 200); color: white; }}
        """)
        self.btn_close.clicked.connect(self.close)
        
        top_bar.addWidget(self.title_label)
        top_bar.addStretch()
        top_bar.addWidget(self.btn_minimize)
        top_bar.addWidget(self.btn_close)
        frame_layout.addLayout(top_bar)

        # --- Funkciógombok és Nézetváltó ---
        content_layout = QVBoxLayout()
        content_layout.setSpacing(15)
        
        action_bar = QHBoxLayout()
        action_bar.setSpacing(10)
        
        self.btn_style_normal = f"""
            QPushButton {{ background-color: rgba(255, 255, 255, 10); color: white; border: 1px solid rgba(255, 255, 255, 30); border-radius: 6px; padding: 8px 16px; font-size: 14px; font-family: {self.font_family}; }}
            QPushButton:hover {{ background-color: rgba(255, 255, 255, 25); border: 1px solid rgba(255, 255, 255, 60); }}
            QPushButton:pressed {{ background-color: rgba(255, 255, 255, 5); }}
        """
        self.btn_style_active = f"""
            QPushButton {{ background-color: rgba(255, 255, 255, 40); color: white; border: 1px solid white; border-radius: 6px; padding: 8px 16px; font-size: 14px; font-weight: bold; font-family: {self.font_family}; }}
        """
        
        # Bal oldal: CRUD gombok
        self.btn_add = QPushButton("Hozzáadás")
        self.btn_add.setStyleSheet(self.btn_style_normal)
        self.btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.btn_edit = QPushButton("Módosítás")
        self.btn_edit.setStyleSheet(self.btn_style_normal)
        self.btn_edit.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.btn_delete = QPushButton("Törlés")
        self.btn_delete.setStyleSheet(self.btn_style_normal)
        self.btn_delete.setCursor(Qt.CursorShape.PointingHandCursor)
        
        action_bar.addWidget(self.btn_add)
        action_bar.addWidget(self.btn_edit)
        action_bar.addWidget(self.btn_delete)
        action_bar.addStretch()
        
        # Jobb oldal: Nézetváltó gombok
        self.btn_view_tagok = QPushButton("Tagok nézete")
        self.btn_view_tagok.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_view_tagok.clicked.connect(lambda: self.switch_view("tagok"))
        
        self.btn_view_presbiterek = QPushButton("Presbiterek nézete")
        self.btn_view_presbiterek.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_view_presbiterek.clicked.connect(lambda: self.switch_view("presbiterek"))
        
        action_bar.addWidget(self.btn_view_tagok)
        action_bar.addWidget(self.btn_view_presbiterek)
        
        content_layout.addLayout(action_bar)
        
        # --- Táblázat inicializálása ---
        self.table = QTableWidget()
        self.table.setStyleSheet(f"""
            QTableWidget {{ background-color: rgba(20, 20, 30, 150); color: #e0e0e0; gridline-color: rgba(255, 255, 255, 15); border: 1px solid rgba(255, 255, 255, 20); border-radius: 8px; font-size: 13px; font-family: {self.font_family}; }}
            QHeaderView::section {{ background-color: rgba(40, 40, 55, 200); color: white; padding: 6px; border: none; border-right: 1px solid rgba(255, 255, 255, 15); border-bottom: 1px solid rgba(255, 255, 255, 15); font-weight: bold; font-size: 13px; font-family: {self.font_family}; }}
            QTableWidget::item:selected {{ background-color: rgba(255, 255, 255, 30); color: white; }}
            QTableWidget::item {{ padding: 5px; }}
        """)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setFrameShape(QFrame.Shape.NoFrame)
        self.table.setShowGrid(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        content_layout.addWidget(self.table)
        frame_layout.addLayout(content_layout)
        layout.addWidget(self.glass_frame)

        # Felület alapállapotba hozása
        self.switch_view("tagok")

    def switch_view(self, view_name):
        """Kicseréli a táblázat oszlopait és a gombok stílusát a kiválasztott nézet alapján."""
        self.current_view = view_name
        
        # Gombok stílusának frissítése
        if view_name == "tagok":
            self.btn_view_tagok.setStyleSheet(self.btn_style_active)
            self.btn_view_presbiterek.setStyleSheet(self.btn_style_normal)
            self.title_label.setText("Gyülekezeti Adatbázis - Tagok")
            
            oszlopok = ["ID", "Vezetéknév", "Keresztnév", "Születési idő", "Életkor", "Szül. hely", 
                        "Település", "Utca", "Házszám", "Neme", "Mióta tag", "Presbitere", 
                        "E. havi járulék", "Megjegyzés"]
        else:
            self.btn_view_presbiterek.setStyleSheet(self.btn_style_active)
            self.btn_view_tagok.setStyleSheet(self.btn_style_normal)
            self.title_label.setText("Gyülekezeti Adatbázis - Presbiterek")
            
            # A presbitereknél nincs "Presbitere" és "Járulék" oszlop (a megbeszélt DB séma szerint)
            oszlopok = ["ID", "Vezetéknév", "Keresztnév", "Születési idő", "Életkor", "Szül. hely", 
                        "Település", "Utca", "Házszám", "Neme", "Mióta presbiter", "Megjegyzés"]

        # Táblázat oszlopok beállítása
        self.table.clear()
        self.table.setColumnCount(len(oszlopok))
        self.table.setHorizontalHeaderLabels(oszlopok)
        self.table.setColumnHidden(0, True) # ID oszlop rejtve marad
        
        # Adatok betöltése
        self.load_dummy_data()

    def load_dummy_data(self):
        """Teszt adatok betöltése a kiválasztott nézetnek megfelelően."""
        if self.current_view == "tagok":
            adatok = [
                ("1", "Kovács", "János", "1985-05-12", "Debrecen", "Debrecen", "Kossuth utca", "12/B", "Férfi", "2010-01-15", "Tóth Péter", "✔️ Igen", "Aktív tag"),
                ("2", "Nagy", "Éva", "1992-11-23", "Budapest", "Hajdúszoboszló", "Fő utca", "5", "Nő", "2021-08-10", "Szabó Lajos", "❌ Nem", "Késik a fizetéssel")
            ]
        else:
            adatok = [
                ("1", "Tóth", "Péter", "1970-03-20", "Debrecen", "Debrecen", "Petőfi tér", "1", "Férfi", "2000-05-01", "Főpresbiter"),
                ("2", "Szabó", "Lajos", "1965-08-14", "Nyíregyháza", "Debrecen", "Piac utca", "42", "Férfi", "1998-10-10", "Pénztáros")
            ]
            
        self.table.setRowCount(len(adatok))
        for row_idx, sor in enumerate(adatok):
            for col_idx, ertek in enumerate(sor):
                # Ha az "Életkor" oszlophoz érünk (index 4-es), számoljuk ki dinamikusan
                if col_idx == 4:
                    eletkor = database.szamol_eletkor(sor[3]) # Születési idő alapján
                    item = QTableWidgetItem(eletkor)
                # Járulék középre igazítása (csak Tagok nézetben)
                elif self.current_view == "tagok" and col_idx == 11:
                    item = QTableWidgetItem(str(ertek))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                else:
                    item = QTableWidgetItem(str(ertek))
                
                self.table.setItem(row_idx, col_idx, item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GlassWindow()
    window.showMaximized()
    sys.exit(app.exec())