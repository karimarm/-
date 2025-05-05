#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, 
    QPushButton, QComboBox, QGroupBox, QSplitter, QMessageBox,
    QRadioButton, QButtonGroup, QFileDialog
)
from PyQt5.QtCore import Qt, pyqtSignal

class ConvertTab(QWidget):
    """
    Вкладка для преобразования библиографических ссылок между форматами.
    """
    
    # Сигналы
    convert_signal = pyqtSignal(str, str, str)  # текст, исходный формат, целевой формат
    convert_batch_signal = pyqtSignal(list, str, str)  # список текстов, исходный формат, целевой формат
    
    def __init__(self, parent=None):
        """Инициализация вкладки преобразования"""
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
        
        # Верхняя часть - преобразование одиночной ссылки
        upper_widget = QWidget()
        upper_layout = QVBoxLayout(upper_widget)
        
        convert_group = QGroupBox("Преобразование формата отдельной ссылки")
        convert_layout = QVBoxLayout()
        
        # Выбор исходного и целевого форматов
        formats_layout = QHBoxLayout()
        
        # Исходный формат
        source_layout = QVBoxLayout()
        source_layout.addWidget(QLabel("Исходный формат:"))
        self.source_combo = QComboBox()
        self.source_combo.addItems(["ГОСТ", "IEEE"])
        source_layout.addWidget(self.source_combo)
        formats_layout.addLayout(source_layout)
        
        # Кнопка обмена форматов
        self.swap_button = QPushButton("⇄")
        self.swap_button.setToolTip("Поменять форматы местами")
        self.swap_button.setFixedWidth(40)
        formats_layout.addWidget(self.swap_button)
        
        # Целевой формат
        target_layout = QVBoxLayout()
        target_layout.addWidget(QLabel("Целевой формат:"))
        self.target_combo = QComboBox()
        self.target_combo.addItems(["IEEE", "ГОСТ"])
        target_layout.addWidget(self.target_combo)
        formats_layout.addLayout(target_layout)
        
        convert_layout.addLayout(formats_layout)
        
        # Текстовые поля для ввода и результата
        input_layout = QVBoxLayout()
        input_layout.addWidget(QLabel("Введите библиографическую ссылку:"))
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Вставьте текст библиографической ссылки для преобразования...")
        input_layout.addWidget(self.input_text)
        
        # Кнопка преобразования
        self.convert_button = QPushButton("Преобразовать")
        input_layout.addWidget(self.convert_button)
        
        convert_layout.addLayout(input_layout)
        
        # Результат преобразования
        result_layout = QVBoxLayout()
        result_layout.addWidget(QLabel("Результат преобразования:"))
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        result_layout.addWidget(self.result_text)
        
        # Кнопка копирования результата
        self.copy_button = QPushButton("Копировать результат")
        result_layout.addWidget(self.copy_button)
        
        convert_layout.addLayout(result_layout)
        
        convert_group.setLayout(convert_layout)
        upper_layout.addWidget(convert_group)
        
        # Нижняя часть - пакетное преобразование
        lower_widget = QWidget()
        lower_layout = QVBoxLayout(lower_widget)
        
        batch_group = QGroupBox("Пакетное преобразование списка ссылок")
        batch_layout = QVBoxLayout()
        
        # Выбор форматов для пакетного преобразования
        batch_formats_layout = QHBoxLayout()
        
        # Исходный формат
        batch_source_layout = QVBoxLayout()
        batch_source_layout.addWidget(QLabel("Исходный формат:"))
        self.batch_source_combo = QComboBox()
        self.batch_source_combo.addItems(["ГОСТ", "IEEE"])
        batch_source_layout.addWidget(self.batch_source_combo)
        batch_formats_layout.addLayout(batch_source_layout)
        
        # Целевой формат
        batch_target_layout = QVBoxLayout()
        batch_target_layout.addWidget(QLabel("Целевой формат:"))
        self.batch_target_combo = QComboBox()
        self.batch_target_combo.addItems(["IEEE", "ГОСТ"])
        batch_target_layout.addWidget(self.batch_target_combo)
        batch_formats_layout.addLayout(batch_target_layout)
        
        batch_layout.addLayout(batch_formats_layout)
        
        # Кнопки для пакетного преобразования
        batch_buttons_layout = QHBoxLayout()
        
        self.convert_all_button = QPushButton("Преобразовать весь библиографический список")
        batch_buttons_layout.addWidget(self.convert_all_button)
        
        self.convert_selected_button = QPushButton("Преобразовать выбранные записи")
        batch_buttons_layout.addWidget(self.convert_selected_button)
        
        batch_layout.addLayout(batch_buttons_layout)
        
        # Экспорт результатов
        export_layout = QHBoxLayout()
        export_layout.addWidget(QLabel("Экспорт результатов:"))
        
        self.export_txt_button = QPushButton("TXT")
        export_layout.addWidget(self.export_txt_button)
        
        self.export_rtf_button = QPushButton("RTF")
        export_layout.addWidget(self.export_rtf_button)
        
        self.export_html_button = QPushButton("HTML")
        export_layout.addWidget(self.export_html_button)
        
        batch_layout.addLayout(export_layout)
        
        # Результаты пакетного преобразования
        batch_layout.addWidget(QLabel("Результаты пакетного преобразования:"))
        self.batch_result_text = QTextEdit()
        self.batch_result_text.setReadOnly(True)
        batch_layout.addWidget(self.batch_result_text)
        
        batch_group.setLayout(batch_layout)
        lower_layout.addWidget(batch_group)
        
        # Добавление виджетов в разделитель
        splitter.addWidget(upper_widget)
        splitter.addWidget(lower_widget)
        
        # Установка относительных размеров частей
        splitter.setSizes([1, 1])
    
    def connect_events(self):
        """Подключение обработчиков событий"""
        # Кнопки для одиночного преобразования
        self.convert_button.clicked.connect(self.on_convert)
        self.copy_button.clicked.connect(self.on_copy_result)
        self.swap_button.clicked.connect(self.on_swap_formats)
        
        # Кнопки для пакетного преобразования
        self.convert_all_button.clicked.connect(self.on_convert_all)
        self.convert_selected_button.clicked.connect(self.on_convert_selected)
        
        # Кнопки экспорта
        self.export_txt_button.clicked.connect(lambda: self.on_export('txt'))
        self.export_rtf_button.clicked.connect(lambda: self.on_export('rtf'))
        self.export_html_button.clicked.connect(lambda: self.on_export('html'))
    
    def on_convert(self):
        """Обработчик преобразования отдельной ссылки"""
        # Получение исходного текста
        source_text = self.input_text.toPlainText().strip()
        
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
    
    def on_copy_result(self):
        """Обработчик копирования результата в буфер обмена"""
        result = self.result_text.toPlainText().strip()
        
        if result:
            clipboard = QApplication.clipboard()
            clipboard.setText(result)
            
            QMessageBox.information(
                self,
                "Копирование",
                "Результат скопирован в буфер обмена."
            )
    
    def on_swap_formats(self):
        """Обработчик обмена форматов местами"""
        # Сохранение текущих индексов
        source_index = self.source_combo.currentIndex()
        target_index = self.target_combo.currentIndex()
        
        # Обмен индексами
        self.source_combo.setCurrentIndex(target_index)
        self.target_combo.setCurrentIndex(source_index)
    
    def on_convert_all(self):
        """Обработчик пакетного преобразования всего списка"""
        # Получение форматов
        source_format = self.batch_source_combo.currentText()
        target_format = self.batch_target_combo.currentText()
        
        # Отправка сигнала на преобразование всего списка
        # Пустой список означает преобразование всех записей
        self.convert_batch_signal.emit([], source_format, target_format)
    
    def on_convert_selected(self):
        """Обработчик преобразования выбранных записей"""
        # Получение форматов
        source_format = self.batch_source_combo.currentText()
        target_format = self.batch_target_combo.currentText()
        
        # Здесь должна быть логика получения списка выбранных записей
        # из основного интерфейса
        selected_indices = []  # Заглушка, в реальном приложении должны быть индексы
        
        if not selected_indices:
            QMessageBox.warning(
                self,
                "Предупреждение",
                "Выберите записи для преобразования."
            )
            return
        
        # Отправка сигнала на преобразование выбранных записей
        self.convert_batch_signal.emit(selected_indices, source_format, target_format)
    
    def on_export(self, format_type):
        """
        Обработчик экспорта результатов
        
        Args:
            format_type (str): Тип формата (txt, rtf, html)
        """
        # Получение текста результатов
        result_text = self.batch_result_text.toPlainText().strip()
        
        if not result_text:
            QMessageBox.warning(
                self,
                "Предупреждение",
                "Нет результатов для экспорта."
            )
            return
        
        # Определение типа файла для диалога сохранения
        if format_type == 'txt':
            file_filter = "Text Files (*.txt)"
            default_ext = "txt"
        elif format_type == 'rtf':
            file_filter = "RTF Files (*.rtf)"
            default_ext = "rtf"
        elif format_type == 'html':
            file_filter = "HTML Files (*.html)"
            default_ext = "html"
        else:
            file_filter = "All Files (*)"
            default_ext = "txt"
        
        # Диалог выбора файла для сохранения
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить результаты",
            f"bibliography_converted.{default_ext}",
            file_filter
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(result_text)
                
                QMessageBox.information(
                    self,
                    "Экспорт",
                    f"Результаты успешно сохранены в файл: {file_path}"
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Ошибка",
                    f"Ошибка при сохранении файла: {str(e)}"
                )
    
    def set_result_text(self, text):
        """Установка текста результата преобразования"""
        self.result_text.setText(text)
    
    def set_batch_result_text(self, text):
        """Установка текста результатов пакетного преобразования"""
        self.batch_result_text.setText(text) 