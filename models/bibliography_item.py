#!/usr/bin/env python
# -*- coding: utf-8 -*-

class BibliographyItem:
    """
    Модель для представления библиографической записи.
    Содержит информацию о библиографической ссылке и ее элементах.
    """
    
    def __init__(self, raw_text=""):
        """
        Инициализация библиографической записи
        
        Args:
            raw_text (str): Исходный текст библиографической ссылки
        """
        self.raw_text = raw_text
        self.authors = []
        self.title = ""
        self.year = ""
        self.publisher = ""
        self.journal = ""
        self.volume = ""
        self.issue = ""
        self.pages = ""
        self.doi = ""
        self.url = ""
        self.language = "ru"  # ru или en
        self.type = "book"    # book, article, web, etc.
        self.is_vak = False
        self.is_rinc = False
        self.additional_info = {}
    
    def __str__(self):
        """Строковое представление библиографической записи"""
        if self.raw_text:
            return self.raw_text
        
        # Если сырого текста нет, формируем его из элементов
        result = ""
        if self.authors:
            result += ", ".join(self.authors)
            result += ". "
        
        if self.title:
            result += self.title + ". "
        
        if self.journal:
            result += self.journal + ". "
        
        if self.year:
            result += self.year + ". "
        
        if self.publisher:
            result += self.publisher + ". "
        
        if self.volume and self.issue:
            result += f"Т. {self.volume}, № {self.issue}. "
        elif self.volume:
            result += f"Т. {self.volume}. "
        elif self.issue:
            result += f"№ {self.issue}. "
        
        if self.pages:
            result += f"С. {self.pages}. "
        
        if self.doi:
            result += f"DOI: {self.doi}. "
        
        if self.url:
            result += f"URL: {self.url}. "
        
        return result.strip()
    
    def format_as(self, format_type="GOST"):
        """
        Форматирование библиографической записи по указанному стандарту
        
        Args:
            format_type (str): Тип форматирования (GOST, APA, MLA, etc.)
            
        Returns:
            str: Отформатированная библиографическая запись
        """
        # Здесь будет реализация различных форматов
        # Пока возвращаем строковое представление
        return str(self)
    
    def is_complete(self):
        """
        Проверка на полноту библиографической записи
        
        Returns:
            bool: True, если запись содержит все необходимые элементы
        """
        # Минимально необходимые поля в зависимости от типа записи
        if self.type == "book":
            return bool(self.authors and self.title and self.year and self.publisher)
        elif self.type == "article":
            return bool(self.authors and self.title and self.year and self.journal)
        elif self.type == "web":
            return bool(self.title and self.url)
        else:
            return bool(self.title and self.year)
    
    def to_dict(self):
        """
        Преобразование библиографической записи в словарь
        
        Returns:
            dict: Словарь с данными библиографической записи
        """
        return {
            'raw_text': self.raw_text,
            'authors': self.authors,
            'title': self.title,
            'year': self.year,
            'publisher': self.publisher,
            'journal': self.journal,
            'volume': self.volume,
            'issue': self.issue,
            'pages': self.pages,
            'doi': self.doi,
            'url': self.url,
            'language': self.language,
            'type': self.type,
            'is_vak': self.is_vak,
            'is_rinc': self.is_rinc,
            'additional_info': self.additional_info
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Создание библиографической записи из словаря
        
        Args:
            data (dict): Словарь с данными библиографической записи
            
        Returns:
            BibliographyItem: Новый экземпляр библиографической записи
        """
        item = cls(data.get('raw_text', ''))
        item.authors = data.get('authors', [])
        item.title = data.get('title', '')
        item.year = data.get('year', '')
        item.publisher = data.get('publisher', '')
        item.journal = data.get('journal', '')
        item.volume = data.get('volume', '')
        item.issue = data.get('issue', '')
        item.pages = data.get('pages', '')
        item.doi = data.get('doi', '')
        item.url = data.get('url', '')
        item.language = data.get('language', 'ru')
        item.type = data.get('type', 'book')
        item.is_vak = data.get('is_vak', False)
        item.is_rinc = data.get('is_rinc', False)
        item.additional_info = data.get('additional_info', {})
        return item 