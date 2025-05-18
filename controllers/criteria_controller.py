#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Counter

class CriteriaController:
    """
    Контроллер для вкладки проверки критериев.
    Обрабатывает логику проверки соответствия библиографических ссылок критериям.
    """
    
    def __init__(self, model, view):
        """
        Инициализация контроллера
        
        Args:
            model: Модель данных
            view: Представление вкладки критериев
        """
        self.model = model
        self.view = view
        
        # Привязка сигналов представления к методам контроллера
        self.view.check_criteria_signal.connect(self.check_criteria)
        self.view.save_criteria_signal.connect(self.save_criteria)
        
        # Загрузка текущих критериев из модели
        self.view.set_criteria(self.model.criteria)
    
    def check_criteria(self, criteria):
        """
        Проверка библиографического списка на соответствие критериям
        
        Args:
            criteria (dict): Словарь с критериями проверки
        """
        # Получение библиографического списка из модели
        bib_list = self.model.bibliography_list
        
        if not bib_list:
            self.view.display_results({})
            self.view.display_statistics("Библиографический список пуст")
            return
        
        # Временное обновление критериев в модели для корректного расчета статистики
        original_criteria = self.model.criteria.copy()
        self.model.criteria = criteria
        
        # Вычисление статистики
        stats = self.calculate_statistics(bib_list)
        
        # Восстановление оригинальных критериев, если пользователь не сохранил их
        self.model.criteria = original_criteria
        
        # Проверка на соответствие критериям
        results = self.check_compliance(stats, criteria)
        
        # Отображение результатов и статистики
        self.view.display_results(results)
        self.view.display_statistics(self.format_statistics(stats))
    
    def save_criteria(self, criteria):
        """
        Сохранение критериев проверки в модель
        
        Args:
            criteria (dict): Словарь с критериями проверки
        """
        self.model.criteria = criteria
    
    def calculate_statistics(self, bib_list):
        """
        Вычисление статистики по библиографическому списку
        
        Args:
            bib_list (list): Список библиографических записей
            
        Returns:
            dict: Словарь со статистикой
        """
        total_items = len(bib_list)
        
        # Количество и процент источников на английском языке
        english_count = sum(1 for item in bib_list if item.language == 'en')
        english_percent = round((english_count / total_items) * 100, 2) if total_items > 0 else 0
        
        # Получение года для свежих источников из критериев
        recent_year = self.model.criteria.get('min_recent_year', 2000)
        
        # Количество и процент свежих источников
        recent_count = sum(1 for item in bib_list if item.year and item.year.isdigit() and int(item.year) >= recent_year)
        recent_percent = round((recent_count / total_items) * 100, 2) if total_items > 0 else 0
        
        # Количество и процент источников ВАК
        vak_count = sum(1 for item in bib_list if item.is_vak)
        vak_percent = round((vak_count / total_items) * 100, 2) if total_items > 0 else 0
        
        # Количество и процент источников РИНЦ
        rinc_count = sum(1 for item in bib_list if item.is_rinc)
        rinc_percent = round((rinc_count / total_items) * 100, 2) if total_items > 0 else 0
        
        # Получение указанного автора из критериев
        specified_author = self.model.criteria.get('specified_author', '').strip()
        
        # Подсчет источников по авторам
        author_counter = Counter()
        for item in bib_list:
            # Подсчет только для первого автора, если указано несколько
            if item.authors:
                first_author = item.authors[0]
                author_counter[first_author] += 1
        
        # Статистика по указанному автору
        if specified_author:
            # Подсчет источников с указанным автором (в любой позиции, не только первым)
            specified_author_count = sum(1 for item in bib_list if specified_author in item.authors)
            specified_author_percent = round((specified_author_count / total_items) * 100, 2) if total_items > 0 else 0
        else:
            # Если автор не указан, используем автора с наибольшим количеством источников
            most_common_author = author_counter.most_common(1)
            if most_common_author:
                specified_author = most_common_author[0][0]
                specified_author_count = most_common_author[0][1]
                specified_author_percent = round((specified_author_count / total_items) * 100, 2) if total_items > 0 else 0
            else:
                specified_author = "Нет"
                specified_author_count = 0
                specified_author_percent = 0
        
        # Типы источников
        types_counter = Counter(item.type for item in bib_list)
        
        # Статистика по годам
        years = [int(item.year) for item in bib_list if item.year and item.year.isdigit()]
        min_year = min(years) if years else None
        max_year = max(years) if years else None
        avg_year = round(sum(years) / len(years), 1) if years else None
        
        # Общая статистика
        stats = {
            'total_items': total_items,
            'english_count': english_count,
            'english_percent': english_percent,
            'recent_count': recent_count,
            'recent_percent': recent_percent,
            'recent_year': recent_year,
            'vak_count': vak_count,
            'vak_percent': vak_percent,
            'rinc_count': rinc_count,
            'rinc_percent': rinc_percent,
            'specified_author': {
                'name': specified_author,
                'count': specified_author_count,
                'percent': specified_author_percent
            },
            'type_stats': dict(types_counter),
            'year_stats': {
                'min_year': min_year,
                'max_year': max_year,
                'avg_year': avg_year
            }
        }
        
        return stats
    
    def check_compliance(self, stats, criteria):
        """
        Проверка соответствия статистики критериям
        
        Args:
            stats (dict): Словарь со статистикой
            criteria (dict): Словарь с критериями проверки
            
        Returns:
            dict: Словарь с результатами проверки
        """
        results = {}
        
        # Проверка источников на английском языке
        english_criteria_type = criteria.get('english_criteria_type', 'percent')
        if english_criteria_type == 'percent':
            min_english_percent = criteria.get('min_english_percent', 0)
            english_match = stats['english_percent'] >= min_english_percent
            required_value = f"≥ {min_english_percent}%"
        else:
            min_english_count = criteria.get('min_english_count', 0)
            english_match = stats['english_count'] >= min_english_count
            required_value = f"≥ {min_english_count} шт."
            
        results['english'] = {
            'name': "Источники на английском языке",
            'required': required_value,
            'current': f"{stats['english_percent']}% ({stats['english_count']} из {stats['total_items']})",
            'match': english_match
        }
        
        # Проверка свежих источников
        recent_criteria_type = criteria.get('recent_criteria_type', 'percent')
        if recent_criteria_type == 'percent':
            min_recent_percent = criteria.get('min_recent_percent', 0)
            recent_match = stats['recent_percent'] >= min_recent_percent
            required_value = f"≥ {min_recent_percent}%"
        else:
            min_recent_count = criteria.get('min_recent_count', 0)
            recent_match = stats['recent_count'] >= min_recent_count
            required_value = f"≥ {min_recent_count} шт."
            
        results['recent'] = {
            'name': f"Источники свежее {stats['recent_year']} года",
            'required': required_value,
            'current': f"{stats['recent_percent']}% ({stats['recent_count']} из {stats['total_items']})",
            'match': recent_match
        }
        
        # Проверка источников ВАК
        vak_criteria_type = criteria.get('vak_criteria_type', 'percent')
        if vak_criteria_type == 'percent':
            min_vak_percent = criteria.get('min_vak_percent', 0)
            vak_match = stats['vak_percent'] >= min_vak_percent
            required_value = f"≥ {min_vak_percent}%"
        else:
            min_vak_count = criteria.get('min_vak_count', 0)
            vak_match = stats['vak_count'] >= min_vak_count
            required_value = f"≥ {min_vak_count} шт."
            
        results['vak'] = {
            'name': "Источники ВАК",
            'required': required_value,
            'current': f"{stats['vak_percent']}% ({stats['vak_count']} из {stats['total_items']})",
            'match': vak_match
        }
        
        # Проверка источников РИНЦ
        rinc_criteria_type = criteria.get('rinc_criteria_type', 'percent')
        if rinc_criteria_type == 'percent':
            min_rinc_percent = criteria.get('min_rinc_percent', 0)
            rinc_match = stats['rinc_percent'] >= min_rinc_percent
            required_value = f"≥ {min_rinc_percent}%"
        else:
            min_rinc_count = criteria.get('min_rinc_count', 0)
            rinc_match = stats['rinc_count'] >= min_rinc_count
            required_value = f"≥ {min_rinc_count} шт."
            
        results['rinc'] = {
            'name': "Источники РИНЦ",
            'required': required_value,
            'current': f"{stats['rinc_percent']}% ({stats['rinc_count']} из {stats['total_items']})",
            'match': rinc_match
        }
        
        # Проверка источников указанного автора
        author_criteria_type = criteria.get('author_criteria_type', 'percent')
        specified_author_name = criteria.get('specified_author', '')
        
        if specified_author_name:
            author_label = f"Источники с автором: {specified_author_name}"
        else:
            author_label = "Источники наиболее представленного автора"
            
        if author_criteria_type == 'percent':
            max_author_percent = criteria.get('max_single_author_percent', 100)
            author_match = stats['specified_author']['percent'] <= max_author_percent
            required_value = f"≤ {max_author_percent}%"
        else:
            max_author_count = criteria.get('max_single_author_count', 1000)
            author_match = stats['specified_author']['count'] <= max_author_count
            required_value = f"≤ {max_author_count} шт."
            
        results['author'] = {
            'name': author_label,
            'required': required_value,
            'current': f"{stats['specified_author']['percent']}% ({stats['specified_author']['count']} из {stats['total_items']})",
            'match': author_match
        }
        
        return results
    
    def format_statistics(self, stats):
        """
        Форматирование статистики для отображения
        
        Args:
            stats (dict): Словарь со статистикой
            
        Returns:
            str: Отформатированная статистика
        """
        result = "Общая статистика библиографического списка:\n\n"
        
        result += f"Всего источников: {stats['total_items']}\n\n"
        
        result += "Языки:\n"
        result += f"- Русский: {stats['total_items'] - stats['english_count']} ({100 - stats['english_percent']}%)\n"
        result += f"- Английский: {stats['english_count']} ({stats['english_percent']}%)\n\n"
        
        result += "Типы источников:\n"
        for source_type, count in stats['type_stats'].items():
            percent = round((count / stats['total_items']) * 100, 2)
            result += f"- {source_type.capitalize()}: {count} ({percent}%)\n"
        result += "\n"
        
        result += "Годы:\n"
        if stats['year_stats']['min_year']:
            result += f"- Диапазон лет: {stats['year_stats']['min_year']} - {stats['year_stats']['max_year']}\n"
            result += f"- Средний год: {stats['year_stats']['avg_year']}\n"
            result += f"- Источников с {stats['recent_year']} года: {stats['recent_count']} ({stats['recent_percent']}%)\n\n"
        else:
            result += "- Нет данных о годах публикаций\n\n"
        
        result += "Авторство:\n"
        if stats['specified_author']['name'] != "Нет":
            if self.model.criteria.get('specified_author'):
                result += f"- Указанный автор: {stats['specified_author']['name']} ({stats['specified_author']['count']} источников, {stats['specified_author']['percent']}%)\n\n"
            else:
                result += f"- Автор с наибольшим числом источников: {stats['specified_author']['name']} ({stats['specified_author']['count']} источников, {stats['specified_author']['percent']}%)\n\n"
        else:
            result += "- Нет данных об авторах\n\n"
        
        result += "Научная аттестация:\n"
        result += f"- Источники ВАК: {stats['vak_count']} ({stats['vak_percent']}%)\n"
        result += f"- Источники РИНЦ: {stats['rinc_count']} ({stats['rinc_percent']}%)\n"
        
        return result 