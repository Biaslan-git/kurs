#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                              QTableWidget, QTableWidgetItem, QHeaderView,
                              QMessageBox, QComboBox, QFrame)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from datetime import datetime


class RegistrationWidget(QWidget):
    def __init__(self, db, go_back):
        super().__init__()
        self.db = db
        self.go_back = go_back
        self.selected_address_id = None
        self.build()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.register()
        else:
            super().keyPressEvent(event)
    
    def build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        
        # Заголовок
        header = QHBoxLayout()
        back_btn = QPushButton("← Назад")
        back_btn.setStyleSheet("QPushButton { background: transparent; color: #0071E3; border: none; font-size: 15px; padding: 5px 10px; } QPushButton:hover { background: #E5E5EA; border-radius: 6px; }")
        back_btn.setFixedWidth(100)
        back_btn.clicked.connect(self.go_back)
        header.addWidget(back_btn)
        
        title = QLabel("✍️ Регистрация")
        title.setFont(QFont("-apple-system", 22, QFont.Weight.Bold))
        header.addWidget(title)
        header.addStretch()
        layout.addLayout(header)
        
        hint = QLabel("💡 Шаг 1: выберите адрес  →  Шаг 2: выберите жильца  →  Нажмите «Зарегистрировать»")
        hint.setStyleSheet("color: #0071E3; background: #E5F0FF; border-radius: 8px; padding: 10px; font-size: 13px;")
        layout.addWidget(hint)
        
        # Выбор адреса
        addr_card = QFrame()
        addr_card.setStyleSheet("background: white; border-radius: 12px; border: 1px solid #E5E5EA;")
        addr_layout = QHBoxLayout(addr_card)
        addr_layout.setContentsMargins(15, 12, 15, 12)
        
        addr_lbl = QLabel("🏠 Адрес:")
        addr_lbl.setFont(QFont("-apple-system", 13, QFont.Weight.Bold))
        addr_lbl.setStyleSheet("background: transparent; border: none;")
        addr_layout.addWidget(addr_lbl)
        
        self.address_combo = QComboBox()
        self.address_combo.currentIndexChanged.connect(self.on_address_changed)
        addr_layout.addWidget(self.address_combo, stretch=1)
        layout.addWidget(addr_card)
        
        # Таблица зарегистрированных
        reg_title = QLabel("Уже зарегистрированы по этому адресу:")
        reg_title.setFont(QFont("-apple-system", 13, QFont.Weight.Bold))
        reg_title.setStyleSheet("color: #1D1D1F;")
        layout.addWidget(reg_title)
        
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["ФИО", "Дата регистрации", "Родство"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table, stretch=2)
        
        # Форма добавления
        form_card = QFrame()
        form_card.setStyleSheet("background: white; border-radius: 12px; border: 1px solid #E5E5EA;")
        form_layout = QHBoxLayout(form_card)
        form_layout.setContentsMargins(15, 12, 15, 12)
        form_layout.setSpacing(15)
        
        res_lbl = QLabel("👤 Жилец:")
        res_lbl.setFont(QFont("-apple-system", 13, QFont.Weight.Bold))
        res_lbl.setStyleSheet("background: transparent; border: none;")
        form_layout.addWidget(res_lbl)
        
        self.resident_combo = QComboBox()
        form_layout.addWidget(self.resident_combo, stretch=2)
        
        rel_lbl = QLabel("Родство:")
        rel_lbl.setStyleSheet("background: transparent; border: none;")
        form_layout.addWidget(rel_lbl)
        
        self.relationship = QComboBox()
        self.relationship.addItems(["Глава семьи", "Супруг(а)", "Сын/дочь", "Отец/мать", "Другое"])
        form_layout.addWidget(self.relationship)
        layout.addWidget(form_card)
        
        # Кнопки
        btn_row = QHBoxLayout()
        
        reg_btn = QPushButton("➕ Зарегистрировать")
        reg_btn.setStyleSheet("QPushButton { background: #34C759; border-radius: 10px; padding: 10px 20px; font-weight: 600; color: white; border: none; } QPushButton:hover { background: #3DD768; }")
        reg_btn.clicked.connect(self.register)
        
        dereg_btn = QPushButton("🗑 Снять с учёта")
        dereg_btn.setStyleSheet("QPushButton { background: #FF3B30; border-radius: 10px; padding: 10px 20px; font-weight: 600; color: white; border: none; } QPushButton:hover { background: #FF453A; }")
        dereg_btn.clicked.connect(self.deregister)
        
        btn_row.addWidget(reg_btn)
        btn_row.addWidget(dereg_btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)
    
    def refresh(self):
        self.address_combo.blockSignals(True)
        self.address_combo.clear()
        self.address_data = {}
        
        addresses = self.db.get_all_addresses()
        for addr in addresses:
            full = self.db.format_address(addr)
            self.address_combo.addItem(full)
            self.address_data[full] = addr['id']
        
        self.address_combo.blockSignals(False)
        
        self.resident_combo.clear()
        self.resident_data = {}
        residents = self.db.get_all_residents()
        for res in residents:
            fio = self.db.format_resident_name(res)
            self.resident_combo.addItem(fio)
            self.resident_data[fio] = res['id']
        
        if self.address_combo.count() > 0:
            self.on_address_changed(0)
    
    def on_address_changed(self, index):
        text = self.address_combo.currentText()
        if text in self.address_data:
            self.selected_address_id = self.address_data[text]
            self.load_registered()
    
    def load_registered(self):
        if not self.selected_address_id:
            return
        regs = self.db.get_active_registrations_by_address(self.selected_address_id)
        self.table.setRowCount(len(regs))
        self.reg_ids = []
        
        for i, reg in enumerate(regs):
            fio = f"{reg['last_name']} {reg['first_name']}"
            if reg['patronymic']:
                fio += f" {reg['patronymic']}"
            self.table.setItem(i, 0, QTableWidgetItem(fio))
            self.table.setItem(i, 1, QTableWidgetItem(reg['registration_date']))
            self.table.setItem(i, 2, QTableWidgetItem(reg['relationship']))
            self.reg_ids.append(reg['id'])
    
    def register(self):
        if not self.selected_address_id:
            QMessageBox.warning(self, "Внимание", "Выберите адрес")
            return
        fio = self.resident_combo.currentText()
        if not fio or fio not in self.resident_data:
            QMessageBox.warning(self, "Внимание", "Выберите жильца")
            return
        try:
            self.db.add_registration(
                self.selected_address_id,
                self.resident_data[fio],
                datetime.now().strftime('%Y-%m-%d'),
                self.relationship.currentText()
            )
            self.load_registered()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
    
    def deregister(self):
        row = self.table.currentRow()
        if row < 0 or row >= len(self.reg_ids):
            QMessageBox.warning(self, "Внимание", "Выберите жильца из таблицы")
            return
        if QMessageBox.question(self, "Подтверждение", "Снять с учёта?") == QMessageBox.StandardButton.Yes:
            try:
                self.db.deregister_resident(self.reg_ids[row], datetime.now().strftime('%Y-%m-%d'))
                self.load_registered()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))
