#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMessageBox
from utils.reference_formatter import ReferenceFormatter

class ConvertController:
    """
    Контроллер для модуля преобразования библиографических ссылок.
    """
    
    def __init__(self, convert_tab, bibliography_model):
        """
        Инициализация контроллера преобразования
        
        Args:
            convert_tab: Вкладка преобразования (представление)
            bibliography_model: Модель библиографии (список записей)
        """
        self.convert_tab = convert_tab
        self.bibliography_model = bibliography_model
        
        # Подключение сигналов
        self.connect_signals()
    
    def connect_signals(self):
        """Подключение сигналов к обработчикам"""
        # Сигналы от вкладки преобразования
        self.convert_tab.convert_signal.connect(self.on_convert)
        self.convert_tab.convert_batch_signal.connect(self.on_convert_batch)
    
    def on_convert(self, text, source_format, target_format):
        """
        Обработчик преобразования отдельной ссылки
        
        Args:
            text (str): Текст ссылки
            source_format (str): Исходный формат
            target_format (str): Целевой формат
        """
        try:
            # Выбор метода преобразования в зависимости от форматов
            if source_format == "ГОСТ" and target_format == "IEEE":
                result = ReferenceFormatter.convert_gost_to_ieee(text)
            elif source_format == "IEEE" and target_format == "ГОСТ":
                result = ReferenceFormatter.convert_ieee_to_gost(text)
            else:
                # Если форматы совпадают, возвращаем исходный текст
                result = text
                QMessageBox.information(
                    self.convert_tab,
                    "Информация",
                    "Исходный и целевой форматы совпадают."
                )
            
            # Обновление представления
            self.convert_tab.set_result_text(result)
            
        except Exception as e:
            QMessageBox.critical(
                self.convert_tab,
                "Ошибка",
                f"Ошибка при преобразовании: {str(e)}"
            )
    
    def on_convert_batch(self, indices, source_format, target_format):
        """
        Обработчик пакетного преобразования
        
        Args:
            indices (list): Список индексов выбранных записей (пустой для всех)
            source_format (str): Исходный формат
            target_format (str): Целевой формат
        """
        try:
            # Получение исходных текстов
            if indices:
                # Только выбранные записи
                texts = [str(self.bibliography_model.items[i]) for i in indices]
            else:
                # Все записи
                texts = [str(item) for item in self.bibliography_model.items]
            
            if not texts:
                QMessageBox.warning(
                    self.convert_tab,
                    "Предупреждение",
                    "Нет записей для преобразования."
                )
                return
            
            # Выполнение пакетного преобразования
            results = ReferenceFormatter.convert_batch(texts, source_format, target_format)
            
            # Форматирование результатов в текст с нумерацией
            formatted_text = ""
            for i, result in enumerate(results):
                formatted_text += f"{i+1}. {result}\n\n"
            
            # Обновление представления
            self.convert_tab.set_batch_result_text(formatted_text)
            
        except Exception as e:
            QMessageBox.critical(
                self.convert_tab,
                "Ошибка",
                f"Ошибка при пакетном преобразовании: {str(e)}"
            ) 