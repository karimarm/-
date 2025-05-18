#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QComboBox, QGridLayout, QGroupBox, 
    QFormLayout, QSpinBox, QProgressBar, QTextEdit, 
    QTableWidget, QTableWidgetItem, QHeaderView, QRadioButton,
    QButtonGroup
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
        
        # Критерий 1: Источники на английском языке
        row = 0
        criteria_layout.addWidget(QLabel("Источники на английском языке:"), row, 0)
        
        english_radio_group = QButtonGroup(self)
        self.english_percent_radio = QRadioButton("Процент:")
        self.english_count_radio = QRadioButton("Количество:")
        english_radio_group.addButton(self.english_percent_radio)
        english_radio_group.addButton(self.english_count_radio)
        self.english_percent_radio.setChecked(True)
        
        # Размещение элементов в сетке
        criteria_layout.addWidget(self.english_percent_radio, row, 1)
        self.english_percent_spin = QSpinBox()
        self.english_percent_spin.setRange(0, 100)
        self.english_percent_spin.setSuffix("%")
        self.english_percent_spin.setFixedWidth(100)
        criteria_layout.addWidget(self.english_percent_spin, row, 2)
        
        row += 1
        criteria_layout.addWidget(self.english_count_radio, row, 1)
        self.english_count_spin = QSpinBox()
        self.english_count_spin.setRange(0, 1000)
        self.english_count_spin.setFixedWidth(100)
        criteria_layout.addWidget(self.english_count_spin, row, 2)
        
        # Критерий 2: Свежие источники
        row += 1
        criteria_layout.addWidget(QLabel("Источники свежее заданного года:"), row, 0)
        
        recent_radio_group = QButtonGroup(self)
        self.recent_percent_radio = QRadioButton("Процент:")
        self.recent_count_radio = QRadioButton("Количество:")
        recent_radio_group.addButton(self.recent_percent_radio)
        recent_radio_group.addButton(self.recent_count_radio)
        self.recent_percent_radio.setChecked(True)
        
        criteria_layout.addWidget(self.recent_percent_radio, row, 1)
        self.recent_percent_spin = QSpinBox()
        self.recent_percent_spin.setRange(0, 100)
        self.recent_percent_spin.setSuffix("%")
        self.recent_percent_spin.setFixedWidth(100)
        criteria_layout.addWidget(self.recent_percent_spin, row, 2)
        
        row += 1
        criteria_layout.addWidget(self.recent_count_radio, row, 1)
        self.recent_count_spin = QSpinBox()
        self.recent_count_spin.setRange(0, 1000)
        self.recent_count_spin.setFixedWidth(100)
        criteria_layout.addWidget(self.recent_count_spin, row, 2)
        
        row += 1
        criteria_layout.addWidget(QLabel("Год считать свежим начиная с:"), row, 0, 1, 1)
        self.recent_year_spin = QSpinBox()
        self.recent_year_spin.setRange(1900, 2100)
        self.recent_year_spin.setValue(2020)
        self.recent_year_spin.setFixedWidth(100)
        criteria_layout.addWidget(self.recent_year_spin, row, 2)
        
        # Критерий 3: Источники ВАК
        row += 1
        criteria_layout.addWidget(QLabel("Источники ВАК:"), row, 0)
        
        vak_radio_group = QButtonGroup(self)
        self.vak_percent_radio = QRadioButton("Процент:")
        self.vak_count_radio = QRadioButton("Количество:")
        vak_radio_group.addButton(self.vak_percent_radio)
        vak_radio_group.addButton(self.vak_count_radio)
        self.vak_percent_radio.setChecked(True)
        
        criteria_layout.addWidget(self.vak_percent_radio, row, 1)
        self.vak_percent_spin = QSpinBox()
        self.vak_percent_spin.setRange(0, 100)
        self.vak_percent_spin.setSuffix("%")
        self.vak_percent_spin.setFixedWidth(100)
        criteria_layout.addWidget(self.vak_percent_spin, row, 2)
        
        row += 1
        criteria_layout.addWidget(self.vak_count_radio, row, 1)
        self.vak_count_spin = QSpinBox()
        self.vak_count_spin.setRange(0, 1000)
        self.vak_count_spin.setFixedWidth(100)
        criteria_layout.addWidget(self.vak_count_spin, row, 2)
        
        # Критерий 4: Источники РИНЦ
        row += 1
        criteria_layout.addWidget(QLabel("Источники РИНЦ:"), row, 0)
        
        rinc_radio_group = QButtonGroup(self)
        self.rinc_percent_radio = QRadioButton("Процент:")
        self.rinc_count_radio = QRadioButton("Количество:")
        rinc_radio_group.addButton(self.rinc_percent_radio)
        rinc_radio_group.addButton(self.rinc_count_radio)
        self.rinc_percent_radio.setChecked(True)
        
        criteria_layout.addWidget(self.rinc_percent_radio, row, 1)
        self.rinc_percent_spin = QSpinBox()
        self.rinc_percent_spin.setRange(0, 100)
        self.rinc_percent_spin.setSuffix("%")
        self.rinc_percent_spin.setFixedWidth(100)
        criteria_layout.addWidget(self.rinc_percent_spin, row, 2)
        
        row += 1
        criteria_layout.addWidget(self.rinc_count_radio, row, 1)
        self.rinc_count_spin = QSpinBox()
        self.rinc_count_spin.setRange(0, 1000)
        self.rinc_count_spin.setFixedWidth(100)
        criteria_layout.addWidget(self.rinc_count_spin, row, 2)
        
        # Критерий 5: Источники одного автора
        row += 1
        criteria_layout.addWidget(QLabel("Источники с указанным автором:"), row, 0)
        
        # Добавляем поле для ввода ФИО автора
        row += 1
        criteria_layout.addWidget(QLabel("Укажите автора:"), row, 0, 1, 1)
        self.author_name_edit = QLineEdit()
        self.author_name_edit.setPlaceholderText("Например: Иванов И.И.")
        criteria_layout.addWidget(self.author_name_edit, row, 1, 1, 2)
        
        row += 1
        author_radio_group = QButtonGroup(self)
        self.author_percent_radio = QRadioButton("Максимальный процент источников с автором:")
        self.author_count_radio = QRadioButton("Максимальное количество источников с автором:")
        author_radio_group.addButton(self.author_percent_radio)
        author_radio_group.addButton(self.author_count_radio)
        self.author_percent_radio.setChecked(True)
        
        criteria_layout.addWidget(self.author_percent_radio, row, 1)
        self.author_percent_spin = QSpinBox()
        self.author_percent_spin.setRange(0, 100)
        self.author_percent_spin.setSuffix("%")
        self.author_percent_spin.setValue(100)
        self.author_percent_spin.setFixedWidth(100)
        criteria_layout.addWidget(self.author_percent_spin, row, 2)
        
        row += 1
        criteria_layout.addWidget(self.author_count_radio, row, 1)
        self.author_count_spin = QSpinBox()
        self.author_count_spin.setRange(0, 1000)
        self.author_count_spin.setValue(1000)
        self.author_count_spin.setFixedWidth(100)
        criteria_layout.addWidget(self.author_count_spin, row, 2)
        
        # Кнопки для работы с критериями
        row += 1
        buttons_layout = QHBoxLayout()
        
        self.check_button = QPushButton("Проверить критерии")
        buttons_layout.addWidget(self.check_button)
        
        self.save_button = QPushButton("Сохранить критерии")
        buttons_layout.addWidget(self.save_button)
        
        criteria_layout.addLayout(buttons_layout, row, 0, 1, 3)
        
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
        
        # Переключение радиокнопок
        self.english_percent_radio.toggled.connect(lambda checked: self.english_percent_spin.setEnabled(checked))
        self.english_count_radio.toggled.connect(lambda checked: self.english_count_spin.setEnabled(checked))
        
        self.recent_percent_radio.toggled.connect(lambda checked: self.recent_percent_spin.setEnabled(checked))
        self.recent_count_radio.toggled.connect(lambda checked: self.recent_count_spin.setEnabled(checked))
        
        self.vak_percent_radio.toggled.connect(lambda checked: self.vak_percent_spin.setEnabled(checked))
        self.vak_count_radio.toggled.connect(lambda checked: self.vak_count_spin.setEnabled(checked))
        
        self.rinc_percent_radio.toggled.connect(lambda checked: self.rinc_percent_spin.setEnabled(checked))
        self.rinc_count_radio.toggled.connect(lambda checked: self.rinc_count_spin.setEnabled(checked))
        
        self.author_percent_radio.toggled.connect(lambda checked: self.author_percent_spin.setEnabled(checked))
        self.author_count_radio.toggled.connect(lambda checked: self.author_count_spin.setEnabled(checked))
        
        # Начальное состояние - активированы только процентные поля
        self._update_spinbox_states()
    
    def _update_spinbox_states(self):
        """Обновление состояния полей ввода в зависимости от выбранных типов критериев"""
        self.english_percent_spin.setEnabled(self.english_percent_radio.isChecked())
        self.english_count_spin.setEnabled(self.english_count_radio.isChecked())
        
        self.recent_percent_spin.setEnabled(self.recent_percent_radio.isChecked())
        self.recent_count_spin.setEnabled(self.recent_count_radio.isChecked())
        
        self.vak_percent_spin.setEnabled(self.vak_percent_radio.isChecked())
        self.vak_count_spin.setEnabled(self.vak_count_radio.isChecked())
        
        self.rinc_percent_spin.setEnabled(self.rinc_percent_radio.isChecked())
        self.rinc_count_spin.setEnabled(self.rinc_count_radio.isChecked())
        
        self.author_percent_spin.setEnabled(self.author_percent_radio.isChecked())
        self.author_count_spin.setEnabled(self.author_count_radio.isChecked())
    
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
        criteria = {
            'min_recent_year': self.recent_year_spin.value(),
        }
        
        # Английские источники
        if self.english_percent_radio.isChecked():
            criteria['min_english_percent'] = self.english_percent_spin.value()
            criteria['min_english_count'] = 0
            criteria['english_criteria_type'] = 'percent'
        else:
            criteria['min_english_percent'] = 0
            criteria['min_english_count'] = self.english_count_spin.value()
            criteria['english_criteria_type'] = 'count'
        
        # Свежие источники
        if self.recent_percent_radio.isChecked():
            criteria['min_recent_percent'] = self.recent_percent_spin.value()
            criteria['min_recent_count'] = 0
            criteria['recent_criteria_type'] = 'percent'
        else:
            criteria['min_recent_percent'] = 0
            criteria['min_recent_count'] = self.recent_count_spin.value()
            criteria['recent_criteria_type'] = 'count'
        
        # Источники ВАК
        if self.vak_percent_radio.isChecked():
            criteria['min_vak_percent'] = self.vak_percent_spin.value()
            criteria['min_vak_count'] = 0
            criteria['vak_criteria_type'] = 'percent'
        else:
            criteria['min_vak_percent'] = 0
            criteria['min_vak_count'] = self.vak_count_spin.value()
            criteria['vak_criteria_type'] = 'count'
        
        # Источники РИНЦ
        if self.rinc_percent_radio.isChecked():
            criteria['min_rinc_percent'] = self.rinc_percent_spin.value()
            criteria['min_rinc_count'] = 0
            criteria['rinc_criteria_type'] = 'percent'
        else:
            criteria['min_rinc_percent'] = 0
            criteria['min_rinc_count'] = self.rinc_count_spin.value()
            criteria['rinc_criteria_type'] = 'count'
        
        # Источники указанного автора
        criteria['specified_author'] = self.author_name_edit.text().strip()
        if self.author_percent_radio.isChecked():
            criteria['max_single_author_percent'] = self.author_percent_spin.value()
            criteria['max_single_author_count'] = 1000
            criteria['author_criteria_type'] = 'percent'
        else:
            criteria['max_single_author_percent'] = 100
            criteria['max_single_author_count'] = self.author_count_spin.value()
            criteria['author_criteria_type'] = 'count'
        
        return criteria
    
    def set_criteria(self, criteria):
        """
        Установка критериев проверки
        
        Args:
            criteria (dict): Словарь с критериями проверки
        """
        # Установка года для свежих источников
        self.recent_year_spin.setValue(criteria.get('min_recent_year', 2020))
        
        # Английские источники
        self.english_percent_spin.setValue(criteria.get('min_english_percent', 0))
        self.english_count_spin.setValue(criteria.get('min_english_count', 0))
        if criteria.get('english_criteria_type') == 'count':
            self.english_count_radio.setChecked(True)
        else:
            self.english_percent_radio.setChecked(True)
        
        # Свежие источники
        self.recent_percent_spin.setValue(criteria.get('min_recent_percent', 0))
        self.recent_count_spin.setValue(criteria.get('min_recent_count', 0))
        if criteria.get('recent_criteria_type') == 'count':
            self.recent_count_radio.setChecked(True)
        else:
            self.recent_percent_radio.setChecked(True)
        
        # Источники ВАК
        self.vak_percent_spin.setValue(criteria.get('min_vak_percent', 0))
        self.vak_count_spin.setValue(criteria.get('min_vak_count', 0))
        if criteria.get('vak_criteria_type') == 'count':
            self.vak_count_radio.setChecked(True)
        else:
            self.vak_percent_radio.setChecked(True)
        
        # Источники РИНЦ
        self.rinc_percent_spin.setValue(criteria.get('min_rinc_percent', 0))
        self.rinc_count_spin.setValue(criteria.get('min_rinc_count', 0))
        if criteria.get('rinc_criteria_type') == 'count':
            self.rinc_count_radio.setChecked(True)
        else:
            self.rinc_percent_radio.setChecked(True)
        
        # Источники указанного автора
        self.author_name_edit.setText(criteria.get('specified_author', ''))
        self.author_percent_spin.setValue(criteria.get('max_single_author_percent', 100))
        self.author_count_spin.setValue(criteria.get('max_single_author_count', 1000))
        if criteria.get('author_criteria_type') == 'count':
            self.author_count_radio.setChecked(True)
        else:
            self.author_percent_radio.setChecked(True)
        
        # Обновление состояния полей ввода
        self._update_spinbox_states()
    
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