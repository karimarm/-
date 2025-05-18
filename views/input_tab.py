#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QTextEdit, QPushButton, QComboBox, QGridLayout, 
    QGroupBox, QListWidget, QListWidgetItem, QSplitter, 
    QFormLayout, QRadioButton, QButtonGroup, QTableView,
    QHeaderView, QAbstractItemView
)
from PyQt5.QtCore import Qt, pyqtSignal, QAbstractTableModel, QModelIndex
from PyQt5.QtGui import QFont
from datetime import datetime

class BibliographyTableModel(QAbstractTableModel):
    """
    Модель данных для таблицы библиографических ссылок.
    """
    
    def __init__(self, items=None):
        super().__init__()
        self.items = items or []
        self.filtered_items = []
        self.filter_text = ""
        self.headers = [
            "Библиографическая ссылка", 
            "Авторы", 
            "Название", 
            "Год", 
            "Источник", 
            "Страницы",
            "Тип",
            "ВАК",
            "РИНЦ",
            "Язык",
            "DOI/URL"
        ]
        self._apply_filter()
    
    def rowCount(self, parent=QModelIndex()):
        return len(self.filtered_items)
    
    def columnCount(self, parent=QModelIndex()):
        return len(self.headers)
    
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self.filtered_items)):
            return None
        
        item = self.filtered_items[index.row()]
        
        if role == Qt.DisplayRole:
            col = index.column()
            if col == 0:  # Полная библиографическая ссылка
                # Сначала пробуем использовать raw_text, если он есть
                if hasattr(item, 'raw_text') and item.raw_text:
                    return item.raw_text
                # Потом проверяем 'full_reference'
                if hasattr(item, 'full_reference') and item.full_reference:
                    return item.full_reference
                # В крайнем случае используем строковое представление
                return str(item)
            elif col == 1:  # Авторы
                if hasattr(item, 'authors'):
                    if isinstance(item.authors, list):
                        return ", ".join(item.authors)
                    return str(item.authors)
                return ""
            elif col == 2:  # Название
                return getattr(item, 'title', "")
            elif col == 3:  # Год
                return getattr(item, 'year', "")
            elif col == 4:  # Источник (журнал/издательство)
                if hasattr(item, 'journal') and item.journal:
                    return item.journal
                return getattr(item, 'publisher', "")
            elif col == 5:  # Страницы
                return getattr(item, 'pages', "")
            elif col == 6:  # Тип
                # Перевод типа в читаемый вид
                type_value = getattr(item, 'type', "")
                type_mapping = {
                    "book": "Книга",
                    "article": "Статья", 
                    "web": "Веб-ресурс",
                    "other": "Другое"
                }
                return type_mapping.get(type_value, type_value)
            elif col == 7:  # ВАК
                return "Да" if getattr(item, 'is_vak', False) else "Нет"
            elif col == 8:  # РИНЦ
                return "Да" if getattr(item, 'is_rinc', False) else "Нет"
            elif col == 9:  # Язык
                lang = getattr(item, 'language', 'ru')
                return "Английский" if lang == 'en' else "Русский"
            elif col == 10:  # DOI/URL
                doi = getattr(item, 'doi', "")
                url = getattr(item, 'url', "")
                if doi:
                    return f"DOI: {doi}"
                elif url:
                    return f"URL: {url}"
                return ""
        
        # Для чекбоксов ВАК и РИНЦ добавим роль Qt.CheckStateRole
        elif role == Qt.CheckStateRole:
            col = index.column()
            if col == 7:  # ВАК
                return Qt.Checked if getattr(item, 'is_vak', False) else Qt.Unchecked
            elif col == 8:  # РИНЦ
                return Qt.Checked if getattr(item, 'is_rinc', False) else Qt.Unchecked
        
        return None
    
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.headers[section]
        return None
    
    def setItems(self, items):
        self.beginResetModel()
        self.items = items
        self._apply_filter()
        self.endResetModel()
    
    def set_filter(self, filter_text):
        """
        Установка фильтра для отображаемых элементов
        
        Args:
            filter_text (str): Текст для фильтрации
        """
        self.filter_text = filter_text.lower()
        self.beginResetModel()
        self._apply_filter()
        self.endResetModel()
    
    def _apply_filter(self):
        """Применение фильтра к элементам"""
        if not self.filter_text:
            self.filtered_items = self.items
            return
        
        self.filtered_items = []
        for item in self.items:
            # Получаем строковое представление для поиска
            item_str = str(item).lower()
            
            # Проверяем авторов
            authors_match = False
            if hasattr(item, 'authors'):
                if isinstance(item.authors, list):
                    authors_match = any(self.filter_text in author.lower() for author in item.authors)
                else:
                    authors_match = self.filter_text in str(item.authors).lower()
            
            # Проверяем другие поля
            title_match = self.filter_text in getattr(item, 'title', "").lower()
            year_match = self.filter_text in getattr(item, 'year', "").lower()
            journal_match = self.filter_text in getattr(item, 'journal', "").lower()
            publisher_match = self.filter_text in getattr(item, 'publisher', "").lower()
            
            # Проверка по новым полям
            doi_match = self.filter_text in getattr(item, 'doi', "").lower()
            url_match = self.filter_text in getattr(item, 'url', "").lower()
            
            # Проверка по флагам ВАК и РИНЦ
            vak_match = (self.filter_text in "вак" and getattr(item, 'is_vak', False))
            rinc_match = (self.filter_text in "ринц" and getattr(item, 'is_rinc', False))
            
            # Проверка по языку
            language = getattr(item, 'language', 'ru')
            language_match = (
                (self.filter_text in "русский" and language == 'ru') or
                (self.filter_text in "английский" and language == 'en')
            )
            
            # Если хотя бы одно совпадение, добавляем в отфильтрованный список
            if (self.filter_text in item_str or authors_match or title_match or 
                year_match or journal_match or publisher_match or doi_match or 
                url_match or vak_match or rinc_match or language_match):
                self.filtered_items.append(item)
    
    def sort(self, column, order):
        """
        Сортировка элементов по указанной колонке
        
        Args:
            column (int): Индекс колонки для сортировки
            order (Qt.SortOrder): Порядок сортировки
        """
        self.beginResetModel()
        
        # Ключ для сортировки в зависимости от колонки
        if column == 0:  # Полная ссылка
            key = lambda x: getattr(x, 'full_reference', str(x))
        elif column == 1:  # Авторы
            def authors_key(x):
                if hasattr(x, 'authors'):
                    if isinstance(x.authors, list):
                        return ", ".join(x.authors)
                    return str(x.authors)
                return ""
            key = authors_key
        elif column == 2:  # Название
            key = lambda x: getattr(x, 'title', "")
        elif column == 3:  # Год
            # Используем числовое значение года для сортировки, если доступно
            def year_key(x):
                if hasattr(x, 'year_int') and isinstance(x.year_int, int):
                    return x.year_int
                year = getattr(x, 'year', "")
                try:
                    return int(year)
                except (ValueError, TypeError):
                    return 0
            key = year_key
        elif column == 4:  # Источник
            def source_key(x):
                if hasattr(x, 'journal') and x.journal:
                    return x.journal
                return getattr(x, 'publisher', "")
            key = source_key
        elif column == 5:  # Страницы
            key = lambda x: getattr(x, 'pages', "")
        elif column == 6:  # Тип
            key = lambda x: getattr(x, 'type', "")
        elif column == 7:  # ВАК
            key = lambda x: "Да" if getattr(x, 'is_vak', False) else "Нет"
        elif column == 8:  # РИНЦ
            key = lambda x: "Да" if getattr(x, 'is_rinc', False) else "Нет"
        elif column == 9:  # Язык
            key = lambda x: getattr(x, 'language', 'ru')
        elif column == 10:  # DOI/URL
            key = lambda x: getattr(x, 'doi', "") or getattr(x, 'url', "")
        else:
            key = lambda x: str(x)
        
        reverse = (order == Qt.DescendingOrder)
        self.items.sort(key=key, reverse=reverse)
        
        self._apply_filter()
        self.endResetModel()
    
    def get_original_index(self, filtered_index):
        """
        Получение индекса в исходном списке по индексу в отфильтрованном списке
        
        Args:
            filtered_index (int): Индекс в отфильтрованном списке
            
        Returns:
            int: Индекс в исходном списке или -1, если не найден
        """
        if 0 <= filtered_index < len(self.filtered_items):
            item = self.filtered_items[filtered_index]
            try:
                return self.items.index(item)
            except ValueError:
                return -1
        return -1

    def setData(self, index, value, role=Qt.EditRole):
        """
        Изменение данных в модели
        
        Args:
            index (QModelIndex): Индекс изменяемого элемента
            value: Новое значение
            role: Роль данных
            
        Returns:
            bool: True, если данные успешно изменены, False в противном случае
        """
        if not index.isValid() or not (0 <= index.row() < len(self.filtered_items)):
            return False
        
        # Получаем индекс в оригинальном списке
        original_index = self.get_original_index(index.row())
        if original_index < 0:
            return False
            
        item = self.items[original_index]
        col = index.column()
        
        # Обработка чекбоксов
        if role == Qt.CheckStateRole:
            if col == 7:  # ВАК
                item.is_vak = (value == Qt.Checked)
                self.dataChanged.emit(index, index)
                # Сигнал для уведомления контроллера
                if hasattr(self, 'parent') and hasattr(self.parent(), 'update_item_property_signal'):
                    self.parent().update_item_property_signal.emit(original_index, 'is_vak', item.is_vak)
                return True
            elif col == 8:  # РИНЦ
                item.is_rinc = (value == Qt.Checked)
                self.dataChanged.emit(index, index)
                # Сигнал для уведомления контроллера
                if hasattr(self, 'parent') and hasattr(self.parent(), 'update_item_property_signal'):
                    self.parent().update_item_property_signal.emit(original_index, 'is_rinc', item.is_rinc)
                return True
        
        return False
    
    def flags(self, index):
        """
        Определение флагов для элементов таблицы
        
        Args:
            index (QModelIndex): Индекс элемента
            
        Returns:
            Qt.ItemFlags: Флаги элемента
        """
        if not index.isValid():
            return Qt.NoItemFlags
            
        flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable
        
        # Добавляем флаг Qt.ItemIsUserCheckable для колонок с чекбоксами
        col = index.column()
        if col == 7 or col == 8:  # ВАК или РИНЦ
            flags |= Qt.ItemIsUserCheckable
            
        return flags

class InputTab(QWidget):
    """
    Вкладка для ввода и редактирования библиографических ссылок.
    """
    
    # Сигналы для взаимодействия с контроллером
    add_bibliography_signal = pyqtSignal(str, str)  # текст, тип формата
    add_structured_bibliography_signal = pyqtSignal(dict)  # словарь с структурированными данными
    edit_bibliography_signal = pyqtSignal(str, int, str)  # текст, индекс, тип формата
    update_item_property_signal = pyqtSignal(int, str, object)  # индекс, имя свойства, значение
    parse_text_signal = pyqtSignal(str)  # текст для распознавания
    remove_item_signal = pyqtSignal(int)  # индекс удаляемого элемента
    
    def __init__(self, parent=None):
        """Инициализация вкладки ввода и редактирования"""
        super().__init__(parent)
        
        # Создание компоновки
        self.create_layout()
        
        # Подключение обработчиков событий
        self.connect_events()
    
    def create_layout(self):
        """Создание компоновки вкладки"""
        main_layout = QVBoxLayout(self)
        
        # Создание разделителя для деления интерфейса на две части
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Левая часть - ввод текста и форма
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        # Группа для прямого ввода текста
        text_group = QGroupBox("Ввод текста библиографической ссылки")
        text_layout = QVBoxLayout()
        
        # Поле для ввода текста
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Введите библиографическую ссылку...")
        text_layout.addWidget(self.text_edit)
        
        # Выбор формата ссылки
        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("Формат:"))
        
        self.format_combo = QComboBox()
        self.format_combo.addItems(["Автоопределение", "ГОСТ", "IEEE"])
        format_layout.addWidget(self.format_combo)
        text_layout.addLayout(format_layout)
        
        # Кнопки для работы с текстом
        buttons_layout = QHBoxLayout()
        
        self.add_button = QPushButton("Добавить")
        buttons_layout.addWidget(self.add_button)
        
        self.parse_button = QPushButton("Распознать")
        buttons_layout.addWidget(self.parse_button)
        
        self.clear_button = QPushButton("Очистить")
        buttons_layout.addWidget(self.clear_button)
        
        text_layout.addLayout(buttons_layout)
        text_group.setLayout(text_layout)
        left_layout.addWidget(text_group)
        
        # Группа для ручного ввода через форму
        form_group = QGroupBox("Ручной ввод данных")
        form_layout = QFormLayout()
        
        # Тип источника
        self.source_type_combo = QComboBox()
        self.source_type_combo.addItems(["Книга", "Статья", "Веб-ресурс", "Другое"])
        form_layout.addRow("Тип источника:", self.source_type_combo)
        
        # Авторы
        self.authors_edit = QLineEdit()
        form_layout.addRow("Автор(ы):", self.authors_edit)
        
        # Название
        self.title_edit = QLineEdit()
        form_layout.addRow("Название:", self.title_edit)
        
        # Название
        self.subtitle_edit = QLineEdit()
        form_layout.addRow("Сведения:", self.subtitle_edit)

        # Год
        self.year_edit = QLineEdit()
        form_layout.addRow("Год:", self.year_edit)
        
        # Место издания (город)
        self.city_edit = QLineEdit()
        form_layout.addRow("Город:", self.city_edit)
        
        # Номер издания
        self.edition_edit = QLineEdit()
        form_layout.addRow("Номер издания:", self.edition_edit)

        # Издательство (для книг)
        self.publisher_edit = QLineEdit()
        form_layout.addRow("Издательство:", self.publisher_edit)
        
        # Журнал (для статей)
        self.journal_edit = QLineEdit()
        form_layout.addRow("Журнал/Сборник:", self.journal_edit)
        
        # Том, номер, страницы
        self.volume_edit = QLineEdit()
        form_layout.addRow("Том:", self.volume_edit)
        
        self.issue_edit = QLineEdit()
        form_layout.addRow("Номер:", self.issue_edit)
        
        self.pages_edit = QLineEdit()
        form_layout.addRow("Страницы:", self.pages_edit)
        
        # URL
        self.url_edit = QLineEdit()
        form_layout.addRow("URL:", self.url_edit)
        
        # DOI
        self.doi_edit = QLineEdit()
        form_layout.addRow("DOI:", self.doi_edit)
        
        # Язык
        language_layout = QHBoxLayout()
        self.language_group = QButtonGroup()
        
        self.ru_radio = QRadioButton("Русский")
        self.ru_radio.setChecked(True)
        self.language_group.addButton(self.ru_radio)
        language_layout.addWidget(self.ru_radio)
        
        self.en_radio = QRadioButton("Английский")
        self.language_group.addButton(self.en_radio)
        language_layout.addWidget(self.en_radio)
        
        form_layout.addRow("Язык:", language_layout)
        
        # Признак ВАК/РИНЦ
        vak_rinc_layout = QHBoxLayout()
        
        self.is_vak_check = QRadioButton("ВАК")
        vak_rinc_layout.addWidget(self.is_vak_check)
        
        self.is_rinc_check = QRadioButton("РИНЦ")
        vak_rinc_layout.addWidget(self.is_rinc_check)
        
        form_layout.addRow("Признак:", vak_rinc_layout)
        
        # Кнопки для работы с формой
        form_buttons_layout = QHBoxLayout()
        
        self.form_add_button = QPushButton("Добавить")
        form_buttons_layout.addWidget(self.form_add_button)
        
        self.form_clear_button = QPushButton("Очистить")
        form_buttons_layout.addWidget(self.form_clear_button)
        
        form_layout.addRow("", form_buttons_layout)
        
        form_group.setLayout(form_layout)
        left_layout.addWidget(form_group)
        
        # Правая часть - список библиографических ссылок
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        # Заголовок и поиск
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("Библиографический список:"))
        
        # Поле поиска
        search_layout = QHBoxLayout()
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Поиск по таблице...")
        search_layout.addWidget(self.search_edit)
        
        self.search_button = QPushButton("Поиск")
        search_layout.addWidget(self.search_button)
        
        self.clear_search_button = QPushButton("Сброс")
        search_layout.addWidget(self.clear_search_button)
        
        header_layout.addLayout(search_layout)
        right_layout.addLayout(header_layout)
        
        # Таблица библиографических ссылок
        self.bibliography_list = QTableView()
        self.bibliography_model = BibliographyTableModel()
        self.bibliography_model.parent = lambda: self  # Устанавливаем родительский виджет
        self.bibliography_list.setModel(self.bibliography_model)
        
        # Настройка отображения таблицы
        self.bibliography_list.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.bibliography_list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.bibliography_list.setAlternatingRowColors(True)
        self.bibliography_list.setSortingEnabled(True)
        
        # Настройка заголовков таблицы
        header = self.bibliography_list.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # Полная ссылка растягивается
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Авторы
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Название
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Год
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Источник
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Страницы
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)  # Тип
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)  # ВАК
        header.setSectionResizeMode(8, QHeaderView.ResizeToContents)  # РИНЦ
        header.setSectionResizeMode(9, QHeaderView.ResizeToContents)  # Язык
        header.setSectionResizeMode(10, QHeaderView.ResizeToContents)  # DOI/URL
        
        # Двойной клик для редактирования
        self.bibliography_list.doubleClicked.connect(self.on_edit_item)
        
        right_layout.addWidget(self.bibliography_list)
        
        # Кнопки для работы со списком
        list_buttons_layout = QHBoxLayout()
        
        self.edit_button = QPushButton("Редактировать")
        list_buttons_layout.addWidget(self.edit_button)
        
        self.remove_button = QPushButton("Удалить")
        list_buttons_layout.addWidget(self.remove_button)
        
        self.clear_list_button = QPushButton("Очистить список")
        list_buttons_layout.addWidget(self.clear_list_button)
        
        right_layout.addLayout(list_buttons_layout)
        
        # Добавление виджетов в разделитель
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        
        # Установка относительных размеров частей
        splitter.setSizes([500, 500])
    
    def connect_events(self):
        """Подключение обработчиков событий"""
        # Кнопки для работы с текстом
        self.add_button.clicked.connect(self.on_add_text)
        self.parse_button.clicked.connect(self.on_parse_text)
        self.clear_button.clicked.connect(self.on_clear_text)
        
        # Кнопки для работы с формой
        self.form_add_button.clicked.connect(self.on_add_form)
        self.form_clear_button.clicked.connect(self.on_clear_form)
        
        # Кнопки для работы со списком
        self.edit_button.clicked.connect(self.on_edit_item)
        self.remove_button.clicked.connect(self.on_remove_item)
        self.clear_list_button.clicked.connect(self.on_clear_list)
        
        # Поиск
        self.search_button.clicked.connect(self.on_search)
        self.clear_search_button.clicked.connect(self.on_clear_search)
        self.search_edit.returnPressed.connect(self.on_search)
        
        # Изменение типа источника
        self.source_type_combo.currentIndexChanged.connect(self.on_source_type_changed)
        
        # Обработка сортировки таблицы
        self.bibliography_list.horizontalHeader().sectionClicked.connect(self.on_header_clicked)
    
    def on_add_text(self):
        """Обработчик добавления текста библиографической ссылки"""
        text = self.text_edit.toPlainText().strip()
        if text:
            format_type = self.format_combo.currentText()
            self.add_bibliography_signal.emit(text, format_type)
            self.text_edit.clear()
    
    def on_parse_text(self):
        """Обработчик распознавания текста библиографической ссылки"""
        text = self.text_edit.toPlainText().strip()
        if text:
            self.parse_text_signal.emit(text)
    
    def on_clear_text(self):
        """Обработчик очистки текстового поля"""
        self.text_edit.clear()
    
    def on_add_form(self):
        """Обработчик добавления данных из формы"""
        # Получение данных из формы
        data = self.get_form_data()
        
        # Проверка наличия обязательных полей
        if not data['title']:
            return
        
        # Формирование текстовой строки полной библиографической ссылки
        full_reference = self.format_from_form_data(data)
        
        if full_reference:
            # Сохраняем полную ссылку в данных
            data['raw_text'] = full_reference
            data['full_reference'] = full_reference
            
            # Для дополнительной надежности создаем отдельную копию данных
            import copy
            send_data = copy.deepcopy(data)
            
            # Эмитируем сигнал со структурированными данными
            self.add_structured_bibliography_signal.emit(send_data)
            self.clear_form()
    
    def on_clear_form(self):
        """Обработчик очистки формы"""
        self.authors_edit.clear()
        self.title_edit.clear()
        self.year_edit.clear()
        self.subtitle_edit.clear()
        self.city_edit.clear()
        self.edition_edit.clear()
        self.publisher_edit.clear()
        self.journal_edit.clear()
        self.volume_edit.clear()
        self.issue_edit.clear()
        self.pages_edit.clear()
        self.url_edit.clear()
        self.doi_edit.clear()
        self.ru_radio.setChecked(True)
        self.is_vak_check.setChecked(False)
        self.is_rinc_check.setChecked(False)
    
    def on_edit_item(self):
        """Обработчик редактирования выбранного элемента таблицы"""
        selected_indexes = self.bibliography_list.selectionModel().selectedRows()
        if selected_indexes:
            filtered_row = selected_indexes[0].row()
            # Получаем индекс в оригинальном (нефильтрованном) списке
            original_row = self.bibliography_model.get_original_index(filtered_row)
            if original_row >= 0:
                item = self.bibliography_model.items[original_row]
                
                # Заполнение текстового поля для редактирования
                self.text_edit.setText(str(item))
                
                # Сохраняем текущее состояние кнопки и подключения
                self.add_button_text = self.add_button.text()
                
                # Временно изменяем кнопку "Добавить" на "Обновить"
                self.add_button.setText("Обновить")
                
                try:
                    # Попытка отключить сигнал, если он подключен
                    self.add_button.clicked.disconnect(self.on_add_text)
                except TypeError:
                    # Если сигнал не был подключен, просто продолжаем
                    pass
                
                # Подключаем новый обработчик
                self.add_button.clicked.connect(lambda: self.on_update_text(original_row))
    
    def on_update_text(self, row_index):
        """
        Обработчик обновления текста библиографической ссылки
        
        Args:
            row_index (int): Индекс строки обновляемого элемента
        """
        text = self.text_edit.toPlainText().strip()
        if text:
            format_type = self.format_combo.currentText()
            self.edit_bibliography_signal.emit(text, row_index, format_type)
            self.text_edit.clear()
            
            # Восстановление исходного состояния кнопки
            self.add_button.setText(self.add_button_text)
            
            try:
                # Пытаемся отключить текущий сигнал
                self.add_button.clicked.disconnect()
            except TypeError:
                # Если возникла ошибка, игнорируем ее
                pass
                
            # Подключаем обратно исходный обработчик
            self.add_button.clicked.connect(self.on_add_text)
    
    def on_remove_item(self):
        """Обработчик удаления выбранного элемента таблицы"""
        selected_indexes = self.bibliography_list.selectionModel().selectedRows()
        if selected_indexes:
            filtered_row = selected_indexes[0].row()
            # Получаем индекс в оригинальном (нефильтрованном) списке
            original_row = self.bibliography_model.get_original_index(filtered_row)
            if original_row >= 0:
                self.remove_item_signal.emit(original_row)
    
    def on_clear_list(self):
        """Обработчик очистки списка библиографических ссылок"""
        self.bibliography_model.setItems([])
    
    def on_source_type_changed(self, index):
        """
        Обработчик изменения типа источника
        
        Args:
            index (int): Индекс выбранного типа источника
        """
        # Изменение видимости полей в зависимости от типа источника
        is_book = index == 0  # "Книга"
        is_article = index == 1  # "Статья"
        is_web = index == 2  # "Веб-ресурс"
        
        # Поля для книг
        self.edition_edit.setEnabled(is_book)
        self.city_edit.setEnabled(is_book or is_article)
        self.publisher_edit.setEnabled(is_book or is_article)
        
        # Поля для статей
        self.journal_edit.setEnabled(is_article)
        self.volume_edit.setEnabled(is_article)
        self.issue_edit.setEnabled(is_article)
        self.pages_edit.setEnabled(is_article or is_book)
        
        # Поля для веб-ресурсов
        self.url_edit.setEnabled(is_web or is_article)
    
    def get_form_data(self):
        """
        Получение данных из формы
        
        Returns:
            dict: Словарь с данными из формы
        """
        # Получение типа источника и преобразование в стандартное значение
        source_type_text = self.source_type_combo.currentText()
        type_mapping = {
            "Книга": "book",
            "Статья": "article",
            "Веб-ресурс": "web",
            "Другое": "other"
        }
        source_type = type_mapping.get(source_type_text, "other")
        
        # Обработка авторов - разделение строки на список авторов
        authors_text = self.authors_edit.text().strip()
        authors_list = [author.strip() for author in authors_text.split(",") if author.strip()]
        
        # Обработка страниц
        pages = self.pages_edit.text().strip()
        
        # Проверка признаков ВАК и РИНЦ
        is_vak = self.is_vak_check.isChecked()
        is_rinc = self.is_rinc_check.isChecked()
        
        # Определение языка
        language = 'en' if self.en_radio.isChecked() else 'ru'
        
        # Основные данные
        data = {
            'type': source_type,
            'authors': authors_list,
            'title': self.title_edit.text().strip(),
            'subtitle': self.subtitle_edit.text().strip(),
            'year': self.year_edit.text().strip(),
            'city': self.city_edit.text().strip(),
            'edition': self.edition_edit.text().strip(),
            'publisher': self.publisher_edit.text().strip(),
            'journal': self.journal_edit.text().strip(),
            'volume': self.volume_edit.text().strip(),
            'issue': self.issue_edit.text().strip(),
            'pages': pages,
            'url': self.url_edit.text().strip(),
            'doi': self.doi_edit.text().strip(),
            'language': language,
            'is_vak': is_vak,
            'is_rinc': is_rinc
        }
        
        # Добавление дополнительных вычисляемых полей
        year_int = 0
        if data['year'] and data['year'].isdigit():
            year_int = int(data['year'])
            
        data['year_int'] = year_int
        data['has_english'] = (language == 'en')
        
        return data
    
    def format_from_form_data(self, data):
        """
        Форматирование библиографической ссылки из данных формы
        
        Args:
            data (dict): Словарь с данными из формы
            
        Returns:
            str: Отформатированная библиографическая ссылка
        """
        if not data['title']:
            return ""
        
        # Форматирование в зависимости от типа источника
        if data['type'] == "book" or data['type'] == "Книга":
            return self._format_book(data)
        elif data['type'] == "article" or data['type'] == "Статья":
            return self._format_article(data)
        elif data['type'] == "web" or data['type'] == "Веб-ресурс":
            return self._format_web_resource(data)
        else:
            return self._format_generic(data)
    
    def _format_book(self, data):
        """Форматирование книги по ГОСТ"""
        result = ""
        
        # Добавление авторов
        if data['authors']:
            result += ", ".join(data['authors'])
            result += ". "
        
        # Добавление названия
        result += data['title']
        
        # Добавление подзаголовка
        if data['subtitle']:
            result += " : " + data['subtitle']
        
        # Добавление сведений об ответственности (авторы после косой черты)
        if data['authors']:
            result += " / " + ", ".join(data['authors'])
        result += ". "
        
        # Добавление сведений об издании
        if data['edition']:
            result += "— " + data['edition'] + "-е изд. "
        
        # Добавление места издания и издательства
        if data['city'] or data['publisher']:
            result += "— "
            if data['city']:
                result += data['city']
                if data['publisher']:
                    result += " : "
            if data['publisher']:
                result += data['publisher']
            result += ", "
        
        # Добавление года
        if data['year']:
            result += data['year']
        result += ". "
        
        # Добавление количества страниц
        if data['pages']:
            result += "— " + data['pages'] + " с."
        
        # Добавление DOI
        if data['doi']:
            result += " DOI: " + data['doi'] + "."
        
        return result.strip()
    
    def _format_article(self, data):
        """Форматирование статьи по ГОСТ"""
        result = ""
        
        # Добавление авторов
        if data['authors']:
            result += ", ".join(data['authors'])
            result += ". "
        
        # Добавление названия
        result += data['title']
        
        # Добавление подзаголовка
        if data['subtitle']:
            result += " : " + data['subtitle']
        
        # Добавление сведений об ответственности
        if data['authors']:
            result += " / " + ", ".join(data['authors'])
        result += ". "
        
        # Добавление названия журнала
        if data['journal']:
            result += "// " + data['journal'] + ". "
        
        # Добавление года
        if data['year']:
            result += "— " + data['year'] + ". "
        
        # Добавление тома
        if data['volume']:
            result += "— Т. " + data['volume']
            if data['issue']:
                result += ", "
            else:
                result += ". "
        
        # Добавление номера
        if data['issue']:
            result += "— № " + data['issue'] + ". "
        
        # Добавление страниц
        if data['pages']:
            result += "— С. " + data['pages'] + ". "
        
        # Добавление DOI
        if data['doi']:
            result += "DOI: " + data['doi'] + ". "
        
        return result.strip()
    
    def _format_web_resource(self, data):
        """Форматирование веб-ресурса по ГОСТ"""
        result = ""
        
        # Добавление авторов
        if data['authors']:
            result += ", ".join(data['authors'])
            result += ". "
        
        # Добавление названия
        result += data['title']
        
        # Добавление подзаголовка
        if data['subtitle']:
            result += " : " + data['subtitle']
        
        result += " [Электронный ресурс]. "
        
        # Добавление сведений об ответственности
        if data['authors']:
            result += "/ " + ", ".join(data['authors']) + ". "
        
        # Добавление места издания и издательства
        if data['city'] or data['publisher']:
            if data['city']:
                result += data['city']
                if data['publisher']:
                    result += " : "
            if data['publisher']:
                result += data['publisher']
            result += ", "
        
        # Добавление года
        if data['year']:
            result += data['year'] + ". "
        
        # Добавление URL
        if data['url']:
            result += "— URL: " + data['url']
            # Добавление даты обращения (текущая дата)
            current_date = datetime.now().strftime("%d.%m.%Y")
            result += f" (дата обращения: {current_date}). "
        
        # Добавление DOI
        if data['doi']:
            result += "DOI: " + data['doi'] + ". "
        
        return result.strip()
    
    def _format_generic(self, data):
        """Общее форматирование для других типов источников"""
        result = ""
        
        # Добавление авторов
        if data['authors']:
            result += ", ".join(data['authors'])
            result += ". "
        
        # Добавление названия
        result += data['title']
        
        # Добавление подзаголовка
        if data['subtitle']:
            result += " : " + data['subtitle']
        result += ". "
        
        # Добавление города и издательства
        if data['city'] or data['publisher']:
            if data['city']:
                result += data['city']
                if data['publisher']:
                    result += " : "
            if data['publisher']:
                result += data['publisher']
            
            if data['year']:
                result += ", "
        
        # Добавление года
        if data['year']:
            result += data['year']
        result += ". "
        
        # Добавление количества страниц
        if data['pages']:
            result += data['pages'] + " с. "
        
        # Добавление DOI
        if data['doi']:
            result += "DOI: " + data['doi'] + ". "
        
        # Добавление URL
        if data['url']:
            result += "URL: " + data['url'] + ". "
        
        return result.strip()
    
    def clear_form(self):
        """Очистка формы ввода"""
        self.authors_edit.clear()
        self.title_edit.clear()
        self.subtitle_edit.clear()
        self.year_edit.clear()
        self.city_edit.clear()
        self.edition_edit.clear()
        self.publisher_edit.clear()
        self.journal_edit.clear()
        self.volume_edit.clear()
        self.issue_edit.clear()
        self.pages_edit.clear()
        self.url_edit.clear()
        self.doi_edit.clear()
        self.ru_radio.setChecked(True)
        self.is_vak_check.setChecked(False)
        self.is_rinc_check.setChecked(False)
    
    def update_bibliography_list(self, items):
        """
        Обновление списка библиографических ссылок
        
        Args:
            items (list): Список библиографических ссылок
        """
        self.bibliography_model.setItems(items)
    
    def fill_form_with_data(self, data):
        """
        Заполнение формы данными
        
        Args:
            data (dict): Словарь с данными для заполнения формы
        """
        # Установка типа источника
        source_type_map = {"book": 0, "article": 1, "web": 2, "other": 3}
        index = source_type_map.get(data.get('type', 'book'), 0)
        self.source_type_combo.setCurrentIndex(index)
        
        # Заполнение полей
        self.authors_edit.setText(", ".join(data.get('authors', [])))
        self.title_edit.setText(data.get('title', ''))
        self.subtitle_edit.setText(data.get('subtitle', ''))
        self.year_edit.setText(data.get('year', ''))
        self.city_edit.setText(data.get('city', ''))
        self.edition_edit.setText(data.get('edition', ''))
        self.publisher_edit.setText(data.get('publisher', ''))
        self.journal_edit.setText(data.get('journal', ''))
        self.volume_edit.setText(data.get('volume', ''))
        self.issue_edit.setText(data.get('issue', ''))
        self.pages_edit.setText(data.get('pages', ''))
        self.url_edit.setText(data.get('url', ''))
        self.doi_edit.setText(data.get('doi', ''))
        
        # Установка языка
        if data.get('language', 'ru') == 'en':
            self.en_radio.setChecked(True)
        else:
            self.ru_radio.setChecked(True)
        
        # Установка признаков ВАК/РИНЦ
        self.is_vak_check.setChecked(data.get('is_vak', False))
        self.is_rinc_check.setChecked(data.get('is_rinc', False))
    
    def on_search(self):
        """Обработчик поиска по таблице"""
        search_text = self.search_edit.text().strip()
        self.bibliography_model.set_filter(search_text)
    
    def on_clear_search(self):
        """Обработчик очистки поискового запроса"""
        self.search_edit.clear()
        self.bibliography_model.set_filter("")
    
    def on_header_clicked(self, logical_index):
        """
        Обработчик клика по заголовку таблицы для сортировки
        
        Args:
            logical_index (int): Индекс колонки
        """
        # Получаем порядок сортировки
        order = self.bibliography_list.horizontalHeader().sortIndicatorOrder()
        # Выполняем сортировку
        self.bibliography_model.sort(logical_index, order) 