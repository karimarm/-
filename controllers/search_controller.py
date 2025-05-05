#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QThread, pyqtSignal, QObject
from utils.online_search import OnlineSearch

class SearchWorker(QObject):
    """
    Рабочий поток для выполнения поиска в фоне, чтобы не блокировать UI
    """
    
    # Сигналы
    results_ready = pyqtSignal(list)
    progress_updated = pyqtSignal(int)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, query, source, max_results):
        """
        Инициализация рабочего потока
        
        Args:
            query (str): Поисковой запрос
            source (str): Источник для поиска
            max_results (int): Максимальное количество результатов
        """
        super().__init__()
        self.query = query
        self.source = source
        self.max_results = max_results
    
    def search(self):
        """Выполнение поиска"""
        try:
            # Эмуляция прогресса
            self.progress_updated.emit(10)
            
            # Выполнение поиска
            results = OnlineSearch.search(self.query, self.source, self.max_results)
            
            self.progress_updated.emit(90)
            
            # Обогащаем результаты дополнительной информацией
            for i, item in enumerate(results):
                if item.doi:
                    try:
                        OnlineSearch.get_full_info(item)
                    except Exception as e:
                        print(f"Ошибка при получении дополнительной информации для {item.doi}: {e}")
                
                # Обновляем прогресс
                progress = 90 + (i + 1) * 10 // len(results) if results else 100
                self.progress_updated.emit(progress)
            
            # Отправляем результаты
            self.results_ready.emit(results)
            
        except Exception as e:
            self.error_occurred.emit(str(e))
            print(f"Ошибка при поиске: {e}")
        finally:
            self.progress_updated.emit(100)


class SearchController:
    """
    Контроллер для вкладки поиска источников.
    """
    
    def __init__(self, model, search_tab):
        """
        Инициализация контроллера
        
        Args:
            model: Модель приложения
            search_tab: Вкладка поиска
        """
        self.model = model
        self.view = search_tab
        self.search_thread = None
        self.search_worker = None
        
        # Подключение сигналов
        self.view.search_requested.connect(self.search)
        self.view.add_to_bibliography.connect(self.add_to_bibliography)
        
        # Подключение сигналов фильтров
        self.connect_filter_signals()
    
    def connect_filter_signals(self):
        """Подключение сигналов фильтров"""
        # Фильтры языка
        self.view.language_all.toggled.connect(lambda: self.apply_filters())
        self.view.language_ru.toggled.connect(lambda: self.apply_filters())
        self.view.language_en.toggled.connect(lambda: self.apply_filters())
        
        # Фильтры типа
        self.view.type_all.toggled.connect(lambda: self.apply_filters())
        self.view.type_article.toggled.connect(lambda: self.apply_filters())
        self.view.type_book.toggled.connect(lambda: self.apply_filters())
        
        # Фильтры индексирования
        self.view.vak_checkbox.toggled.connect(lambda: self.apply_filters())
        self.view.rinc_checkbox.toggled.connect(lambda: self.apply_filters())
    
    def search(self, query, source, max_results):
        """
        Выполнение поиска источников
        
        Args:
            query (str): Поисковой запрос
            source (str): Источник для поиска
            max_results (int): Максимальное количество результатов
        """
        # Остановка предыдущего поиска, если он существует
        if self.search_thread and self.search_thread.isRunning():
            self.search_thread.quit()
            self.search_thread.wait()
        
        # Создание нового потока для поиска
        self.search_thread = QThread()
        self.search_worker = SearchWorker(query, source, max_results)
        self.search_worker.moveToThread(self.search_thread)
        
        # Подключение сигналов
        self.search_thread.started.connect(self.search_worker.search)
        self.search_worker.results_ready.connect(self.handle_search_results)
        self.search_worker.results_ready.connect(self.search_thread.quit)
        self.search_worker.progress_updated.connect(self.view.update_progress)
        self.search_worker.error_occurred.connect(self.handle_search_error)
        
        # Запуск потока
        self.search_thread.start()
    
    def handle_search_results(self, results):
        """
        Обработка результатов поиска
        
        Args:
            results (list): Список объектов BibliographyItem
        """
        # Применяем фильтры к результатам
        filtered_results = self.filter_results(results)
        
        # Отображаем результаты
        self.view.display_results(filtered_results)
    
    def handle_search_error(self, error_message):
        """
        Обработка ошибки поиска
        
        Args:
            error_message (str): Сообщение об ошибке
        """
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.critical(self.view, "Ошибка поиска", f"Произошла ошибка при поиске: {error_message}")
    
    def add_to_bibliography(self, items):
        """
        Добавление источников в библиографию
        
        Args:
            items (list): Список объектов BibliographyItem для добавления
        """
        for item in items:
            self.model.add_bibliography_item(item)
    
    def filter_results(self, results):
        """
        Фильтрация результатов поиска по заданным критериям
        
        Args:
            results (list): Исходный список результатов
            
        Returns:
            list: Отфильтрованный список результатов
        """
        filtered_results = []
        
        # Получаем состояние фильтров
        language_filter = None
        if self.view.language_ru.isChecked():
            language_filter = "ru"
        elif self.view.language_en.isChecked():
            language_filter = "en"
        
        type_filter = None
        if self.view.type_article.isChecked():
            type_filter = "article"
        elif self.view.type_book.isChecked():
            type_filter = "book"
        
        vak_filter = self.view.vak_checkbox.isChecked()
        rinc_filter = self.view.rinc_checkbox.isChecked()
        
        # Применяем фильтры
        for item in results:
            # Фильтр языка
            if language_filter and item.language != language_filter:
                continue
            
            # Фильтр типа
            if type_filter and item.type != type_filter:
                continue
            
            # Фильтр ВАК
            if vak_filter and not item.is_vak:
                continue
            
            # Фильтр РИНЦ
            if rinc_filter and not item.is_rinc:
                continue
            
            # Если прошли все фильтры, добавляем в результаты
            filtered_results.append(item)
        
        return filtered_results
    
    def apply_filters(self):
        """Применение фильтров к текущим результатам"""
        if hasattr(self.view.results_table, "_bibliography_items") and self.view.results_table._bibliography_items:
            original_results = self.view.results_table._bibliography_items
            filtered_results = self.filter_results(original_results)
            self.view.display_results(filtered_results) 