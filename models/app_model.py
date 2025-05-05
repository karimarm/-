#!/usr/bin/env python
# -*- coding: utf-8 -*-

class AppModel:
    """
    Основная модель приложения.
    Содержит данные и бизнес-логику приложения.
    """
    
    def __init__(self):
        """Инициализация модели приложения"""
        # Текущий библиографический список
        self._bibliography_list = []
        # История библиографических списков
        self._history = []
        # Критерии проверки
        self._criteria = {
            'min_english_percent': 0,
            'min_recent_year': 2020,
            'min_recent_percent': 0,
            'min_vak_percent': 0,
            'min_rinc_percent': 0,
            'max_single_author_percent': 100
        }
    
    @property
    def bibliography_list(self):
        """Получить текущий библиографический список"""
        return self._bibliography_list
        
    @bibliography_list.setter
    def bibliography_list(self, value):
        """Установить текущий библиографический список и добавить в историю"""
        if self._bibliography_list:
            self._history.append(self._bibliography_list.copy())
        self._bibliography_list = value
    
    @property
    def criteria(self):
        """Получить текущие критерии проверки"""
        return self._criteria
    
    @criteria.setter
    def criteria(self, value):
        """Установить новые критерии проверки"""
        self._criteria = value
    
    @property
    def history(self):
        """Получить историю библиографических списков"""
        return self._history
    
    def add_bibliography_item(self, item):
        """Добавить элемент в библиографический список"""
        self._bibliography_list.append(item)
    
    def remove_bibliography_item(self, index):
        """Удалить элемент из библиографического списка по индексу"""
        if 0 <= index < len(self._bibliography_list):
            del self._bibliography_list[index]
            
    def clear_bibliography(self):
        """Очистить текущий библиографический список"""
        if self._bibliography_list:
            self._history.append(self._bibliography_list.copy())
        self._bibliography_list = []
    
    def revert_to_previous(self):
        """Вернуться к предыдущему состоянию библиографического списка"""
        if self._history:
            self._bibliography_list = self._history.pop()
            return True
        return False 