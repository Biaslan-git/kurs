#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт запуска системы справок о составе семьи
"""

import sys
import os

# Добавляем src в путь
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Импортируем и запускаем main
from main import main

if __name__ == '__main__':
    main()
