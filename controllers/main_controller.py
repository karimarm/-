#!/usr/bin/env python
# -*- coding: utf-8 -*-

from views.input_tab import InputTab
from views.criteria_tab import CriteriaTab
from controllers.input_controller import InputController
from controllers.criteria_controller import CriteriaController
from utils.file_utils import read_file, save_file
from models.bibliography_item import BibliographyItem

class MainController:
    """
    Основной контроллер приложения.
    Связывает модель и представление, обрабатывает действия пользователя.
    """
    
    def __init__(self, model, view):
        """
        Инициализация контроллера
        
        Args:
            model: Основная модель приложения
            view: Главное окно приложения
        """
        self.model = model
        self.view = view
        
        # Подключение сигналов представления к обработчикам
        self.view.import_bibliography_signal.connect(self.import_bibliography)
        self.view.export_bibliography_signal.connect(self.export_bibliography)
        
        # Инициализация вкладок
        self.init_tabs()
        
        # Подключение обработчика отмены действия
        self.view.on_undo = self.undo_last_action
    
    def init_tabs(self):
        """Инициализация вкладок приложения и их контроллеров"""
        # Удаление временных вкладок
        while self.view.tabs.count() > 0:
            self.view.tabs.removeTab(0)
        
        # Инициализация вкладки ввода и редактирования
        self.input_tab = InputTab()
        self.view.tabs.addTab(self.input_tab, "Ввод и редактирование")
        
        # Инициализация вкладки проверки критериев
        self.criteria_tab = CriteriaTab()
        self.view.tabs.addTab(self.criteria_tab, "Проверка критериев")
        
        # Создание контроллера для вкладки ввода
        self.input_controller = InputController(self.model, self.input_tab)
        
        # Создание контроллера для вкладки проверки критериев
        self.criteria_controller = CriteriaController(self.model, self.criteria_tab)
        
        # Установка активной вкладки
        self.view.tabs.setCurrentIndex(0)
    
    def import_bibliography(self, file_path, file_format):
        """
        Импорт библиографического списка из файла
        
        Args:
            file_path (str): Путь к файлу
            file_format (str): Формат файла (docx, pdf, txt)
        """
        try:
            # Чтение текста из файла
            text = read_file(file_path)
            
            # Разделение текста на библиографические ссылки
            # Предполагаем, что каждая ссылка находится на отдельной строке
            references = [ref.strip() for ref in text.split('\n') if ref.strip()]
            
            # Добавление каждой ссылки в модель
            for ref in references:
                item = BibliographyItem(ref)
                self.model.add_bibliography_item(item)
            
            # Обновление представления
            self.input_controller.update_view()
            
            self.view.show_status_message(f"Файл {file_path} успешно импортирован")
            
        except Exception as e:
            self.view.show_error_message("Ошибка импорта", f"Не удалось импортировать файл: {str(e)}")
    
    def export_bibliography(self, file_path, file_format):
        """
        Экспорт библиографического списка в файл
        
        Args:
            file_path (str): Путь к файлу
            file_format (str): Формат файла (docx, pdf, txt)
        """
        try:
            # Формирование текста из библиографического списка
            text = '\n'.join(str(item) for item in self.model.bibliography_list)
            
            # Сохранение текста в файл
            save_file(text, file_path)
            
            self.view.show_status_message(f"Библиографический список успешно экспортирован в {file_path}")
            
        except Exception as e:
            self.view.show_error_message("Ошибка экспорта", f"Не удалось экспортировать файл: {str(e)}")
    
    def undo_last_action(self):
        """Отмена последнего действия"""
        if self.model.revert_to_previous():
            # Обновление представления
            self.input_controller.update_view()
            self.view.show_status_message("Последнее действие отменено")
        else:
            self.view.show_status_message("Нет действий для отмены")
    
    def add_bibliography_item(self, item):
        """
        Добавление библиографической записи
        
        Args:
            item: Библиографическая запись для добавления
        """
        self.model.add_bibliography_item(item)
        # Обновление представления
        self.input_controller.update_view()
        self.view.show_status_message("Библиографическая запись добавлена")
    
    def remove_bibliography_item(self, index):
        """
        Удаление библиографической записи по индексу
        
        Args:
            index (int): Индекс записи для удаления
        """
        self.model.remove_bibliography_item(index)
        # Обновление представления
        self.input_controller.update_view()
        self.view.show_status_message("Библиографическая запись удалена")
    
    def clear_bibliography(self):
        """Очистка библиографического списка"""
        self.model.clear_bibliography()
        # Обновление представления
        self.input_controller.update_view()
        self.view.show_status_message("Библиографический список очищен") 