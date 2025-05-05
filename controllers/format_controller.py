#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMessageBox
from utils.reference_formatter import ReferenceFormatter

class FormatController:
    """
    Контроллер для модуля форматирования библиографических ссылок.
    """
    
    def __init__(self, format_tab, bibliography_model):
        """
        Инициализация контроллера форматирования
        
        Args:
            format_tab: Вкладка форматирования (представление)
            bibliography_model: Модель библиографии (список записей)
        """
        self.format_tab = format_tab
        self.bibliography_model = bibliography_model
        
        # Подключение сигналов
        self.connect_signals()
    
    def connect_signals(self):
        """Подключение сигналов к обработчикам"""
        # Сигналы от вкладки форматирования
        self.format_tab.convert_signal.connect(self.on_convert)
        self.format_tab.batch_convert_signal.connect(self.on_batch_convert)
        self.format_tab.export_signal.connect(self.on_export)
    
    def on_convert(self, source_text, source_format, target_format):
        """
        Обработчик преобразования отдельной ссылки
        
        Args:
            source_text (str): Исходный текст ссылки
            source_format (str): Исходный формат
            target_format (str): Целевой формат
        """
        try:
            # Преобразование ссылки
            result = ReferenceFormatter.convert(source_text, source_format, target_format)
            
            # Обновление представления
            self.format_tab.set_result_text(result)
            
        except Exception as e:
            QMessageBox.critical(
                self.format_tab,
                "Ошибка",
                f"Ошибка при преобразовании ссылки: {str(e)}"
            )
    
    def on_batch_convert(self, source_format, target_format):
        """
        Обработчик пакетного преобразования списка ссылок
        
        Args:
            source_format (str): Исходный формат
            target_format (str): Целевой формат
        """
        items = self.bibliography_model.items
        
        if not items:
            QMessageBox.warning(
                self.format_tab,
                "Предупреждение",
                "Список библиографических записей пуст."
            )
            return
        
        try:
            # Преобразование каждой записи в целевой формат
            results = []
            for i, item in enumerate(items):
                formatted = ReferenceFormatter.format(item, target_format)
                results.append(f"{i+1}. {formatted}")
            
            # Обновление представления
            self.format_tab.set_batch_result_text("\n\n".join(results))
            
        except Exception as e:
            QMessageBox.critical(
                self.format_tab,
                "Ошибка",
                f"Ошибка при пакетном преобразовании: {str(e)}"
            )
    
    def on_export(self, file_path):
        """
        Обработчик экспорта результатов
        
        Args:
            file_path (str): Путь к файлу для сохранения
        """
        try:
            result_text = self.format_tab.batch_result_text.toPlainText()
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(result_text)
            
            QMessageBox.information(
                self.format_tab,
                "Информация",
                f"Результаты успешно сохранены в файл: {file_path}"
            )
            
        except Exception as e:
            QMessageBox.critical(
                self.format_tab,
                "Ошибка",
                f"Ошибка при сохранении файла: {str(e)}"
            ) 