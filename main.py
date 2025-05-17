#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication
from controllers.main_controller import MainController
from models.app_model import AppModel
from views.main_window import MainWindow

def main():
    """Точка входа в приложение"""
    app = QApplication(sys.argv)
    app.setApplicationName("БиблиоАналитика")
    
    # Инициализация основных компонентов MVC
    model = AppModel()
    view = MainWindow()
    controller = MainController(model, view)
    
    # Запуск главного окна
    view.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 