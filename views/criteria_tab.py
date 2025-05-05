#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QComboBox, QGridLayout, QGroupBox, 
    QFormLayout, QSpinBox, QProgressBar, QTextEdit, 
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor

class CriteriaTab(QWidget):
    """
    Вкладка для проверки соответствия библиографического списка критериям.
    """
    
    # Сигналы для взаимодействия с контроллером
    check_criteria_signal = pyqtSignal(dict)  # критерии для проверки
    save_criteria_signal = pyqtSignal(dict)   # критерии для сохранения
    
    def __init__(self, parent=None):
        """Инициализация вкладки проверки критериев"""
        super().__init__(parent)
        
        # Создание компоновки
        self.create_layout()
        
        # Подключение обработчиков событий
        self.connect_events()
    
    def create_layout(self):
        """Создание компоновки вкладки"""
        main_layout = QVBoxLayout(self)
        
        # Верхняя часть - настройка критериев
        criteria_group = QGroupBox("Настройка критериев проверки")
        criteria_layout = QGridLayout()
        
        # Критерий 1: Минимальный процент источников на английском языке
        criteria_layout.addWidget(QLabel("Минимальный процент на английском языке:"), 0, 0)
        self.english_percent_spin = QSpinBox()
        self.english_percent_spin.setRange(0, 100)
        self.english_percent_spin.setSuffix("%")
        self.english_percent_spin.setFixedWidth(100)
        criteria_layout.addWidget(self.english_percent_spin, 0, 1)
        
        # Критерий 2: Минимальный процент источников свежее заданного года
        criteria_layout.addWidget(QLabel("Минимальный процент свежих источников:"), 1, 0)
        self.recent_percent_spin = QSpinBox()
        self.recent_percent_spin.setRange(0, 100)
        self.recent_percent_spin.setSuffix("%")
        self.recent_percent_spin.setFixedWidth(100)
        criteria_layout.addWidget(self.recent_percent_spin, 1, 1)
        
        criteria_layout.addWidget(QLabel("Год считать свежим начиная с:"), 2, 0)
        self.recent_year_spin = QSpinBox()
        self.recent_year_spin.setRange(1900, 2100)
        self.recent_year_spin.setValue(2020)
        self.recent_year_spin.setFixedWidth(100)
        criteria_layout.addWidget(self.recent_year_spin, 2, 1)
        
        # Критерий 3: Минимальный процент источников ВАК
        criteria_layout.addWidget(QLabel("Минимальный процент источников ВАК:"), 3, 0)
        self.vak_percent_spin = QSpinBox()
        self.vak_percent_spin.setRange(0, 100)
        self.vak_percent_spin.setSuffix("%")
        self.vak_percent_spin.setFixedWidth(100)
        criteria_layout.addWidget(self.vak_percent_spin, 3, 1)
        
        # Критерий 4: Минимальный процент источников РИНЦ
        criteria_layout.addWidget(QLabel("Минимальный процент источников РИНЦ:"), 4, 0)
        self.rinc_percent_spin = QSpinBox()
        self.rinc_percent_spin.setRange(0, 100)
        self.rinc_percent_spin.setSuffix("%")
        self.rinc_percent_spin.setFixedWidth(100)
        criteria_layout.addWidget(self.rinc_percent_spin, 4, 1)
        
        # Критерий 5: Максимальный процент источников одного автора
        criteria_layout.addWidget(QLabel("Максимальный процент источников одного автора:"), 5, 0)
        self.author_percent_spin = QSpinBox()
        self.author_percent_spin.setRange(0, 100)
        self.author_percent_spin.setSuffix("%")
        self.author_percent_spin.setValue(100)
        self.author_percent_spin.setFixedWidth(100)
        criteria_layout.addWidget(self.author_percent_spin, 5, 1)
        
        # Кнопки для работы с критериями
        buttons_layout = QHBoxLayout()
        
        self.check_button = QPushButton("Проверить критерии")
        buttons_layout.addWidget(self.check_button)
        
        self.save_button = QPushButton("Сохранить критерии")
        buttons_layout.addWidget(self.save_button)
        
        criteria_layout.addLayout(buttons_layout, 6, 0, 1, 2)
        
        criteria_group.setLayout(criteria_layout)
        main_layout.addWidget(criteria_group)
        
        # Средняя часть - результаты проверки
        results_group = QGroupBox("Результаты проверки")
        results_layout = QVBoxLayout()
        
        # Таблица с результатами проверки
        self.results_table = QTableWidget(0, 4)
        self.results_table.setHorizontalHeaderLabels([
            "Критерий", 
            "Требуемое значение", 
            "Текущее значение", 
            "Соответствие"
        ])
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        results_layout.addWidget(self.results_table)
        
        results_group.setLayout(results_layout)
        main_layout.addWidget(results_group)
        
        # Нижняя часть - детальная статистика
        stats_group = QGroupBox("Детальная статистика")
        stats_layout = QVBoxLayout()
        
        # Текстовое поле для отображения статистики
        self.stats_text = QTextEdit()
        self.stats_text.setReadOnly(True)
        stats_layout.addWidget(self.stats_text)
        
        stats_group.setLayout(stats_layout)
        main_layout.addWidget(stats_group)
    
    def connect_events(self):
        """Подключение обработчиков событий"""
        self.check_button.clicked.connect(self.on_check_criteria)
        self.save_button.clicked.connect(self.on_save_criteria)
    
    def on_check_criteria(self):
        """Обработчик проверки критериев"""
        criteria = self.get_criteria()
        self.check_criteria_signal.emit(criteria)
    
    def on_save_criteria(self):
        """Обработчик сохранения критериев"""
        criteria = self.get_criteria()
        self.save_criteria_signal.emit(criteria)
    
    def get_criteria(self):
        """
        Получение текущих критериев проверки
        
        Returns:
            dict: Словарь с критериями проверки
        """
        return {
            'min_english_percent': self.english_percent_spin.value(),
            'min_recent_percent': self.recent_percent_spin.value(),
            'min_recent_year': self.recent_year_spin.value(),
            'min_vak_percent': self.vak_percent_spin.value(),
            'min_rinc_percent': self.rinc_percent_spin.value(),
            'max_single_author_percent': self.author_percent_spin.value()
        }
    
    def set_criteria(self, criteria):
        """
        Установка критериев проверки
        
        Args:
            criteria (dict): Словарь с критериями проверки
        """
        self.english_percent_spin.setValue(criteria.get('min_english_percent', 0))
        self.recent_percent_spin.setValue(criteria.get('min_recent_percent', 0))
        self.recent_year_spin.setValue(criteria.get('min_recent_year', 2020))
        self.vak_percent_spin.setValue(criteria.get('min_vak_percent', 0))
        self.rinc_percent_spin.setValue(criteria.get('min_rinc_percent', 0))
        self.author_percent_spin.setValue(criteria.get('max_single_author_percent', 100))
    
    def display_results(self, results):
        """
        Отображение результатов проверки критериев
        
        Args:
            results (dict): Словарь с результатами проверки
        """
        # Очистка таблицы
        self.results_table.setRowCount(0)
        
        # Заполнение таблицы результатами
        for i, (name, result) in enumerate(results.items()):
            self.results_table.insertRow(i)
            
            # Название критерия
            self.results_table.setItem(i, 0, QTableWidgetItem(result['name']))
            
            # Требуемое значение
            required_item = QTableWidgetItem(result['required'])
            self.results_table.setItem(i, 1, required_item)
            
            # Текущее значение
            current_item = QTableWidgetItem(result['current'])
            self.results_table.setItem(i, 2, current_item)
            
            # Соответствие критерию
            match_item = QTableWidgetItem("✓" if result['match'] else "✗")
            match_item.setTextAlignment(Qt.AlignCenter)
            if result['match']:
                match_item.setForeground(QColor(0, 128, 0))  # Зеленый цвет для соответствия
            else:
                match_item.setForeground(QColor(255, 0, 0))  # Красный цвет для несоответствия
            self.results_table.setItem(i, 3, match_item)
    
    def display_statistics(self, statistics):
        """
        Отображение детальной статистики
        
        Args:
            statistics (str): Текст с детальной статистикой
        """
        self.stats_text.setText(statistics) 