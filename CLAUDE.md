# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## О проекте

Система подготовки справок о составе семьи (форма № 9). Desktop-приложение на PyQt6 + SQLite для учебной курсовой работы КЧГУ.

## Команды

```bash
# Запуск
uv run python run.py

# Или без uv
python run.py

# Установка зависимостей
uv sync
# или
pip install -r requirements.txt

# Сборка в .exe
pyinstaller --onefile --windowed --name="Certificate_System" src/main.py
```

## Архитектура

```
src/
├── main.py           # Главное окно (MainWindow), глобальные стили (STYLE), CardButton
├── database.py       # Database класс — SQLite CRUD для 4 таблиц
├── gui_addresses.py  # AddressesWidget — справочник адресов
├── gui_residents.py  # ResidentsWidget — справочник жильцов
├── gui_registration.py # RegistrationWidget — привязка жильцов к адресам
└── gui_certificate.py  # CertificateWidget — формирование справки в Word (python-docx)
```

**Навигация**: `QStackedWidget` в `MainWindow` переключает между страницами. Каждый виджет получает `db` и `go_back` callback.

**Стили**: Глобальный QSS в `main.py:STYLE`. Классы через `setProperty("class", "...")`.

**БД**: `database/certificates.db` создаётся автоматически. Таблицы: `addresses`, `residents`, `registrations`, `certificates`.
