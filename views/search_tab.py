#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                            QPushButton, QComboBox, QTableWidget, QTableWidgetItem, 
                            QHeaderView, QCheckBox, QGroupBox, QSpinBox,
                            QRadioButton, QButtonGroup, QMessageBox, QProgressBar)
from PyQt5.QtCore import Qt, pyqtSignal

class SearchTab(QWidget):
    """
    Вкладка для поиска библиографических источников в онлайн-библиотеках.
    """
    
    # Сигналы
    search_requested = pyqtSignal(str, str, int)
    add_to_bibliography = pyqtSignal(list)
    
    def __init__(self):
        """Инициализация вкладки поиска"""
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Настройка интерфейса вкладки"""
        # Основной лейаут
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        
        # Заголовок
        title_label = QLabel("Поиск источников в онлайн-библиотеках")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        main_layout.addWidget(title_label)
        
        # Секция критериев поиска
        search_group = QGroupBox("Критерии поиска")
        search_layout = QVBoxLayout()
        
        # Строка поиска
        search_input_layout = QHBoxLayout()
        search_input_layout.addWidget(QLabel("Запрос:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Введите ключевые слова или название...")
        search_input_layout.addWidget(self.search_input)
        search_layout.addLayout(search_input_layout)
        
        # Источники для поиска
        sources_layout = QHBoxLayout()
        sources_layout.addWidget(QLabel("Источник:"))
        self.source_combo = QComboBox()
        self.source_combo.addItems(["Все источники", "Google Scholar", "eLIBRARY.RU", "Scopus", "КиберЛенинка"])
        sources_layout.addWidget(self.source_combo)
        
        # Количество результатов
        sources_layout.addWidget(QLabel("Количество результатов:"))
        self.results_spinbox = QSpinBox()
        self.results_spinbox.setRange(5, 50)
        self.results_spinbox.setValue(10)
        self.results_spinbox.setSingleStep(5)
        sources_layout.addWidget(self.results_spinbox)
        
        search_layout.addLayout(sources_layout)
        
        # Фильтры поиска
        filters_layout = QHBoxLayout()
        
        # Фильтр по языку
        self.language_group = QGroupBox("Язык")
        language_layout = QHBoxLayout()
        self.language_all = QRadioButton("Любой")
        self.language_ru = QRadioButton("Русский")
        self.language_en = QRadioButton("Английский")
        self.language_all.setChecked(True)
        language_layout.addWidget(self.language_all)
        language_layout.addWidget(self.language_ru)
        language_layout.addWidget(self.language_en)
        self.language_group.setLayout(language_layout)
        filters_layout.addWidget(self.language_group)
        
        # Фильтр по типу источника
        self.type_group = QGroupBox("Тип источника")
        type_layout = QHBoxLayout()
        self.type_all = QRadioButton("Любой")
        self.type_article = QRadioButton("Статья")
        self.type_book = QRadioButton("Книга")
        self.type_all.setChecked(True)
        type_layout.addWidget(self.type_all)
        type_layout.addWidget(self.type_article)
        type_layout.addWidget(self.type_book)
        self.type_group.setLayout(type_layout)
        filters_layout.addWidget(self.type_group)
        
        # Фильтр по признакам ВАК/РИНЦ
        self.flags_group = QGroupBox("Индексация")
        flags_layout = QHBoxLayout()
        self.vak_checkbox = QCheckBox("ВАК")
        self.rinc_checkbox = QCheckBox("РИНЦ")
        flags_layout.addWidget(self.vak_checkbox)
        flags_layout.addWidget(self.rinc_checkbox)
        self.flags_group.setLayout(flags_layout)
        filters_layout.addWidget(self.flags_group)
        
        search_layout.addLayout(filters_layout)
        
        # Кнопка поиска
        search_button_layout = QHBoxLayout()
        self.search_button = QPushButton("Найти")
        self.search_button.setMinimumWidth(120)
        self.search_button.setStyleSheet("font-weight: bold;")
        search_button_layout.addStretch()
        search_button_layout.addWidget(self.search_button)
        search_layout.addLayout(search_button_layout)
        
        search_group.setLayout(search_layout)
        main_layout.addWidget(search_group)
        
        # Прогресс поиска
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("Поиск... %p%")
        self.progress_bar.setHidden(True)
        main_layout.addWidget(self.progress_bar)
        
        # Результаты поиска
        results_group = QGroupBox("Результаты поиска")
        results_layout = QVBoxLayout()
        
        # Таблица результатов
        self.results_table = QTableWidget(0, 7)
        self.results_table.setHorizontalHeaderLabels(["", "Авторы", "Название", "Издание", "Год", "Тип", "Индексирование"])
        self.results_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.results_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.results_table.setEditTriggers(QTableWidget.NoEditTriggers)
        results_layout.addWidget(self.results_table)
        
        # Кнопки действий
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        self.view_details_button = QPushButton("Просмотр детали")
        self.add_selected_button = QPushButton("Добавить выбранные")
        self.add_all_button = QPushButton("Добавить все")
        
        buttons_layout.addWidget(self.view_details_button)
        buttons_layout.addWidget(self.add_selected_button)
        buttons_layout.addWidget(self.add_all_button)
        
        results_layout.addLayout(buttons_layout)
        results_group.setLayout(results_layout)
        
        main_layout.addWidget(results_group)
        
        # Установка основного лейаута
        self.setLayout(main_layout)
        
        # Подключение сигналов
        self.search_button.clicked.connect(self._on_search_clicked)
        self.add_selected_button.clicked.connect(self._on_add_selected_clicked)
        self.add_all_button.clicked.connect(self._on_add_all_clicked)
        self.view_details_button.clicked.connect(self._on_view_details_clicked)
        
        # Начальное состояние кнопок действий
        self.update_action_buttons_state()
    
    def _on_search_clicked(self):
        """Обработчик нажатия кнопки поиска"""
        query = self.search_input.text().strip()
        if not query:
            QMessageBox.warning(self, "Внимание", "Введите запрос для поиска")
            return
        
        # Определяем выбранный источник
        source_index = self.source_combo.currentIndex()
        sources = ["all", "scholar", "elibrary", "scopus", "cyberleninka"]
        source = sources[source_index] if source_index < len(sources) else "all"
        
        # Получаем количество результатов
        max_results = self.results_spinbox.value()
        
        # Показываем прогресс-бар
        self.progress_bar.setValue(0)
        self.progress_bar.setHidden(False)
        
        # Испускаем сигнал поиска
        self.search_requested.emit(query, source, max_results)
    
    def _on_add_selected_clicked(self):
        """Обработчик добавления выбранных результатов в библиографию"""
        selected_rows = set(item.row() for item in self.results_table.selectedItems())
        
        if not selected_rows:
            QMessageBox.information(self, "Информация", "Выберите результаты для добавления")
            return
        
        # Получаем выбранные элементы и испускаем сигнал
        selected_items = []
        for row in selected_rows:
            if hasattr(self.results_table, "_bibliography_items") and row < len(self.results_table._bibliography_items):
                selected_items.append(self.results_table._bibliography_items[row])
        
        if selected_items:
            self.add_to_bibliography.emit(selected_items)
            QMessageBox.information(self, "Успешно", f"Добавлено {len(selected_items)} источников в библиографию")
    
    def _on_add_all_clicked(self):
        """Обработчик добавления всех результатов в библиографию"""
        if hasattr(self.results_table, "_bibliography_items") and self.results_table._bibliography_items:
            self.add_to_bibliography.emit(self.results_table._bibliography_items)
            QMessageBox.information(self, "Успешно", 
                                   f"Добавлено {len(self.results_table._bibliography_items)} источников в библиографию")
        else:
            QMessageBox.information(self, "Информация", "Нет результатов для добавления")
    
    def _on_view_details_clicked(self):
        """Обработчик просмотра деталей выбранного источника"""
        selected_items = self.results_table.selectedItems()
        if not selected_items:
            QMessageBox.information(self, "Информация", "Выберите источник для просмотра")
            return
        
        # Получаем выбранный элемент
        row = selected_items[0].row()
        if hasattr(self.results_table, "_bibliography_items") and row < len(self.results_table._bibliography_items):
            item = self.results_table._bibliography_items[row]
            self._show_item_details(item)
    
    def _show_item_details(self, item):
        """
        Показать детали библиографического элемента
        
        Args:
            item (BibliographyItem): Библиографический элемент для отображения
        """
        # Создаем сообщение с деталями источника
        details = f"<b>Название:</b> {item.title}<br>"
        details += f"<b>Авторы:</b> {', '.join(item.authors)}<br>"
        if item.journal:
            details += f"<b>Журнал:</b> {item.journal}<br>"
        if item.publisher:
            details += f"<b>Издательство:</b> {item.publisher}<br>"
        if item.year:
            details += f"<b>Год:</b> {item.year}<br>"
        if item.volume:
            details += f"<b>Том:</b> {item.volume}<br>"
        if item.issue:
            details += f"<b>Номер:</b> {item.issue}<br>"
        if item.pages:
            details += f"<b>Страницы:</b> {item.pages}<br>"
        if item.doi:
            details += f"<b>DOI:</b> {item.doi}<br>"
        if item.url:
            details += f"<b>URL:</b> <a href='{item.url}'>{item.url}</a><br>"
        details += f"<b>Язык:</b> {'Английский' if item.language == 'en' else 'Русский'}<br>"
        details += f"<b>Тип:</b> {'Статья' if item.type == 'article' else 'Книга' if item.type == 'book' else 'Веб-ресурс' if item.type == 'web' else 'Другое'}<br>"
        details += f"<b>ВАК:</b> {'Да' if item.is_vak else 'Нет'}<br>"
        details += f"<b>РИНЦ:</b> {'Да' if item.is_rinc else 'Нет'}<br>"
        
        # Показываем сообщение с деталями
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Детали источника")
        msg_box.setTextFormat(Qt.RichText)
        msg_box.setText(details)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
    
    def display_results(self, results):
        """
        Отображение результатов поиска в таблице
        
        Args:
            results (list): Список объектов BibliographyItem
        """
        # Скрываем прогресс-бар
        self.progress_bar.setHidden(True)
        
        # Сохраняем полные объекты
        self.results_table._bibliography_items = results
        
        # Очищаем таблицу
        self.results_table.setRowCount(0)
        
        # Добавляем новые результаты
        for i, item in enumerate(results):
            self.results_table.insertRow(i)
            
            # Чекбокс для выбора
            checkbox_item = QTableWidgetItem()
            checkbox_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            checkbox_item.setCheckState(Qt.Unchecked)
            self.results_table.setItem(i, 0, checkbox_item)
            
            # Авторы
            authors_text = ", ".join(item.authors[:2])
            if len(item.authors) > 2:
                authors_text += " и др."
            self.results_table.setItem(i, 1, QTableWidgetItem(authors_text))
            
            # Название
            title_item = QTableWidgetItem(item.title)
            title_item.setToolTip(item.title)
            self.results_table.setItem(i, 2, title_item)
            
            # Издание (журнал или издательство)
            source = item.journal if item.journal else item.publisher if item.publisher else ""
            self.results_table.setItem(i, 3, QTableWidgetItem(source))
            
            # Год
            self.results_table.setItem(i, 4, QTableWidgetItem(item.year))
            
            # Тип источника
            type_map = {
                'article': 'Статья',
                'book': 'Книга',
                'web': 'Веб-ресурс'
            }
            type_text = type_map.get(item.type, 'Другое')
            self.results_table.setItem(i, 5, QTableWidgetItem(type_text))
            
            # Индексирование
            index_text = []
            if item.is_vak:
                index_text.append("ВАК")
            if item.is_rinc:
                index_text.append("РИНЦ")
            self.results_table.setItem(i, 6, QTableWidgetItem(", ".join(index_text)))
        
        # Обновляем состояние кнопок
        self.update_action_buttons_state()
    
    def update_action_buttons_state(self):
        """Обновление состояния кнопок действий"""
        has_items = hasattr(self.results_table, "_bibliography_items") and bool(self.results_table._bibliography_items)
        
        self.add_all_button.setEnabled(has_items)
        self.view_details_button.setEnabled(has_items and self.results_table.selectedItems())
        self.add_selected_button.setEnabled(has_items and self.results_table.selectedItems())
    
    def update_progress(self, value):
        """
        Обновление прогресс-бара
        
        Args:
            value (int): Значение прогресса (0-100)
        """
        self.progress_bar.setValue(value)
    
    def highlight_filters(self, conditions):
        """
        Подсветить фильтры, соответствующие условиям
        
        Args:
            conditions (dict): Словарь с условиями фильтрации
        """
        # Реализация подсветки фильтров по необходимости 