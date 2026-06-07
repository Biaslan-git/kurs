#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                              QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView,
                              QMessageBox, QFrame, QDateEdit)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont


class ResidentsWidget(QWidget):
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
        back_btn.setStyleSheet("QPushButton { background: transparent; color: #0071E3; border: none; font-size: 15px; padding: 5px 10px; } QPushButton:hover { background: #E5E5EA; border-radius: 6px; }")
        back_btn.clicked.connect(self.go_back)
        header.addWidget(back_btn)
        
        title = QLabel("👥 Жильцы")
        title.setFont(QFont("-apple-system", 22, QFont.Weight.Bold))
        header.addWidget(title)
        header.addStretch()
        layout.addLayout(header)
        
        # Подсказка
        hint = QLabel("💡 Добавьте жильцов: ФИО, дата рождения и паспортные данные")
        hint.setStyleSheet("color: #0071E3; background: #E5F0FF; border-radius: 8px; padding: 10px; font-size: 13px;")
        layout.addWidget(hint)
        
        # Поиск
        self.search = QLineEdit()
        self.search.setPlaceholderText("🔍 Поиск по ФИО...")
        self.search.textChanged.connect(self.load_data)
        layout.addWidget(self.search)
        
        # Таблица
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["ID", "ФИО", "Дата рождения", "Паспорт"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
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
        
        # Строка 1: ФИО
        row1 = QHBoxLayout()
        self.last_name = QLineEdit()
        self.last_name.setPlaceholderText("Фамилия")
        self.first_name = QLineEdit()
        self.first_name.setPlaceholderText("Имя")
        self.patronymic = QLineEdit()
        self.patronymic.setPlaceholderText("Отчество")
        row1.addWidget(self.last_name)
        row1.addWidget(self.first_name)
        row1.addWidget(self.patronymic)
        form_layout.addLayout(row1)
        
        # Строка 2: дата + паспорт
        row2 = QHBoxLayout()
        
        birth_layout = QVBoxLayout()
        birth_lbl = QLabel("Дата рождения")
        birth_lbl.setStyleSheet("color: #8E8E93; font-size: 11px; background: transparent; border: none;")
        self.birth_date = QDateEdit()
        self.birth_date.setDate(QDate(1990, 1, 1))
        self.birth_date.setCalendarPopup(True)
        self.birth_date.setDisplayFormat("dd.MM.yyyy")
        birth_layout.addWidget(birth_lbl)
        birth_layout.addWidget(self.birth_date)
        row2.addLayout(birth_layout)
        
        self.passport_series = QLineEdit()
        self.passport_series.setPlaceholderText("Серия паспорта")
        self.passport_number = QLineEdit()
        self.passport_number.setPlaceholderText("Номер паспорта")
        row2.addWidget(self.passport_series)
        row2.addWidget(self.passport_number)
        form_layout.addLayout(row2)
        
        # Строка 3: кем выдан + дата
        row3 = QHBoxLayout()
        self.issued_by = QLineEdit()
        self.issued_by.setPlaceholderText("Кем выдан")
        
        issue_layout = QVBoxLayout()
        issue_lbl = QLabel("Дата выдачи")
        issue_lbl.setStyleSheet("color: #8E8E93; font-size: 11px; background: transparent; border: none;")
        self.issue_date = QDateEdit()
        self.issue_date.setDate(QDate.currentDate())
        self.issue_date.setCalendarPopup(True)
        self.issue_date.setDisplayFormat("dd.MM.yyyy")
        issue_layout.addWidget(issue_lbl)
        issue_layout.addWidget(self.issue_date)
        
        row3.addWidget(self.issued_by, stretch=2)
        row3.addLayout(issue_layout)
        form_layout.addLayout(row3)
        
        layout.addWidget(form_card)
        
        # Кнопки
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)
        
        for text, color, hover, handler in [
            ("➕ Добавить", "#34C759", "#3DD768", self.add),
            ("✏️ Изменить", "#FF9500", "#FFAA00", self.update),
            ("🗑 Удалить", "#FF3B30", "#FF453A", self.delete),
            ("Очистить", "#8E8E93", "#9E9EA3", self.clear),
        ]:
            btn = QPushButton(text)
            btn.setStyleSheet(f"QPushButton {{ background: {color}; border-radius: 10px; padding: 10px 20px; font-weight: 600; color: white; border: none; }} QPushButton:hover {{ background: {hover}; }}")
            btn.clicked.connect(handler)
            btn_row.addWidget(btn)
        
        btn_row.addStretch()
        layout.addLayout(btn_row)
    
    def refresh(self):
        self.load_data()
    
    def load_data(self):
        search = self.search.text()
        residents = self.db.search_residents(search) if search else self.db.get_all_residents()
        
        self.table.setRowCount(len(residents))
        for i, res in enumerate(residents):
            fio = self.db.format_resident_name(res)
            passport = f"{res['passport_series']} {res['passport_number']}"
            self.table.setItem(i, 0, QTableWidgetItem(str(res['id'])))
            self.table.setItem(i, 1, QTableWidgetItem(fio))
            self.table.setItem(i, 2, QTableWidgetItem(res['birth_date']))
            self.table.setItem(i, 3, QTableWidgetItem(passport))
            self.table.item(i, 0).setData(Qt.ItemDataRole.UserRole, res['id'])
    
    def on_select(self, index):
        row = index.row()
        res_id = self.table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        self.selected_id = res_id
        res = self.db.get_resident_by_id(res_id)
        if res:
            self.last_name.setText(res['last_name'])
            self.first_name.setText(res['first_name'])
            self.patronymic.setText(res['patronymic'] or '')
            self.birth_date.setDate(QDate.fromString(res['birth_date'], "yyyy-MM-dd"))
            self.passport_series.setText(res['passport_series'])
            self.passport_number.setText(res['passport_number'])
            self.issued_by.setText(res['passport_issued_by'])
            self.issue_date.setDate(QDate.fromString(res['passport_issue_date'], "yyyy-MM-dd"))
    
    def clear(self):
        self.selected_id = None
        self.last_name.clear()
        self.first_name.clear()
        self.patronymic.clear()
        self.birth_date.setDate(QDate(1990, 1, 1))
        self.passport_series.clear()
        self.passport_number.clear()
        self.issued_by.clear()
        self.issue_date.setDate(QDate.currentDate())
    
    def add(self):
        if not self.last_name.text() or not self.first_name.text():
            QMessageBox.warning(self, "Внимание", "Введите фамилию и имя")
            return
        try:
            self.db.add_resident(
                self.last_name.text(), self.first_name.text(),
                self.patronymic.text() or None,
                self.birth_date.date().toString("yyyy-MM-dd"),
                self.passport_series.text(), self.passport_number.text(),
                self.issued_by.text(),
                self.issue_date.date().toString("yyyy-MM-dd")
            )
            self.load_data()
            self.clear()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
    
    def update(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Внимание", "Выберите жильца из таблицы")
            return
        try:
            self.db.update_resident(
                self.selected_id,
                self.last_name.text(), self.first_name.text(),
                self.patronymic.text() or None,
                self.birth_date.date().toString("yyyy-MM-dd"),
                self.passport_series.text(), self.passport_number.text(),
                self.issued_by.text(),
                self.issue_date.date().toString("yyyy-MM-dd")
            )
            self.load_data()
            self.clear()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
    
    def delete(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Внимание", "Выберите жильца из таблицы")
            return
        if QMessageBox.question(self, "Подтверждение", "Удалить этого жильца?") == QMessageBox.StandardButton.Yes:
            try:
                self.db.delete_resident(self.selected_id)
                self.load_data()
                self.clear()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))
