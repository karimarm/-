#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QTextEdit, QPushButton, QComboBox, QGridLayout, 
    QGroupBox, QListWidget, QListWidgetItem, QSplitter, 
    QFormLayout, QRadioButton, QButtonGroup
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from datetime import datetime

class InputTab(QWidget):
    """
    Вкладка для ввода и редактирования библиографических ссылок.
    """
    
    # Сигналы для взаимодействия с контроллером
    add_bibliography_signal = pyqtSignal(str, str)  # текст, тип формата
    edit_bibliography_signal = pyqtSignal(str, int, str)  # текст, индекс, тип формата
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
        
        right_layout.addWidget(QLabel("Библиографический список:"))
        
        # Список библиографических ссылок
        self.bibliography_list = QListWidget()
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
        
        # Изменение типа источника
        self.source_type_combo.currentIndexChanged.connect(self.on_source_type_changed)
    
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
        # Формирование строки библиографической ссылки из данных формы
        data = self.get_form_data()
        text = self.format_from_form_data(data)
        
        if text:
            format_type = "GOST"  # Форма всегда формирует в формате ГОСТ
            self.add_bibliography_signal.emit(text, format_type)
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
        """Обработчик редактирования выбранного элемента списка"""
        selected_items = self.bibliography_list.selectedItems()
        if selected_items:
            item = selected_items[0]
            text = item.text()
            index = self.bibliography_list.row(item)
            
            # Заполнение текстового поля для редактирования
            self.text_edit.setText(text)
            
            # Временное изменение кнопки "Добавить" на "Обновить"
            self.add_button.setText("Обновить")
            self.add_button.clicked.disconnect(self.on_add_text)
            self.add_button.clicked.connect(lambda: self.on_update_text(index))
    
    def on_update_text(self, index):
        """
        Обработчик обновления текста библиографической ссылки
        
        Args:
            index (int): Индекс обновляемого элемента
        """
        text = self.text_edit.toPlainText().strip()
        if text:
            format_type = self.format_combo.currentText()
            self.edit_bibliography_signal.emit(text, index, format_type)
            self.text_edit.clear()
            
            # Возвращение кнопки "Обновить" в состояние "Добавить"
            self.add_button.setText("Добавить")
            self.add_button.clicked.disconnect()
            self.add_button.clicked.connect(self.on_add_text)
    
    def on_remove_item(self):
        """Обработчик удаления выбранного элемента списка"""
        selected_items = self.bibliography_list.selectedItems()
        if selected_items:
            item = selected_items[0]
            index = self.bibliography_list.row(item)
            self.remove_item_signal.emit(index)
    
    def on_clear_list(self):
        """Обработчик очистки списка библиографических ссылок"""
        self.bibliography_list.clear()
    
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
        data = {
            'type': self.source_type_combo.currentText(),
            'authors': self.authors_edit.text(),
            'title': self.title_edit.text(),
            'subtitle': self.subtitle_edit.text(),
            'year': self.year_edit.text(),
            'city': self.city_edit.text(),
            'edition': self.edition_edit.text(),
            'publisher': self.publisher_edit.text(),
            'journal': self.journal_edit.text(),
            'volume': self.volume_edit.text(),
            'issue': self.issue_edit.text(),
            'pages': self.pages_edit.text(),
            'url': self.url_edit.text(),
            'doi': self.doi_edit.text(),
            'language': 'ru' if self.ru_radio.isChecked() else 'en',
            'is_vak': self.is_vak_check.isChecked(),
            'is_rinc': self.is_rinc_check.isChecked()
        }
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
        
        result = ""
        
        # Добавление авторов
        if data['authors']:
            result += data['authors']
            result += " "
        
        # Добавление названия
        result += data['title']
        
        # Добавление подзаголовка
        if data['subtitle']:
            result += " : " + data['subtitle']
        
        # В зависимости от типа источника
        if data['type'] == "Книга":
            # Добавление сведений об ответственности (авторы после косой черты)
            if data['authors']:
                result += " / " + data['authors']
            result += " "
            
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
                if data['year']:
                    result += ", "
            
            # Добавление года
            if data['year']:
                result += data['year']
            result += ". "
            
            # Добавление количества страниц
            if data['pages']:
                result += "— " + data['pages'] + " с. "
            
        elif data['type'] == "Статья":
            # Добавление сведений об ответственности
            if data['authors']:
                result += " / " + data['authors']
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
                result += "№ " + data['issue'] + ". "
            
            # Добавление страниц
            if data['pages']:
                result += "— С. " + data['pages'] + ". "
            
        elif data['type'] == "Веб-ресурс":
            result += " [Электронный ресурс]. "
            
            # Добавление года
            if data['year']:
                result += "— " + data['year'] + ". "
            
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
        self.bibliography_list.clear()
        for item in items:
            self.bibliography_list.addItem(QListWidgetItem(str(item)))
    
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