#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QStatusBar, QAction, QMenuBar, QMenu,
    QMessageBox, QFileDialog
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon

class MainWindow(QMainWindow):
    """
    Главное окно приложения.
    Содержит основной интерфейс с вкладками для разных функций.
    """
    
    # Сигналы для взаимодействия с контроллером
    import_bibliography_signal = pyqtSignal(str, str)  # путь к файлу, формат
    export_bibliography_signal = pyqtSignal(str, str)  # путь к файлу, формат
    
    def __init__(self):
        """Инициализация главного окна"""
        super().__init__()
        
        self.setWindowTitle("БиблиоАналитика")
        self.setMinimumSize(800, 600)
        
        # Создание центрального виджета
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Создание основной компоновки
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # Создание меню
        self.create_menu()
        
        # Создание вкладок
        self.create_tabs()
        
        # Создание строки состояния
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Готово")
    
    def create_menu(self):
        """Создание главного меню"""
        menu_bar = self.menuBar()
        
        # Меню "Файл"
        file_menu = menu_bar.addMenu("&Файл")
        
        # Действия в меню "Файл"
        import_action = QAction("&Импорт из файла...", self)
        import_action.setShortcut("Ctrl+O")
        import_action.triggered.connect(self.on_import)
        file_menu.addAction(import_action)
        
        export_action = QAction("&Экспорт в файл...", self)
        export_action.setShortcut("Ctrl+S")
        export_action.triggered.connect(self.on_export)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("&Выход", self)
        exit_action.setShortcut("Alt+F4")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Меню "Правка"
        edit_menu = menu_bar.addMenu("&Правка")
        
        undo_action = QAction("&Отменить", self)
        undo_action.setShortcut("Ctrl+Z")
        undo_action.triggered.connect(self.on_undo)
        edit_menu.addAction(undo_action)
        
        # Меню "Помощь"
        help_menu = menu_bar.addMenu("&Справка")
        
        about_action = QAction("&О программе", self)
        about_action.triggered.connect(self.on_about)
        help_menu.addAction(about_action)
    
    def create_tabs(self):
        """Создание вкладок для разных функций"""
        self.tabs = QTabWidget()
        self.main_layout.addWidget(self.tabs)
        
        # Вкладка "Ввод и редактирование"
        self.input_tab = QWidget()
        self.tabs.addTab(self.input_tab, "Ввод и редактирование")
        
        # Вкладка "Проверка критериев"
        self.criteria_tab = QWidget()
        self.tabs.addTab(self.criteria_tab, "Проверка критериев")
        
        # Вкладка "Поиск источников"
        self.search_tab = QWidget()
        self.tabs.addTab(self.search_tab, "Поиск источников")
        
        # Вкладка "Форматирование и экспорт"
        self.export_tab = QWidget()
        self.tabs.addTab(self.export_tab, "Форматирование и экспорт")
    
    def on_import(self):
        """Обработчик импорта из файла"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Импорт библиографического списка",
            "",
            "Документы Word (*.docx);;PDF-файлы (*.pdf);;Все файлы (*.*)"
        )
        
        if file_path:
            # Определение формата файла по расширению
            file_format = file_path.split('.')[-1].lower()
            self.import_bibliography_signal.emit(file_path, file_format)
    
    def on_export(self):
        """Обработчик экспорта в файл"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Экспорт библиографического списка",
            "",
            "Документы Word (*.docx);;PDF-файлы (*.pdf);;Текстовые файлы (*.txt)"
        )
        
        if file_path:
            # Определение формата файла по расширению
            file_format = file_path.split('.')[-1].lower()
            self.export_bibliography_signal.emit(file_path, file_format)
    
    def on_undo(self):
        """Обработчик отмены последнего действия"""
        # Этот метод будет связан с контроллером
        pass
    
    def on_about(self):
        """Отображение информации о программе"""
        QMessageBox.about(
            self,
            "О программе БиблиоАналитика",
            "БиблиоАналитика версия 1.0\n\n"
            "Программа для обработки библиографических списков.\n\n"
            "© 2025 Все права защищены."
        )
    
    def show_status_message(self, message, timeout=5000):
        """
        Отображение сообщения в строке состояния
        
        Args:
            message (str): Текст сообщения
            timeout (int): Время отображения в миллисекундах
        """
        self.status_bar.showMessage(message, timeout)
    
    def show_error_message(self, title, message):
        """
        Отображение сообщения об ошибке
        
        Args:
            title (str): Заголовок сообщения
            message (str): Текст сообщения
        """
        QMessageBox.critical(self, title, message)
    
    def show_info_message(self, title, message):
        """
        Отображение информационного сообщения
        
        Args:
            title (str): Заголовок сообщения
            message (str): Текст сообщения
        """
        QMessageBox.information(self, title, message) 