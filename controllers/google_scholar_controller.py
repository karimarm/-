#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import time
from PyQt5.QtCore import QObject, pyqtSignal, QThread
from utils.google_scholar_api import GoogleScholarAPI
from PyQt5.QtWidgets import QMessageBox

class GoogleScholarWorker(QThread):
    """
    Рабочий поток для выполнения поиска в Google Scholar в фоновом режиме.
    """
    
    # Сигналы для взаимодействия с контроллером
    result_signal = pyqtSignal(list)  # список результатов
    error_signal = pyqtSignal(str)    # сообщение об ошибке
    
    def __init__(self, api, query, page, num, lang):
        """
        Инициализация рабочего потока
        
        Args:
            api (GoogleScholarAPI): Объект API для поиска
            query (str): Поисковый запрос
            page (int): Номер страницы результатов
            num (int): Количество результатов на странице
            lang (str): Язык результатов (ru, en)
        """
        super().__init__()
        self.api = api
        self.query = query
        self.page = page
        self.num = num
        self.lang = lang
    
    def run(self):
        """Выполнение поиска в фоновом потоке"""
        try:
            # Выполнение поиска через API
            results = self.api.search(self.query, self.page, self.num, self.lang)
            
            # Отправка сигнала с результатами
            self.result_signal.emit(results)
            
        except Exception as e:
            # Отправка сигнала об ошибке
            self.error_signal.emit(str(e))

class GoogleScholarController(QObject):
    """
    Контроллер для работы с Google Scholar API.
    """
    
    # Сигналы для взаимодействия с представлением
    results_updated_signal = pyqtSignal(list)  # обновление результатов поиска
    
    def __init__(self, widget, bibliography_model, api_key):
        """
        Инициализация контроллера
        
        Args:
            widget: Виджет поиска в Google Scholar
            bibliography_model: Модель библиографии
            api_key (str): API-ключ для доступа к SerpDog API
        """
        super().__init__()
        self.widget = widget
        self.bibliography_model = bibliography_model
        self.api = GoogleScholarAPI(api_key)
        
        # Хранение текущих результатов поиска
        self.current_results = []
        
        # Рабочий поток для поиска
        self.search_worker = None
        
        # Подключение сигналов
        self.connect_signals()
    
    def connect_signals(self):
        """Подключение сигналов к обработчикам"""
        # Сигналы от виджета поиска
        self.widget.search_signal.connect(self.on_search)
        self.widget.add_citation_signal.connect(self.on_add_citation)
        
        # Сигнал обновления результатов
        self.results_updated_signal.connect(self.widget.update_results)
    
    def on_search(self, query, page, num, lang):
        """
        Обработчик поиска
        
        Args:
            query (str): Поисковый запрос
            page (int): Номер страницы результатов
            num (int): Количество результатов на странице
            lang (str): Язык результатов (ru, en)
        """
        # Создание рабочего потока для поиска
        self.search_worker = GoogleScholarWorker(self.api, query, page, num, lang)
        
        # Подключение сигналов рабочего потока
        self.search_worker.result_signal.connect(self.on_search_result)
        self.search_worker.error_signal.connect(self.on_search_error)
        
        # Запуск рабочего потока
        self.search_worker.start()
    
    def on_search_result(self, results):
        """
        Обработчик получения результатов поиска
        
        Args:
            results (list): Список объектов BibliographyItem
        """
        # Сохранение текущих результатов
        self.current_results = results
        
        # Отправка сигнала на обновление интерфейса
        self.results_updated_signal.emit(results)
    
    def on_search_error(self, error_message):
        """
        Обработчик ошибки поиска
        
        Args:
            error_message (str): Сообщение об ошибке
        """
        QMessageBox.critical(
            self.widget,
            "Ошибка поиска",
            f"Произошла ошибка при выполнении поиска в Google Scholar: {error_message}"
        )
    
    def on_add_citation(self, index):
        """
        Добавление выбранной ссылки в библиографию
        
        Args:
            index (int): Индекс выбранного результата
        """
        if 0 <= index < len(self.current_results):
            # Получение выбранного результата
            item = self.current_results[index]
            
            # Добавление в модель библиографии
            self.bibliography_model.add_item(item)
            
            QMessageBox.information(
                self.widget,
                "Добавление в библиографию",
                f"Источник \"{item.title}\" успешно добавлен в библиографию."
            ) 