#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль работы с базой данных SQLite
"""

import sqlite3
import os
import sys
from datetime import datetime


class Database:
    """Класс для работы с базой данных"""
    
    def __init__(self, db_path=None):
        """Инициализация подключения к БД"""
        if db_path is None:
            # Для .exe — рядом с исполняемым файлом
            # Для обычного запуска — в папке database
            if getattr(sys, 'frozen', False):
                base_dir = os.path.dirname(sys.executable)
            else:
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            db_dir = os.path.join(base_dir, 'database')
            os.makedirs(db_dir, exist_ok=True)
            db_path = os.path.join(db_dir, 'certificates.db')
            
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        
        self.connect()
        self.create_tables()
        
    def connect(self):
        """Подключение к базе данных"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        
    def create_tables(self):
        """Создание таблиц БД"""
        # Таблица адресов
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS addresses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT NOT NULL DEFAULT 'Карачаевск',
                street TEXT NOT NULL,
                house TEXT NOT NULL,
                building TEXT,
                apartment TEXT NOT NULL
            )
        ''')
        
        # Таблица жильцов
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS residents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                last_name TEXT NOT NULL,
                first_name TEXT NOT NULL,
                patronymic TEXT,
                birth_date DATE NOT NULL,
                passport_series TEXT NOT NULL,
                passport_number TEXT NOT NULL,
                passport_issued_by TEXT NOT NULL,
                passport_issue_date DATE NOT NULL
            )
        ''')
        
        # Таблица регистраций
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS registrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                address_id INTEGER NOT NULL,
                resident_id INTEGER NOT NULL,
                registration_date DATE NOT NULL,
                deregistration_date DATE,
                relationship TEXT DEFAULT 'Член семьи',
                is_active BOOLEAN DEFAULT 1,
                FOREIGN KEY (address_id) REFERENCES addresses(id) ON DELETE CASCADE,
                FOREIGN KEY (resident_id) REFERENCES residents(id) ON DELETE CASCADE
            )
        ''')
        
        # Таблица выданных справок
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS certificates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                address_id INTEGER NOT NULL,
                issue_date DATE NOT NULL,
                issued_by TEXT NOT NULL,
                recipient TEXT NOT NULL,
                FOREIGN KEY (address_id) REFERENCES addresses(id)
            )
        ''')
        
        self.conn.commit()
        
    # ===== МЕТОДЫ ДЛЯ РАБОТЫ С АДРЕСАМИ =====
    
    def add_address(self, city, street, house, building, apartment):
        """Добавить новый адрес"""
        self.cursor.execute('''
            INSERT INTO addresses (city, street, house, building, apartment)
            VALUES (?, ?, ?, ?, ?)
        ''', (city, street, house, building, apartment))
        self.conn.commit()
        return self.cursor.lastrowid
        
    def get_all_addresses(self):
        """Получить все адреса"""
        self.cursor.execute('SELECT * FROM addresses ORDER BY street, house, apartment')
        return self.cursor.fetchall()
        
    def get_address_by_id(self, address_id):
        """Получить адрес по ID"""
        self.cursor.execute('SELECT * FROM addresses WHERE id = ?', (address_id,))
        return self.cursor.fetchone()
        
    def update_address(self, address_id, city, street, house, building, apartment):
        """Обновить адрес"""
        self.cursor.execute('''
            UPDATE addresses
            SET city = ?, street = ?, house = ?, building = ?, apartment = ?
            WHERE id = ?
        ''', (city, street, house, building, apartment, address_id))
        self.conn.commit()
        
    def delete_address(self, address_id):
        """Удалить адрес"""
        self.cursor.execute('DELETE FROM addresses WHERE id = ?', (address_id,))
        self.conn.commit()
        
    def search_addresses(self, search_text):
        """Поиск адресов"""
        search_pattern = f'%{search_text}%'
        self.cursor.execute('''
            SELECT * FROM addresses
            WHERE street LIKE ? OR house LIKE ? OR apartment LIKE ?
            ORDER BY street, house, apartment
        ''', (search_pattern, search_pattern, search_pattern))
        return self.cursor.fetchall()
        
    def format_address(self, address):
        """Форматировать адрес для отображения"""
        parts = [
            address['city'],
            f"ул. {address['street']}",
            f"д. {address['house']}"
        ]
        if address['building']:
            parts.append(f"корп. {address['building']}")
        parts.append(f"кв. {address['apartment']}")
        return ', '.join(parts)
        
    # ===== МЕТОДЫ ДЛЯ РАБОТЫ С ЖИЛЬЦАМИ =====
    
    def add_resident(self, last_name, first_name, patronymic, birth_date,
                    passport_series, passport_number, passport_issued_by,
                    passport_issue_date):
        """Добавить нового жильца"""
        self.cursor.execute('''
            INSERT INTO residents (
                last_name, first_name, patronymic, birth_date,
                passport_series, passport_number, passport_issued_by,
                passport_issue_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (last_name, first_name, patronymic, birth_date,
              passport_series, passport_number, passport_issued_by,
              passport_issue_date))
        self.conn.commit()
        return self.cursor.lastrowid
        
    def get_all_residents(self):
        """Получить всех жильцов"""
        self.cursor.execute('SELECT * FROM residents ORDER BY last_name, first_name')
        return self.cursor.fetchall()
        
    def get_resident_by_id(self, resident_id):
        """Получить жильца по ID"""
        self.cursor.execute('SELECT * FROM residents WHERE id = ?', (resident_id,))
        return self.cursor.fetchone()
        
    def update_resident(self, resident_id, last_name, first_name, patronymic,
                       birth_date, passport_series, passport_number,
                       passport_issued_by, passport_issue_date):
        """Обновить данные жильца"""
        self.cursor.execute('''
            UPDATE residents
            SET last_name = ?, first_name = ?, patronymic = ?,
                birth_date = ?, passport_series = ?, passport_number = ?,
                passport_issued_by = ?, passport_issue_date = ?
            WHERE id = ?
        ''', (last_name, first_name, patronymic, birth_date,
              passport_series, passport_number, passport_issued_by,
              passport_issue_date, resident_id))
        self.conn.commit()
        
    def delete_resident(self, resident_id):
        """Удалить жильца"""
        self.cursor.execute('DELETE FROM residents WHERE id = ?', (resident_id,))
        self.conn.commit()
        
    def search_residents(self, search_text):
        """Поиск жильцов"""
        search_pattern = f'%{search_text}%'
        self.cursor.execute('''
            SELECT * FROM residents
            WHERE last_name LIKE ? OR first_name LIKE ? OR patronymic LIKE ?
            ORDER BY last_name, first_name
        ''', (search_pattern, search_pattern, search_pattern))
        return self.cursor.fetchall()
        
    def format_resident_name(self, resident):
        """Форматировать ФИО жильца"""
        parts = [resident['last_name'], resident['first_name']]
        if resident['patronymic']:
            parts.append(resident['patronymic'])
        return ' '.join(parts)
        
    # ===== МЕТОДЫ ДЛЯ РАБОТЫ С РЕГИСТРАЦИЯМИ =====
    
    def add_registration(self, address_id, resident_id, registration_date, relationship):
        """Зарегистрировать жильца по адресу"""
        self.cursor.execute('''
            INSERT INTO registrations (
                address_id, resident_id, registration_date, relationship, is_active
            ) VALUES (?, ?, ?, ?, 1)
        ''', (address_id, resident_id, registration_date, relationship))
        self.conn.commit()
        return self.cursor.lastrowid
        
    def get_active_registrations_by_address(self, address_id):
        """Получить активные регистрации по адресу"""
        self.cursor.execute('''
            SELECT r.*, res.last_name, res.first_name, res.patronymic,
                   res.birth_date, res.passport_series, res.passport_number,
                   res.passport_issued_by, res.passport_issue_date
            FROM registrations r
            JOIN residents res ON r.resident_id = res.id
            WHERE r.address_id = ? AND r.is_active = 1
            ORDER BY r.registration_date
        ''', (address_id,))
        return self.cursor.fetchall()
        
    def deregister_resident(self, registration_id, deregistration_date):
        """Снять жильца с регистрации"""
        self.cursor.execute('''
            UPDATE registrations
            SET is_active = 0, deregistration_date = ?
            WHERE id = ?
        ''', (deregistration_date, registration_id))
        self.conn.commit()
        
    def check_resident_registered(self, address_id, resident_id):
        """Проверить, зарегистрирован ли жилец по адресу"""
        self.cursor.execute('''
            SELECT COUNT(*) as count FROM registrations
            WHERE address_id = ? AND resident_id = ? AND is_active = 1
        ''', (address_id, resident_id))
        result = self.cursor.fetchone()
        return result['count'] > 0
        
    # ===== МЕТОДЫ ДЛЯ РАБОТЫ СО СПРАВКАМИ =====
    
    def add_certificate(self, address_id, issue_date, issued_by, recipient):
        """Зарегистрировать выдачу справки"""
        self.cursor.execute('''
            INSERT INTO certificates (address_id, issue_date, issued_by, recipient)
            VALUES (?, ?, ?, ?)
        ''', (address_id, issue_date, issued_by, recipient))
        self.conn.commit()
        return self.cursor.lastrowid
        
    def get_certificates_by_address(self, address_id):
        """Получить историю выданных справок по адресу"""
        self.cursor.execute('''
            SELECT * FROM certificates
            WHERE address_id = ?
            ORDER BY issue_date DESC
        ''', (address_id,))
        return self.cursor.fetchall()
        
    def close(self):
        """Закрыть соединение с БД"""
        if self.conn:
            self.conn.close()
