# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

# from models.bibliography_item import BibliographyItem
# from utils.reference_parser import ReferenceParser

# class ReferenceFormatter:
#     """
#     Класс для форматирования библиографических ссылок в различные стили.
#     Поддерживает форматы: ГОСТ, IEEE.
#     """
    
#     @staticmethod
#     def convert(text, source_format, target_format):
#         """
#         Преобразование ссылки из одного формата в другой
        
#         Args:
#             text (str): Текст библиографической ссылки
#             source_format (str): Исходный формат (ГОСТ, IEEE, auto)
#             target_format (str): Целевой формат (ГОСТ, IEEE)
            
#         Returns:
#             str: Преобразованная ссылка
#         """
#         # Используем существующий парсер для распознавания элементов
#         item = ReferenceParser.parse(text, source_format)
        
#         # Форматируем результат в целевой формат
#         return ReferenceFormatter.format(item, target_format)
    
#     @staticmethod
#     def format(item, format_type):
#         """
#         Форматирование библиографической записи в указанный формат
        
#         Args:
#             item (BibliographyItem): Объект библиографической записи
#             format_type (str): Тип формата (ГОСТ, IEEE)
            
#         Returns:
#             str: Отформатированная ссылка
#         """
#         if format_type.lower() == "гост" or format_type.lower() == "gost":
#             return ReferenceFormatter._format_gost(item)
#         elif format_type.lower() == "ieee":
#             return ReferenceFormatter._format_ieee(item)
#         else:
#             # По умолчанию используем ГОСТ
#             return ReferenceFormatter._format_gost(item)
    
#     @staticmethod
#     def _format_gost(item):
#         """
#         Форматирование ссылки по ГОСТ 7.0.5-2008
        
#         Args:
#             item (BibliographyItem): Объект библиографической записи
            
#         Returns:
#             str: Отформатированная ссылка
#         """
#         result = ""
        
#         # Добавление авторов
#         if item.authors:
#             # В ГОСТ автор обычно идет в формате "Фамилия И. О."
#             for i, author in enumerate(item.authors):
#                 if i > 0:
#                     result += ", "
#                 # Проверяем, в каком формате записаны инициалы
#                 if "." in author and author.index(".") < author.index(" ") if " " in author else True:
#                     # Инициалы идут перед фамилией (формат IEEE) - переставляем
#                     parts = author.split()
#                     if len(parts) >= 2:
#                         # Последняя часть - фамилия, все остальное - инициалы
#                         surname = parts[-1]
#                         initials = " ".join(parts[:-1])
#                         result += f"{surname} {initials}"
#                     else:
#                         result += author
#                 else:
#                     result += author
#             result += ". "
        
#         # Добавление названия
#         if item.title:
#             result += item.title + ". "
        
#         # В зависимости от типа источника
#         if item.type == 'book' or item.type == 'книга':
#             # Для книг: Город: Издательство, Год. - Страницы с.
#             if item.publisher:
#                 if item.city:
#                     result += item.city + ": "
#                 result += item.publisher
#                 if item.year:
#                     result += ", " + item.year
#                 result += ". "
#             elif item.year:
#                 result += item.year + ". "
                
#             if item.pages:
#                 # Если указан диапазон страниц
#                 if "-" in item.pages or "–" in item.pages:
#                     result += item.pages + " с. "
#                 else:
#                     result += item.pages + " с. "
                
#         elif item.type == 'article' or item.type == 'статья':
#             # Для статей: // Журнал. Год. Том X. № Y. С. Z-W.
#             if item.journal:
#                 result += "// " + item.journal + ". "
            
#             if item.year:
#                 result += item.year + ". "
            
#             if item.volume:
#                 result += "Т. " + item.volume + ". "
            
#             if item.issue:
#                 result += "№ " + item.issue + ". "
            
#             if item.pages:
#                 result += "С. " + item.pages + ". "
                
#         elif item.type == 'web' or item.type == 'веб-ресурс':
#             # Для веб-ресурсов: [Электронный ресурс]. URL: http://example.com (дата обращения: ДД.ММ.ГГГГ).
#             result += "[Электронный ресурс]. "
            
#             if item.year:
#                 result += item.year + ". "
            
#             if item.url:
#                 result += "URL: " + item.url + " "
                
#             if item.access_date:
#                 result += "(дата обращения: " + item.access_date + "). "
        
#         # Добавление DOI
#         if item.doi:
#             result += "DOI: " + item.doi + " "
        
#         return result.strip()
    
#     @staticmethod
#     def _format_ieee(item):
#         """
#         Форматирование ссылки по стандарту IEEE
        
#         Args:
#             item (BibliographyItem): Объект библиографической записи
            
#         Returns:
#             str: Отформатированная ссылка
#         """
#         result = ""
        
#         # Добавление авторов
#         if item.authors:
#             # В IEEE автор обычно идет в формате "И. О. Фамилия"
#             for i, author in enumerate(item.authors):
#                 if i > 0:
#                     result += ", "
#                 # Проверяем, в каком формате записаны инициалы
#                 if "." in author and author.index(".") > author.index(" ") if " " in author else False:
#                     # Инициалы идут после фамилии (формат ГОСТ) - переставляем
#                     parts = author.split()
#                     if len(parts) >= 2:
#                         # Первая часть - фамилия, все остальное - инициалы
#                         surname = parts[0]
#                         initials = " ".join(parts[1:])
#                         result += f"{initials} {surname}"
#                     else:
#                         result += author
#                 else:
#                     result += author
#             result += ", "
        
#         # Добавление названия
#         if item.title:
#             result += "\"" + item.title + "\", "
        
#         # В зависимости от типа источника
#         if item.type == 'book' or item.type == 'книга':
#             # Для книг: City, Country: Publisher, Year.
#             if item.city:
#                 result += item.city
#                 if item.country:
#                     result += ", " + item.country
#                 result += ": "
            
#             if item.publisher:
#                 result += item.publisher + ", "
            
#             if item.year:
#                 result += item.year + "."
#             else:
#                 # Убираем последнюю запятую, если нет года
#                 if result.endswith(", "):
#                     result = result[:-2] + "."
#                 else:
#                     result += "."
                
#         elif item.type == 'article' or item.type == 'статья':
#             # Для статей: Journal Name, vol. X, no. Y, pp. Z-W, Month Year.
#             if item.journal:
#                 result += item.journal + ", "
            
#             if item.volume:
#                 result += "vol. " + item.volume
#                 if item.issue:
#                     result += ", no. " + item.issue
#                 result += ", "
#             elif item.issue:
#                 result += "no. " + item.issue + ", "
            
#             if item.pages:
#                 # Если указан диапазон страниц
#                 if "-" in item.pages or "–" in item.pages:
#                     result += "pp. " + item.pages
#                 else:
#                     result += "p. " + item.pages
#                 result += ", "
            
#             if item.year:
#                 if hasattr(item, 'month') and item.month:
#                     result += item.month + " "
#                 result += item.year + "."
#             else:
#                 # Убираем последнюю запятую, если нет года
#                 if result.endswith(", "):
#                     result = result[:-2] + "."
#                 else:
#                     result += "."
                
#         elif item.type == 'web' or item.type == 'веб-ресурс':
#             # Для веб-ресурсов: [Online]. Available: http://example.com, Accessed on: Date.
#             result += "[Online]. Available: "
            
#             if item.url:
#                 result += item.url + ", "
                
#             if item.access_date:
#                 result += "Accessed on: " + item.access_date + "."
#             else:
#                 # Убираем последнюю запятую, если нет даты доступа
#                 if result.endswith(", "):
#                     result = result[:-2] + "."
#                 else:
#                     result += "."
        
#         # Добавление DOI
#         if item.doi:
#             result += " DOI: " + item.doi
        
#         return result.strip()
    
#     @staticmethod
#     def format_list(items, format_type, sort_by=None):
#         """
#         Форматирование списка библиографических записей
        
#         Args:
#             items (list): Список объектов BibliographyItem
#             format_type (str): Тип формата (ГОСТ, IEEE)
#             sort_by (str, optional): Поле для сортировки (author, year, title)
            
#         Returns:
#             list: Список отформатированных ссылок
#         """
#         # Сортировка списка, если указано поле
#         if sort_by:
#             if sort_by.lower() == "author" or sort_by.lower() == "автор":
#                 # Сортировка по первому автору
#                 sorted_items = sorted(items, key=lambda x: x.authors[0] if x.authors else "")
#             elif sort_by.lower() == "year" or sort_by.lower() == "год":
#                 # Сортировка по году
#                 sorted_items = sorted(items, key=lambda x: x.year if x.year else "")
#             elif sort_by.lower() == "title" or sort_by.lower() == "название":
#                 # Сортировка по названию
#                 sorted_items = sorted(items, key=lambda x: x.title if x.title else "")
#             else:
#                 sorted_items = items
#         else:
#             sorted_items = items
        
#         # Форматирование каждой записи
#         formatted_items = []
#         for item in sorted_items:
#             formatted_items.append(ReferenceFormatter.format(item, format_type))
        
#         return formatted_items
    
#     @staticmethod
#     def batch_convert(texts, source_format, target_format):
#         """
#         Пакетное преобразование списка ссылок из одного формата в другой
        
#         Args:
#             texts (list): Список текстов библиографических ссылок
#             source_format (str): Исходный формат (ГОСТ, IEEE, auto)
#             target_format (str): Целевой формат (ГОСТ, IEEE)
            
#         Returns:
#             list: Список преобразованных ссылок
#         """
#         result = []
#         for text in texts:
#             result.append(ReferenceFormatter.convert(text, source_format, target_format))
#         return result
    
#     @staticmethod
#     def convert_gost_to_ieee(text):
#         """
#         Преобразование ссылки из формата ГОСТ в IEEE
        
#         Args:
#             text (str): Текст библиографической ссылки в формате ГОСТ
            
#         Returns:
#             str: Преобразованная ссылка в формате IEEE
#         """
#         # Используем парсер для извлечения элементов
#         item = ReferenceParser.parse(text, "ГОСТ")
        
#         # Форматируем в IEEE
#         return ReferenceFormatter._format_ieee(item)
    
#     @staticmethod
#     def convert_ieee_to_gost(text):
#         """
#         Преобразование ссылки из формата IEEE в ГОСТ
        
#         Args:
#             text (str): Текст библиографической ссылки в формате IEEE
            
#         Returns:
#             str: Преобразованная ссылка в формате ГОСТ
#         """
#         # Используем парсер для извлечения элементов
#         item = ReferenceParser.parse(text, "IEEE")
        
#         # Форматируем в ГОСТ
#         return ReferenceFormatter._format_gost(item)
    
#     @staticmethod
#     def convert_batch(texts, source_format, target_format):
#         """
#         Пакетное преобразование списка ссылок
        
#         Args:
#             texts (list): Список текстов библиографических ссылок
#             source_format (str): Исходный формат (ГОСТ, IEEE)
#             target_format (str): Целевой формат (ГОСТ, IEEE)
            
#         Returns:
#             list: Список преобразованных ссылок
#         """
#         results = []
        
#         for text in texts:
#             # Парсинг исходного текста
#             item = ReferenceParser.parse(text, source_format)
            
#             # Форматирование в целевой формат
#             if target_format.lower() == "гост" or target_format.lower() == "gost":
#                 converted = ReferenceFormatter._format_gost(item)
#             elif target_format.lower() == "ieee":
#                 converted = ReferenceFormatter._format_ieee(item)
#             else:
#                 converted = text  # Если формат не распознан, возвращаем исходный текст
            
#             results.append(converted)
        
#         return results 