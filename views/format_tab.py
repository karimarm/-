#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, 
    QPushButton, QComboBox, QRadioButton, QButtonGroup,
    QGroupBox, QSplitter, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

class FormatTab(QWidget):
    """
    Вкладка для форматирования библиографических ссылок.
    """
    
    # Сигналы для взаимодействия с контроллером
    convert_signal = pyqtSignal(str, str, str)  # текст, исходный формат, целевой формат
    batch_convert_signal = pyqtSignal(str, str)  # исходный формат, целевой формат
    export_signal = pyqtSignal(str)  # путь к файлу
    
    def __init__(self, parent=None):
        """Инициализация вкладки форматирования"""
        super().__init__(parent)
        
        # Создание компоновки
        self.create_layout()
        
        # Подключение обработчиков событий
        self.connect_events()
    
    def create_layout(self):
        """Создание компоновки вкладки"""
        main_layout = QVBoxLayout(self)
        
        # Создание разделителя для верхней и нижней частей
        splitter = QSplitter(Qt.Vertical)
        main_layout.addWidget(splitter)
        
        # Верхняя часть - преобразование отдельной ссылки
        upper_widget = QWidget()
        upper_layout = QVBoxLayout(upper_widget)
        
        upper_group = QGroupBox("Преобразование отдельной ссылки")
        upper_inner_layout = QVBoxLayout()
        
        # Настройки преобразования
        settings_layout = QHBoxLayout()
        
        # Исходный формат
        source_layout = QVBoxLayout()
        source_layout.addWidget(QLabel("Исходный формат:"))
        self.source_combo = QComboBox()
        self.source_combo.addItems(["Автоопределение", "ГОСТ", "IEEE"])
        source_layout.addWidget(self.source_combo)
        settings_layout.addLayout(source_layout)
        
        # Целевой формат
        target_layout = QVBoxLayout()
        target_layout.addWidget(QLabel("Целевой формат:"))
        self.target_combo = QComboBox()
        self.target_combo.addItems(["ГОСТ", "IEEE"])
        target_layout.addWidget(self.target_combo)
        settings_layout.addLayout(target_layout)
        
        upper_inner_layout.addLayout(settings_layout)
        
        # Поле для ввода исходного текста
        upper_inner_layout.addWidget(QLabel("Исходный текст:"))
        self.source_text = QTextEdit()
        self.source_text.setPlaceholderText("Введите библиографическую ссылку для преобразования...")
        upper_inner_layout.addWidget(self.source_text)
        
        # Кнопка преобразования
        self.convert_button = QPushButton("Преобразовать")
        upper_inner_layout.addWidget(self.convert_button)
        
        # Поле для вывода результата
        upper_inner_layout.addWidget(QLabel("Результат преобразования:"))
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        upper_inner_layout.addWidget(self.result_text)
        
        upper_group.setLayout(upper_inner_layout)
        upper_layout.addWidget(upper_group)
        
        # Нижняя часть - пакетное преобразование
        lower_widget = QWidget()
        lower_layout = QVBoxLayout(lower_widget)
        
        lower_group = QGroupBox("Пакетное преобразование списка ссылок")
        lower_inner_layout = QVBoxLayout()
        
        # Настройки пакетного преобразования
        batch_settings_layout = QHBoxLayout()
        
        # Исходный формат для пакетного преобразования
        batch_source_layout = QVBoxLayout()
        batch_source_layout.addWidget(QLabel("Исходный формат:"))
        self.batch_source_combo = QComboBox()
        self.batch_source_combo.addItems(["Автоопределение", "ГОСТ", "IEEE"])
        batch_source_layout.addWidget(self.batch_source_combo)
        batch_settings_layout.addLayout(batch_source_layout)
        
        # Целевой формат для пакетного преобразования
        batch_target_layout = QVBoxLayout()
        batch_target_layout.addWidget(QLabel("Целевой формат:"))
        self.batch_target_combo = QComboBox()
        self.batch_target_combo.addItems(["ГОСТ", "IEEE"])
        batch_target_layout.addWidget(self.batch_target_combo)
        batch_settings_layout.addLayout(batch_target_layout)
        
        lower_inner_layout.addLayout(batch_settings_layout)
        
        # Кнопки для пакетного преобразования
        batch_buttons_layout = QHBoxLayout()
        
        self.batch_convert_button = QPushButton("Преобразовать все записи")
        batch_buttons_layout.addWidget(self.batch_convert_button)
        
        self.export_button = QPushButton("Экспорт результатов")
        batch_buttons_layout.addWidget(self.export_button)
        
        lower_inner_layout.addLayout(batch_buttons_layout)
        
        # Поле для вывода результатов пакетного преобразования
        lower_inner_layout.addWidget(QLabel("Результаты пакетного преобразования:"))
        self.batch_result_text = QTextEdit()
        self.batch_result_text.setReadOnly(True)
        lower_inner_layout.addWidget(self.batch_result_text)
        
        lower_group.setLayout(lower_inner_layout)
        lower_layout.addWidget(lower_group)
        
        # Добавление виджетов в разделитель
        splitter.addWidget(upper_widget)
        splitter.addWidget(lower_widget)
        
        # Установка относительных размеров частей
        splitter.setSizes([500, 500])
    
    def connect_events(self):
        """Подключение обработчиков событий"""
        # Кнопка преобразования отдельной ссылки
        self.convert_button.clicked.connect(self.on_convert)
        
        # Кнопки пакетного преобразования
        self.batch_convert_button.clicked.connect(self.on_batch_convert)
        self.export_button.clicked.connect(self.on_export)
    
    def on_convert(self):
        """Обработчик преобразования отдельной ссылки"""
        # Получение исходного текста
        source_text = self.source_text.toPlainText().strip()
        
        if not source_text:
            QMessageBox.warning(
                self,
                "Предупреждение",
                "Введите текст для преобразования."
            )
            return
        
        # Получение форматов
        source_format = self.source_combo.currentText()
        target_format = self.target_combo.currentText()
        
        # Отправка сигнала на преобразование
        self.convert_signal.emit(source_text, source_format, target_format)
    
    def on_batch_convert(self):
        """Обработчик пакетного преобразования списка ссылок"""
        # Получение форматов
        source_format = self.batch_source_combo.currentText()
        target_format = self.batch_target_combo.currentText()
        
        # Отправка сигнала на пакетное преобразование
        self.batch_convert_signal.emit(source_format, target_format)
    
    def on_export(self):
        """Обработчик экспорта результатов"""
        # Получение текста результатов
        result_text = self.batch_result_text.toPlainText().strip()
        
        if not result_text:
            QMessageBox.warning(
                self,
                "Предупреждение",
                "Нет результатов для экспорта."
            )
            return
        
        # Диалог выбора файла для сохранения
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить результаты",
            "",
            "Text Files (*.txt);;All Files (*)"
        )
        
        if file_path:
            # Отправка сигнала на экспорт
            self.export_signal.emit(file_path)
    
    def set_result_text(self, text):
        """Установка текста результата преобразования"""
        self.result_text.setText(text)
    
    def set_batch_result_text(self, text):
        """Установка текста результатов пакетного преобразования"""
        self.batch_result_text.setText(text) 