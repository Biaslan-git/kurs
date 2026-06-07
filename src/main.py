#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Система справок о составе семьи - PyQt6
"""

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                              QHBoxLayout, QLabel, QPushButton, QFrame, QStackedWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QPalette

from database import Database
from gui_addresses import AddressesWidget
from gui_residents import ResidentsWidget
from gui_registration import RegistrationWidget
from gui_certificate import CertificateWidget


STYLE = """
QWidget {
    font-family: -apple-system, 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif;
    font-size: 14px;
    background-color: #F5F5F7;
    color: #1D1D1F;
}

QMainWindow {
    background-color: #F5F5F7;
}

QPushButton {
    border: none;
    border-radius: 10px;
    padding: 10px 20px;
    font-size: 14px;
    font-weight: 600;
    color: white;
    background-color: #0071E3;
}

QPushButton:hover {
    background-color: #0077ED;
}

QPushButton:pressed {
    background-color: #005BBB;
}

QPushButton.danger {
    background-color: #FF3B30;
}
QPushButton.danger:hover {
    background-color: #FF453A;
}

QPushButton.warning {
    background-color: #FF9500;
    color: white;
}
QPushButton.warning:hover {
    background-color: #FFAA00;
}

QPushButton.success {
    background-color: #34C759;
}
QPushButton.success:hover {
    background-color: #3DD768;
}

QPushButton.secondary {
    background-color: #8E8E93;
}
QPushButton.secondary:hover {
    background-color: #9E9EA3;
}

QPushButton.back {
    background-color: transparent;
    color: #0071E3;
    font-size: 15px;
    padding: 5px 10px;
}
QPushButton.back:hover {
    background-color: #E5E5EA;
}

QLineEdit {
    border: 1px solid #D1D1D6;
    border-radius: 8px;
    padding: 8px 12px;
    background-color: white;
    font-size: 14px;
    color: #1D1D1F;
    selection-background-color: #0071E3;
}

QLineEdit:focus {
    border: 2px solid #0071E3;
}

QLineEdit::placeholder {
    color: #AEAEB2;
}

QComboBox {
    border: 1px solid #D1D1D6;
    border-radius: 8px;
    padding: 8px 12px;
    background-color: white;
    font-size: 14px;
    color: #1D1D1F;
}

QComboBox:focus {
    border: 2px solid #0071E3;
}

QComboBox::drop-down {
    border: none;
    width: 24px;
}

QComboBox QAbstractItemView {
    border: 1px solid #D1D1D6;
    border-radius: 8px;
    background-color: white;
    selection-background-color: #E5F0FF;
    selection-color: #0071E3;
}

QTableWidget {
    border: 1px solid #D1D1D6;
    border-radius: 10px;
    background-color: white;
    gridline-color: #F2F2F7;
    outline: none;
    color: #1D1D1F;
}

QTableWidget::item {
    padding: 10px;
    border: none;
}

QTableWidget::item:selected {
    background-color: #E5F0FF;
    color: #0071E3;
}

QHeaderView::section {
    background-color: #F2F2F7;
    border: none;
    border-bottom: 1px solid #D1D1D6;
    padding: 10px;
    font-weight: 600;
    color: #8E8E93;
    font-size: 12px;
    text-transform: uppercase;
}

QScrollBar:vertical {
    width: 8px;
    background: transparent;
}

QScrollBar::handle:vertical {
    background: #C7C7CC;
    border-radius: 4px;
    min-height: 30px;
}

QFrame.card {
    background-color: white;
    border-radius: 12px;
    border: 1px solid #E5E5EA;
}

QLabel.title {
    font-size: 28px;
    font-weight: 700;
    color: #1D1D1F;
}

QLabel.subtitle {
    font-size: 15px;
    color: #8E8E93;
}

QLabel.section {
    font-size: 13px;
    font-weight: 600;
    color: #8E8E93;
    text-transform: uppercase;
}

QLabel.hint {
    font-size: 13px;
    color: #636366;
    padding: 10px;
    background-color: #E5F0FF;
    border-radius: 8px;
}
"""


class CardButton(QFrame):
    """Карточка-кнопка на главном экране"""

    def __init__(self, icon, title, description, color, callback):
        super().__init__()
        self.callback = callback
        self.color = color
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedSize(220, 160)
        self.setFrameShape(QFrame.Shape.NoFrame)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)
        
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Arial", 32))
        icon_label.setStyleSheet("background: transparent; border: none;")
        layout.addWidget(icon_label)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("-apple-system", 16, QFont.Weight.Bold))
        title_label.setStyleSheet(f"color: white; background: transparent; border: none;")
        layout.addWidget(title_label)
        
        desc_label = QLabel(description)
        desc_label.setFont(QFont("-apple-system", 11))
        desc_label.setStyleSheet("color: rgba(255,255,255,0.8); background: transparent; border: none;")
        layout.addWidget(desc_label)
        
        layout.addStretch()
        
        self.update_style(False)
    
    def update_style(self, hovered):
        color = self.color
        if hovered:
            r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
            r = min(255, r + 20)
            g = min(255, g + 20)
            b = min(255, b + 20)
            color = f"#{r:02X}{g:02X}{b:02X}"

        self.setStyleSheet(f"background-color: {color}; border-radius: 16px;")
    
    def enterEvent(self, event):
        self.update_style(True)
    
    def leaveEvent(self, event):
        self.update_style(False)
    
    def mousePressEvent(self, event):
        self.callback()


class MainWindow(QMainWindow):
    """Главное окно"""
    
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.help_dialog = None

        self.setWindowTitle("Система справок о составе семьи")
        self.setMinimumSize(900, 650)

        # Стек страниц
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Страницы
        self.main_page = self.create_main_page()
        self.addresses_page = AddressesWidget(self.db, self.show_main)
        self.residents_page = ResidentsWidget(self.db, self.show_main)
        self.registration_page = RegistrationWidget(self.db, self.show_main)
        self.certificate_page = CertificateWidget(self.db, self.show_main)

        self.stack.addWidget(self.main_page)
        self.stack.addWidget(self.addresses_page)
        self.stack.addWidget(self.residents_page)
        self.stack.addWidget(self.registration_page)
        self.stack.addWidget(self.certificate_page)

        self.show_main()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_F1:
            self.show_help()
        elif event.key() == Qt.Key.Key_Escape:
            if self.stack.currentWidget() != self.main_page:
                self.show_main()
        else:
            super().keyPressEvent(event)

    def show_help(self):
        if self.help_dialog is None:
            self.help_dialog = HelpDialog(self)
        self.help_dialog.show()
        self.help_dialog.raise_()
    
    def create_main_page(self):
        """Главный экран"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)
        
        # Заголовок
        header = QVBoxLayout()
        header.setSpacing(8)
        
        title = QLabel("Справки о составе семьи")
        title.setFont(QFont("-apple-system", 28, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setProperty("class", "title")
        header.addWidget(title)
        
        subtitle = QLabel("Формирование справок по форме № 9")
        subtitle.setFont(QFont("-apple-system", 15))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #8E8E93;")
        header.addWidget(subtitle)
        
        layout.addLayout(header)
        
        # Контент: инструкция + кнопки
        content = QHBoxLayout()
        content.setSpacing(30)
        
        # Левая панель - инструкция
        hint_card = QFrame()
        hint_card.setProperty("class", "card")
        hint_card.setFixedWidth(260)
        hint_card.setStyleSheet("background-color: white; border-radius: 16px; border: 1px solid #E5E5EA;")
        
        hint_layout = QVBoxLayout(hint_card)
        hint_layout.setContentsMargins(20, 20, 20, 20)
        hint_layout.setSpacing(12)
        
        hint_title = QLabel("💡 Как начать?")
        hint_title.setFont(QFont("-apple-system", 17, QFont.Weight.Bold))
        hint_title.setStyleSheet("color: #1D1D1F; background: transparent;")
        hint_layout.addWidget(hint_title)
        
        steps = [
            ("1️⃣", "Добавьте адреса", "улица, дом, квартира"),
            ("2️⃣", "Добавьте жильцов", "ФИО, паспорт"),
            ("3️⃣", "Зарегистрируйте", "свяжите с адресами"),
            ("4️⃣", "Сформируйте справку", "документ Word"),
        ]
        
        for emoji, step, sub in steps:
            step_layout = QHBoxLayout()
            step_layout.setSpacing(10)
            
            em = QLabel(emoji)
            em.setFont(QFont("Arial", 18))
            em.setStyleSheet("background: transparent;")
            em.setFixedWidth(30)
            step_layout.addWidget(em)
            
            texts = QVBoxLayout()
            texts.setSpacing(2)
            
            step_label = QLabel(step)
            step_label.setFont(QFont("-apple-system", 13, QFont.Weight.Bold))
            step_label.setStyleSheet("color: #1D1D1F; background: transparent;")
            texts.addWidget(step_label)
            
            sub_label = QLabel(sub)
            sub_label.setFont(QFont("-apple-system", 11))
            sub_label.setStyleSheet("color: #8E8E93; background: transparent;")
            texts.addWidget(sub_label)
            
            step_layout.addLayout(texts)
            hint_layout.addLayout(step_layout)
        
        hint_layout.addStretch()
        content.addWidget(hint_card)
        
        # Правая панель - карточки-кнопки
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(15)
        
        row1 = QHBoxLayout()
        row1.setSpacing(15)
        row1.addWidget(CardButton("📍", "Адреса", "Управление адресами", "#E63946", self.show_addresses))
        row1.addWidget(CardButton("👥", "Жильцы", "База жильцов", "#2A9D8F", self.show_residents))
        buttons_layout.addLayout(row1)

        row2 = QHBoxLayout()
        row2.setSpacing(15)
        row2.addWidget(CardButton("✍️", "Регистрация", "Регистрация по адресам", "#E85D04", self.show_registration))
        row2.addWidget(CardButton("📄", "Справка", "Сформировать справку", "#2D8A4E", self.show_certificate))
        buttons_layout.addLayout(row2)
        
        content.addLayout(buttons_layout)
        layout.addLayout(content)
        
        # Футер
        footer = QLabel("Байрамкулов Биаслан, гр. 33 ФЭУ  •  КЧГУ им. У.Д. Алиева  •  2025")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet("color: #AEAEB2; font-size: 12px;")
        layout.addWidget(footer)
        
        return page
    
    def show_main(self):
        self.stack.setCurrentWidget(self.main_page)
    
    def show_addresses(self):
        self.addresses_page.refresh()
        self.stack.setCurrentWidget(self.addresses_page)
    
    def show_residents(self):
        self.residents_page.refresh()
        self.stack.setCurrentWidget(self.residents_page)
    
    def show_registration(self):
        self.registration_page.refresh()
        self.stack.setCurrentWidget(self.registration_page)
    
    def show_certificate(self):
        self.certificate_page.refresh()
        self.stack.setCurrentWidget(self.certificate_page)


class SplashScreen(QWidget):
    """Заставка при запуске"""

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(400, 300)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 20px;
                border: 1px solid #E5E5EA;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(30, 30, 30, 30)
        card_layout.setSpacing(15)

        icon = QLabel("📋")
        icon.setFont(QFont("Arial", 48))
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(icon)

        title = QLabel("Система справок\nо составе семьи")
        title.setFont(QFont("-apple-system", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #1D1D1F;")
        card_layout.addWidget(title)

        version = QLabel("Версия 1.0")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version.setStyleSheet("color: #8E8E93; font-size: 14px;")
        card_layout.addWidget(version)

        card_layout.addStretch()

        author = QLabel("Выполнил: Байрамкулов Биаслан\nГруппа 33, ФЭУ\nКЧГУ им. У.Д. Алиева, 2025")
        author.setAlignment(Qt.AlignmentFlag.AlignCenter)
        author.setStyleSheet("color: #8E8E93; font-size: 12px;")
        card_layout.addWidget(author)

        layout.addWidget(card)

        screen = QApplication.primaryScreen().geometry()
        self.move((screen.width() - 400) // 2, (screen.height() - 300) // 2)


class HelpDialog(QWidget):
    """Окно справки"""

    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowType.Window)
        self.setWindowTitle("Справка")
        self.setFixedSize(500, 450)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        title = QLabel("📖 Справка по программе")
        title.setFont(QFont("-apple-system", 18, QFont.Weight.Bold))
        layout.addWidget(title)

        help_text = """
<b>Система справок о составе семьи</b><br><br>

<b>Порядок работы:</b><br>
1. <b>Адреса</b> — добавьте адреса (город, улица, дом, квартира)<br>
2. <b>Жильцы</b> — добавьте жильцов (ФИО, паспортные данные)<br>
3. <b>Регистрация</b> — зарегистрируйте жильцов по адресам<br>
4. <b>Справка</b> — сформируйте справку в формате Word<br><br>

<b>Горячие клавиши:</b><br>
• F1 — открыть справку<br>
• Enter — подтвердить ввод<br>
• Esc — закрыть окно / вернуться назад<br>
• Tab — переход между полями<br><br>

<b>База данных:</b><br>
Данные сохраняются в файле database/certificates.db<br><br>

<b>Курсовая работа</b><br>
Выполнил: Байрамкулов Биаслан, группа 33, ФЭУ<br>
Дисциплина: Проектирование информационных систем<br>
Направление: 09.03.03 Прикладная информатика<br>
КЧГУ им. У.Д. Алиева, 2025
        """

        text = QLabel(help_text)
        text.setWordWrap(True)
        text.setStyleSheet("font-size: 13px; line-height: 1.5;")
        layout.addWidget(text)

        layout.addStretch()

        close_btn = QPushButton("Закрыть")
        close_btn.setFixedWidth(120)
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape or event.key() == Qt.Key.Key_F1:
            self.close()
        else:
            super().keyPressEvent(event)


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE)

    splash = SplashScreen()
    splash.show()
    app.processEvents()

    import time
    time.sleep(1.5)

    window = MainWindow()
    window.show()

    splash.close()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
