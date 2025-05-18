#!/usr/bin/env python
# -*- coding: utf-8 -*-

from models.bibliography_item import BibliographyItem
from utils.reference_parser import ReferenceParser

class InputController:
    """
    Контроллер для вкладки ввода и редактирования библиографических ссылок.
    Обрабатывает взаимодействие между моделью и представлением.
    """
    
    def __init__(self, model, view):
        """
        Инициализация контроллера
        
        Args:
            model: Модель данных
            view: Представление вкладки ввода
        """
        self.model = model
        self.view = view
        
        # Привязка сигналов представления к методам контроллера
        self.view.add_bibliography_signal.connect(self.add_bibliography)
        self.view.add_structured_bibliography_signal.connect(self.add_structured_bibliography)
        self.view.edit_bibliography_signal.connect(self.edit_bibliography)
        self.view.update_item_property_signal.connect(self.update_item_property)
        self.view.parse_text_signal.connect(self.parse_text)
        self.view.remove_item_signal.connect(self.remove_item)
        
        # Начальное обновление списка в представлении
        self.update_view()
    
    def add_bibliography(self, text, format_type):
        """
        Добавление новой библиографической ссылки
        
        Args:
            text (str): Текст библиографической ссылки
            format_type (str): Тип формата
        """
        if not text:
            return
        
        # Создание объекта библиографической записи
        item = BibliographyItem(text)
        
        # Добавление в модель
        self.model.add_bibliography_item(item)
        
        # Обновление представления
        self.update_view()
    
    def edit_bibliography(self, text, index, format_type):
        """
        Редактирование существующей библиографической ссылки
        
        Args:
            text (str): Новый текст библиографической ссылки
            index (int): Индекс редактируемой записи
            format_type (str): Тип формата
        """
        if not text or index < 0 or index >= len(self.model.bibliography_list):
            return
        
        # Замена существующей записи
        self.model.bibliography_list[index] = BibliographyItem(text)
        
        # Обновление представления
        self.update_view()
    
    def parse_text(self, text):
        """
        Распознавание библиографической ссылки и заполнение формы
        
        Args:
            text (str): Текст библиографической ссылки
        """
        if not text:
            return
        
        # Распознавание библиографической ссылки
        item = ReferenceParser.parse(text)
        
        # Заполнение формы распознанными данными
        self.view.fill_form_with_data(item.to_dict())
    
    def remove_item(self, index):
        """
        Удаление библиографической ссылки
        
        Args:
            index (int): Индекс удаляемой записи
        """
        if index < 0 or index >= len(self.model.bibliography_list):
            return
        
        # Удаление записи из модели
        self.model.remove_bibliography_item(index)
        
        # Обновление представления
        self.update_view()
    
    def update_view(self):
        """Обновление представления списка библиографических ссылок"""
        self.view.update_bibliography_list(self.model.bibliography_list)
    
    def add_structured_bibliography(self, data):
        """
        Добавление новой библиографической ссылки из структурированных данных
        
        Args:
            data (dict): Словарь с данными библиографической записи
        """
        if not data or not data.get('title'):
            return
        
        # Создание объекта библиографической записи из словаря
        item = BibliographyItem.from_dict(data)
        
        # Устанавливаем сырой текст ссылки (полную библиографическую ссылку)
        if 'raw_text' in data and data['raw_text']:
            item.raw_text = data['raw_text']
        elif 'full_reference' in data and data['full_reference']:
            item.raw_text = data['full_reference']
        
        # Добавление в модель
        self.model.add_bibliography_item(item)
        
        # Обновление представления
        self.update_view()
    
    def update_item_property(self, index, property_name, value):
        """
        Обновление свойства библиографической записи
        
        Args:
            index (int): Индекс записи
            property_name (str): Имя свойства
            value: Новое значение
        """
        if index < 0 or index >= len(self.model.bibliography_list):
            return
            
        # Обновление свойства
        setattr(self.model.bibliography_list[index], property_name, value) 