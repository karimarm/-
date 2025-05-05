#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QComboBox, QGroupBox, QFormLayout, QSpinBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
    QCheckBox, QRadioButton, QButtonGroup
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

class GoogleScholarSearchWidget(QWidget):
    """
    Виджет для поиска в Google Scholar
    """
    
    # Сигнал с результатами поиска
    search_signal = pyqtSignal(str, int, int, str)  # запрос, страница, результатов, язык
    add_citation_signal = pyqtSignal(int)  # индекс результата
    
    def __init__(self, parent=None):
        """Инициализация виджета поиска"""
        super().__init__(parent)
        
        # Создание компоновки
        self.create_layout()
        
        # Подключение обработчиков событий
        self.connect_events()
        
        # Результаты поиска
        self.search_results = []
    
    def create_layout(self):
        """Создание компоновки виджета"""
        main_layout = QVBoxLayout(self)
        
        # Группа настроек поиска
        search_group = QGroupBox("Поиск в Google Scholar")
        search_layout = QFormLayout()
        
        # Поисковый запрос
        self.query_edit = QLineEdit()
        self.query_edit.setPlaceholderText("Введите поисковый запрос...")
        search_layout.addRow("Запрос:", self.query_edit)
        
        # Настройки поиска (в одну строку)
        settings_layout = QHBoxLayout()
        
        # Язык результатов
        lang_layout = QVBoxLayout()
        lang_layout.addWidget(QLabel("Язык:"))
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["Русский", "Английский"])
        lang_layout.addWidget(self.lang_combo)
        settings_layout.addLayout(lang_layout)
        
        # Количество результатов
        results_layout = QVBoxLayout()
        results_layout.addWidget(QLabel("Результатов:"))
        self.results_spin = QSpinBox()
        self.results_spin.setMinimum(5)
        self.results_spin.setMaximum(50)
        self.results_spin.setValue(10)
        self.results_spin.setSingleStep(5)
        results_layout.addWidget(self.results_spin)
        settings_layout.addLayout(results_layout)
        
        # Тип публикации
        type_layout = QVBoxLayout()
        type_layout.addWidget(QLabel("Тип публикации:"))
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Все", "Статьи", "Книги", "Диссертации"])
        type_layout.addWidget(self.type_combo)
        settings_layout.addLayout(type_layout)
        
        # Временной диапазон
        time_layout = QVBoxLayout()
        time_layout.addWidget(QLabel("Период:"))
        self.time_combo = QComboBox()
        self.time_combo.addItems(["Любое время", "С 2020 года", "С 2015 года", "С 2010 года"])
        time_layout.addWidget(self.time_combo)
        settings_layout.addLayout(time_layout)
        
        search_layout.addRow("Фильтры:", settings_layout)
        
        # Кнопки поиска
        buttons_layout = QHBoxLayout()
        
        self.search_button = QPushButton("Поиск")
        self.search_button.setDefault(True)
        buttons_layout.addWidget(self.search_button)
        
        self.clear_button = QPushButton("Очистить")
        buttons_layout.addWidget(self.clear_button)
        
        search_layout.addRow("", buttons_layout)
        
        search_group.setLayout(search_layout)
        main_layout.addWidget(search_group)
        
        # Таблица результатов
        main_layout.addWidget(QLabel("Результаты поиска:"))
        
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(6)
        self.results_table.setHorizontalHeaderLabels(["", "Авторы", "Название", "Источник", "Год", "Цитирования"])
        
        # Настройка ширины колонок
        self.results_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.results_table.setColumnWidth(0, 30)  # Ширина чекбокса
        self.results_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.results_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.results_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.results_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Fixed)
        self.results_table.setColumnWidth(4, 60)  # Ширина колонки года
        self.results_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.Fixed)
        self.results_table.setColumnWidth(5, 100)  # Ширина колонки цитирований
        
        main_layout.addWidget(self.results_table)
        
        # Кнопки навигации и действий с результатами
        nav_buttons_layout = QHBoxLayout()
        
        self.prev_button = QPushButton("Предыдущая страница")
        self.prev_button.setEnabled(False)
        nav_buttons_layout.addWidget(self.prev_button)
        
        self.next_button = QPushButton("Следующая страница")
        self.next_button.setEnabled(False)
        nav_buttons_layout.addWidget(self.next_button)
        
        self.add_selected_button = QPushButton("Добавить выбранные в библиографию")
        nav_buttons_layout.addWidget(self.add_selected_button)
        
        main_layout.addLayout(nav_buttons_layout)
    
    def connect_events(self):
        """Подключение обработчиков событий"""
        # Кнопки поиска
        self.search_button.clicked.connect(self.on_search)
        self.clear_button.clicked.connect(self.on_clear)
        
        # Ввод Enter в поле запроса
        self.query_edit.returnPressed.connect(self.on_search)
        
        # Кнопки для работы с результатами
        self.add_selected_button.clicked.connect(self.on_add_selected)
        
        # Кнопки навигации
        self.prev_button.clicked.connect(self.on_prev_page)
        self.next_button.clicked.connect(self.on_next_page)
        
        # Двойной клик по элементу таблицы
        self.results_table.cellDoubleClicked.connect(self.on_item_double_clicked)
    
    def on_search(self):
        """Обработчик поиска"""
        # Получение поискового запроса
        query = self.query_edit.text().strip()
        
        if not query:
            QMessageBox.warning(
                self, 
                "Предупреждение", 
                "Введите поисковый запрос."
            )
            return
        
        # Получение языка результатов
        lang = "ru" if self.lang_combo.currentText() == "Русский" else "en"
        
        # Количество результатов
        num_results = self.results_spin.value()
        
        # Отправка сигнала на поиск (с нулевой страницей)
        self.current_page = 0
        self.search_signal.emit(query, self.current_page, num_results, lang)
    
    def on_clear(self):
        """Обработчик очистки результатов"""
        # Очистка поля запроса
        self.query_edit.clear()
        
        # Очистка таблицы результатов
        self.results_table.setRowCount(0)
        self.search_results = []
        
        # Сброс состояния кнопок навигации
        self.prev_button.setEnabled(False)
        self.next_button.setEnabled(False)
    
    def on_add_selected(self):
        """Обработчик добавления выбранных элементов в библиографию"""
        # Получение индексов выбранных элементов
        selected_indices = []
        for i in range(self.results_table.rowCount()):
            if self.results_table.item(i, 0).checkState() == Qt.Checked:
                selected_indices.append(i)
        
        if not selected_indices:
            QMessageBox.warning(
                self,
                "Предупреждение",
                "Выберите хотя бы один элемент для добавления в библиографию."
            )
            return
        
        # Отправка сигнала для каждого выбранного результата
        for index in selected_indices:
            self.add_citation_signal.emit(index)
    
    def on_prev_page(self):
        """Обработчик перехода на предыдущую страницу"""
        if self.current_page > 0:
            # Уменьшаем номер страницы на 10 (формат API)
            self.current_page -= 10
            
            # Повторяем поиск с новым номером страницы
            query = self.query_edit.text().strip()
            lang = "ru" if self.lang_combo.currentText() == "Русский" else "en"
            num_results = self.results_spin.value()
            
            self.search_signal.emit(query, self.current_page, num_results, lang)
    
    def on_next_page(self):
        """Обработчик перехода на следующую страницу"""
        # Увеличиваем номер страницы на 10 (формат API)
        self.current_page += 10
        
        # Повторяем поиск с новым номером страницы
        query = self.query_edit.text().strip()
        lang = "ru" if self.lang_combo.currentText() == "Русский" else "en"
        num_results = self.results_spin.value()
        
        self.search_signal.emit(query, self.current_page, num_results, lang)
    
    def on_item_double_clicked(self, row, column):
        """Обработчик двойного клика по элементу таблицы"""
        # Добавляем выбранный элемент в библиографию
        self.add_citation_signal.emit(row)
    
    def update_results(self, results):
        """
        Обновление таблицы результатов
        
        Args:
            results (list): Список объектов BibliographyItem
        """
        # Сохранение результатов
        self.search_results = results
        
        # Очистка таблицы
        self.results_table.setRowCount(0)
        
        # Заполнение таблицы данными
        for i, item in enumerate(results):
            self.results_table.insertRow(i)
            
            # Чекбокс для выбора
            checkbox = QTableWidgetItem()
            checkbox.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            checkbox.setCheckState(Qt.Unchecked)
            self.results_table.setItem(i, 0, checkbox)
            
            # Авторы
            authors_text = ", ".join(item.authors) if item.authors else ""
            self.results_table.setItem(i, 1, QTableWidgetItem(authors_text))
            
            # Название
            title_item = QTableWidgetItem(item.title if item.title else "")
            title_item.setToolTip(item.title)
            self.results_table.setItem(i, 2, title_item)
            
            # Источник (журнал)
            self.results_table.setItem(i, 3, QTableWidgetItem(item.journal if item.journal else ""))
            
            # Год
            self.results_table.setItem(i, 4, QTableWidgetItem(item.year if item.year else ""))
            
            # Цитирования
            citations = str(item.citations) if hasattr(item, 'citations') and item.citations else "0"
            self.results_table.setItem(i, 5, QTableWidgetItem(citations))
        
        # Обновление состояния кнопок навигации
        self.prev_button.setEnabled(self.current_page > 0)
        self.next_button.setEnabled(len(results) > 0)  # Если есть результаты, можно перейти дальше 