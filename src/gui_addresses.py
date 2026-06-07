#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                              QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView,
                              QMessageBox, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class AddressesWidget(QWidget):
    def __init__(self, db, go_back):
        super().__init__()
        self.db = db
        self.go_back = go_back
        self.selected_id = None
        self.build()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            if self.selected_id:
                self.update()
            else:
                self.add()
        else:
            super().keyPressEvent(event)
    
    def build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        
        # Заголовок
        header = QHBoxLayout()
        back_btn = QPushButton("← Назад")
        back_btn.setProperty("class", "back")
        back_btn.setFixedWidth(100)
        back_btn.clicked.connect(self.go_back)
        header.addWidget(back_btn)
        
        title = QLabel("📍 Адреса")
        title.setFont(QFont("-apple-system", 22, QFont.Weight.Bold))
        header.addWidget(title)
        header.addStretch()
        layout.addLayout(header)
        
        # Подсказка
        hint = QLabel("💡 Добавьте адреса: заполните поля ниже и нажмите «Добавить»")
        hint.setStyleSheet("color: #0071E3; background: #E5F0FF; border-radius: 8px; padding: 10px; font-size: 13px;")
        layout.addWidget(hint)
        
        # Поиск
        self.search = QLineEdit()
        self.search.setPlaceholderText("🔍 Поиск по адресу...")
        self.search.textChanged.connect(self.load_data)
        layout.addWidget(self.search)
        
        # Таблица
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["ID", "Адрес"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.clicked.connect(self.on_select)
        layout.addWidget(self.table, stretch=2)
        
        # Форма
        form_card = QFrame()
        form_card.setStyleSheet("background: white; border-radius: 12px; border: 1px solid #E5E5EA;")
        form_layout = QVBoxLayout(form_card)
        form_layout.setContentsMargins(15, 15, 15, 15)
        form_layout.setSpacing(10)
        
        form_title = QLabel("Редактирование")
        form_title.setFont(QFont("-apple-system", 13, QFont.Weight.Bold))
        form_title.setStyleSheet("color: #1D1D1F; background: transparent; border: none;")
        form_layout.addWidget(form_title)
        
        row1 = QHBoxLayout()
        self.city = QLineEdit()
        self.city.setPlaceholderText("Город")
        self.city.setText("Карачаевск")
        self.street = QLineEdit()
        self.street.setPlaceholderText("Улица")
        row1.addWidget(self.city)
        row1.addWidget(self.street)
        form_layout.addLayout(row1)
        
        row2 = QHBoxLayout()
        self.house = QLineEdit()
        self.house.setPlaceholderText("Дом")
        self.building = QLineEdit()
        self.building.setPlaceholderText("Корпус (необяз.)")
        self.apartment = QLineEdit()
        self.apartment.setPlaceholderText("Квартира")
        row2.addWidget(self.house)
        row2.addWidget(self.building)
        row2.addWidget(self.apartment)
        form_layout.addLayout(row2)
        
        layout.addWidget(form_card)
        
        # Кнопки
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)
        
        add_btn = QPushButton("➕ Добавить")
        add_btn.setProperty("class", "success")
        add_btn.setStyleSheet("QPushButton { background: #34C759; border-radius: 10px; padding: 10px 20px; font-weight: 600; color: white; } QPushButton:hover { background: #3DD768; }")
        add_btn.clicked.connect(self.add)
        
        edit_btn = QPushButton("✏️ Изменить")
        edit_btn.setStyleSheet("QPushButton { background: #FF9500; border-radius: 10px; padding: 10px 20px; font-weight: 600; color: white; } QPushButton:hover { background: #FFAA00; }")
        edit_btn.clicked.connect(self.update)
        
        del_btn = QPushButton("🗑 Удалить")
        del_btn.setStyleSheet("QPushButton { background: #FF3B30; border-radius: 10px; padding: 10px 20px; font-weight: 600; color: white; } QPushButton:hover { background: #FF453A; }")
        del_btn.clicked.connect(self.delete)
        
        clear_btn = QPushButton("Очистить")
        clear_btn.setStyleSheet("QPushButton { background: #8E8E93; border-radius: 10px; padding: 10px 20px; font-weight: 600; color: white; } QPushButton:hover { background: #9E9EA3; }")
        clear_btn.clicked.connect(self.clear)
        
        btn_row.addWidget(add_btn)
        btn_row.addWidget(edit_btn)
        btn_row.addWidget(del_btn)
        btn_row.addWidget(clear_btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)
    
    def refresh(self):
        self.load_data()
    
    def load_data(self):
        search = self.search.text()
        addresses = self.db.search_addresses(search) if search else self.db.get_all_addresses()
        
        self.table.setRowCount(len(addresses))
        for i, addr in enumerate(addresses):
            full = self.db.format_address(addr)
            self.table.setItem(i, 0, QTableWidgetItem(str(addr['id'])))
            self.table.setItem(i, 1, QTableWidgetItem(full))
            self.table.item(i, 0).setData(Qt.ItemDataRole.UserRole, addr['id'])
    
    def on_select(self, index):
        row = index.row()
        addr_id = self.table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        self.selected_id = addr_id
        addr = self.db.get_address_by_id(addr_id)
        if addr:
            self.city.setText(addr['city'])
            self.street.setText(addr['street'])
            self.house.setText(addr['house'])
            self.building.setText(addr['building'] or '')
            self.apartment.setText(addr['apartment'])
    
    def clear(self):
        self.selected_id = None
        self.city.setText("Карачаевск")
        self.street.clear()
        self.house.clear()
        self.building.clear()
        self.apartment.clear()
    
    def add(self):
        if not self.street.text() or not self.house.text() or not self.apartment.text():
            QMessageBox.warning(self, "Внимание", "Заполните улицу, дом и квартиру")
            return
        try:
            self.db.add_address(self.city.text(), self.street.text(), self.house.text(),
                               self.building.text() or None, self.apartment.text())
            self.load_data()
            self.clear()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
    
    def update(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Внимание", "Выберите адрес из таблицы")
            return
        try:
            self.db.update_address(self.selected_id, self.city.text(), self.street.text(),
                                  self.house.text(), self.building.text() or None, self.apartment.text())
            self.load_data()
            self.clear()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
    
    def delete(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Внимание", "Выберите адрес из таблицы")
            return
        if QMessageBox.question(self, "Подтверждение", "Удалить этот адрес?") == QMessageBox.StandardButton.Yes:
            try:
                self.db.delete_address(self.selected_id)
                self.load_data()
                self.clear()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))
