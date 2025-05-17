#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from models.bibliography_item import BibliographyItem

class ReferenceParser:
    """
    Класс для распознавания элементов библиографических ссылок из текста.
    """
    
    # Компилированные регулярные выражения для более быстрой работы
    # Шаблоны для определения формата
    GOST_DETECT_PATTERN = re.compile(r'\.[\s]*[–-][\s]*[^\d]*\d+|С\.\s*\d+')
    IEEE_DETECT_PATTERN = re.compile(r'^\[\d+\]|IEEE', re.IGNORECASE)
    
    # Шаблоны ГОСТ для разных типов источников
    # Книга: Автор. Название : Подзаголовок / Авторы. — Издание — Город : Издательство, Год. — Страницы с.
    # GOST_BOOK_PATTERN = re.compile(
    #     r'(?P<authors>.*?)\.\s+'  # Авторы, заканчивающиеся точкой
    #     r'(?P<title>.*?)'  # Название книги
    #     r'(?:\s*:\s*(?P<subtitle>.*?))?'  # Подзаголовок (опционально)
    #     r'(?:\s*/\s*(?P<authors2>.*?))?'  # Авторы после косой черты (опционально)
    #     r'(?:\.\s+—\s+(?P<edition>.*?))?'  # Издание (опционально)
    #     r'(?:\s*—\s+)?'  # Разделитель (опционально)
    #     r'(?P<city>.*?)'  # Город издания
    #     r'\s*:\s*'  # Разделитель между городом и издательством
    #     r'(?P<publisher>.*?)'  # Издательство
    #     r',\s+(?P<year>\d{4})'  # Год издания
    #     r'(?:\.\s+—\s+(?P<pages>\d+)\s+с\.)?'  # Количество страниц (опционально)
    # )
    # GOST_BOOK_PATTERN = re.compile(
    #     r'(?P<authors>.*?)\.\s+'  # Авторы, заканчивающиеся точкой
    #     r'(?P<title>.*?)'  # Название книги
    #     r'(?:\s*:\s*(?P<subtitle>.*?))?\s*/\s*'  # Подзаголовок (опционально)
    #     r'(?:(?P<authors2>.*?)\.\s*—\s*)?'  # Авторы после косой черты (опционально)
    #     r'(?:\.\s+—\s+(?P<edition>.*?))?'  # Издание (опционально)
    #     r'(?:\s*—\s+)?'  # Разделитель (опционально)
    #     r'(?P<city>.*?)'  # Город издания
    #     r'\s*:\s*'  # Разделитель между городом и издательством
    #     r'(?P<publisher>.*?)'  # Издательство
    #     r',\s+(?P<year>\d{4})'  # Год издания
    #     r'(?:\.\s+—\s+(?P<pages>\d+)\s+с\.)?'  # Количество страниц (опционально)
    # )
    GOST_BOOK_PATTERN = re.compile(
        r'(?P<authors>.*?)\.\s+'
        r'(?P<title>.*?)'
        r'(?:\s*:\s*(?P<subtitle>.*?))?\s*/\s*'
        r'(?P<authors2>.*?)'
        r'(?:\.\s+—\s+(?P<edition>.*?)-е изд\.)?'
        r'(?:\s*—\s+(?P<city>.*?))?'
        r'\s*:\s*'
        r'(?P<publisher>.*?)?'
        r',\s+(?P<year>\d{4})?'
        r'(?:\.\s+—\s+)?'
        r'(?P<pages>\d+)\s+с\.'
    )

    # # Статья в журнале: Автор. Название статьи // Название журнала. — Год. — Том X. — № Y. — С. Z-W.
    # GOST_ARTICLE_PATTERN = re.compile(
    #     r'(?P<authors>.*?)\.\s+'  # Авторы, заканчивающиеся точкой
    #     r'(?P<title>.*?)(?:\s+/\s+[^/]*?)?'  # Название статьи, исключая авторов после косой черты (если есть)
    #     r'\s+//'  # Разделитель между названием статьи и названием журнала
    #     r'\s+(?P<journal>.*?)'  # Название журнала
    #     r'(?:\.\s+—\s+|\.\s+)?'  # Разделитель (опционально)
    #     r'(?P<year>\d{4})'  # Год издания
    #     r'(?:\.\s+—\s+|\.\s+)?'  # Разделитель
    #     r'(?:Т\.\s+(?P<volume>\d+))?'  # Том (опционально)
    #     r'(?:\.\s+—\s+|\.\s+)?'  # Разделитель (опционально)
    #     r'(?:№\s+(?P<issue>.*?))?'  # Номер (опционально)
    #     r'(?:\.\s+—\s+|\.\s+)?'  # Разделитель
    #     #r'(?:С\.\s+(?P<pages>\d+(?:-\d+)?))?'  # Страницы (опционально)
    #     r'(?:[Сс]\.\s*(?P<pages>.*?)\.)?'  # Страницы (опционально)
    # )

    # Статья в журнале: Автор. Название статьи // Название журнала. — Год. — Том X. — № Y. — С. Z-W.
    GOST_ARTICLE_PATTERN = re.compile(
        r'(?P<authors>.*?)\.\s+'  # Авторы (минимум 1 символ до точки)
        #r'(?P<authors>(?:[А-ЯЁ][а-яё]+\s+[А-ЯЁ]\.[А-ЯЁ]\.)(?:\s*,\s*[А-ЯЁ][а-яё]+\s+[А-ЯЁ]\.[А-ЯЁ]\.)*(?:\s+и\s+(?:др\.|[А-ЯЁ][а-яё]+\s+[А-ЯЁ]\.[А-ЯЁ]\.))?\.\s*'
        r'(?P<title>.+?)\s+//\s*'  # Название статьи (минимум 1 символ)
        r'(?P<journal>.+?)\.\s*'  # Название журнала (минимум 1 символ)
        r'(?:—\s*(?P<year>\d{4})\s*\.\s*)?'  # Год
        r'(?:—\s*Т\.\s*(?P<volume>\d+)\s*\.\s*)?'  # Том (опционально)
        r'(?:—\s*№\s*(?P<issue>[^.—]+)\s*\.\s*)?'  # Номер (опционально)
        r'(?:—\s*[Сс]\.\s*(?P<pages>\d+(?:\s*-\s*\d+)?)\s*\.)?'  # Страницы (опционально)
    )
    
    # Статья в сборнике: Автор. Название статьи // Название сборника / Под ред. Редактора. — Город : Издательство, Год. — С. X-Y.
    GOST_COLLECTION_PATTERN = re.compile(
        r'(?P<authors>.*?)\.\s+'  # Авторы, заканчивающиеся точкой
        r'(?P<title>.*?)(?:\s+/\s+[^/]*?)?'  # Название статьи, исключая авторов после косой черты (если есть)
        r'\s+//'  # Разделитель между названием статьи и названием сборника
        r'\s+(?P<collection>.*?)'  # Название сборника
        r'(?:\s*/\s*(?P<editors>.*?))?'  # Редакторы (опционально)
        r'(?:\.\s+—\s+|\.\s+)?'  # Разделитель (опционально)
        r'(?P<city>.*?)'  # Город издания
        r'\s*:\s*'  # Разделитель между городом и издательством
        r'(?P<publisher>.*?)'  # Издательство
        r',\s+(?P<year>\d{4})'  # Год издания
        r'(?:\.\s+—\s+|\.\s+)'  # Разделитель
        r'(?:С\.\s+(?P<pages>\d+(?:-\d+)?))?'  # Страницы (опционально)
    )
    
    # Веб-ресурс: Автор. Название [Электронный ресурс]. — URL: http://example.com (дата обращения: ДД.ММ.ГГГГ).
    GOST_WEB_PATTERN = re.compile(
        r'(?P<authors>.*?)\.\s+'  # Авторы, заканчивающиеся точкой
        r'(?P<title>.*?)(?:\s+/\s+[^/]*?)?'  # Название ресурса, исключая авторов после косой черты (если есть)
        r'(?:\s+\[Электронный\s+ресурс\])?'  # Тип ресурса (опционально)
        r'(?:\.\s+—\s+|\.\s+)'  # Разделитель
        r'(?:URL:\s+)?'  # Метка URL (опционально)
        r'(?P<url>https?://[^\s]+)'  # URL адрес
        r'(?:\s+\(дата\s+обращения:\s+(?P<access_date>[\d\.]+)\))?'  # Дата обращения (опционально)
    )
    
    # Автореферат диссертации: Автор. Название : автореф. дис. ... канд. наук / Автор. — Город, Год. — Страницы с.
    GOST_THESIS_PATTERN = re.compile(
        r'(?P<authors>.*?)\.\s+'  # Авторы, заканчивающиеся точкой
        r'(?P<title>.*?)(?:\s+/\s+[^/]*?)?'  # Название работы, исключая авторов после косой черты (если есть)
        r'\s*:\s*автореф\.\s+дис\.\s+\.\.\.\s+'  # Указание на автореферат
        r'(?P<degree>.*?)'  # Степень
        r'\s*/\s*(?P<authors2>.*?)'  # Авторы после косой черты
        r'(?:\.\s+—\s+|\.\s+)'  # Разделитель
        r'(?P<city>.*?)'  # Город
        r',\s+(?P<year>\d{4})'  # Год
        r'(?:\.\s+—\s+(?P<pages>\d+(?:-\d+)?)\s+с\.)?'  # Страницы (опционально), с возможным диапазоном
    )
    
    # Шаблоны IEEE
    # Статья в журнале: A. Author1, B. Author2, "Title of paper," Journal Name, vol. X, no. Y, pp. Z-W, Month Year
    IEEE_ARTICLE_PATTERN = re.compile(
        r'(?P<authors>.*?),\s+'  # Авторы, заканчивающиеся запятой
        r'"(?P<title>.*?)",'  # Название статьи в кавычках
        r'\s+(?P<journal>.*?),'  # Название журнала
        r'(?:\s+vol\.\s+(?P<volume>\d+))?'  # Том (опционально)
        r'(?:,\s+no\.\s+(?P<issue>\d+))?'  # Номер (опционально)
        r'(?:,\s+pp\.\s+(?P<pages>\d+[-–]\d+)|,\s+p\.\s+(?P<page>\d+))?'  # Страницы (опционально)
        r'(?:,\s+(?P<month>[A-Za-z]+))?\s+'  # Месяц (опционально)
        r'(?P<year>\d{4})'  # Год
    )
    
    # Статья в сборнике конференции: A. Author1, B. Author2, "Title of paper," in Proc. Conference Name, City, Country, Year, pp. X-Y.
    IEEE_CONFERENCE_PATTERN = re.compile(
        r'(?P<authors>.*?),\s+'  # Авторы, заканчивающиеся запятой
        r'"(?P<title>.*?)",'  # Название статьи в кавычках
        r'\s+in\s+Proc\.\s+(?P<conference>.*?),'  # Название конференции
        r'\s+(?P<city>.*?),'  # Город
        r'(?:\s+(?P<country>.*?),)?'  # Страна (опционально)
        r'\s+(?P<year>\d{4})'  # Год
        r'(?:,\s+pp\.\s+(?P<pages>\d+[-–]\d+)|,\s+p\.\s+(?P<page>\d+))?'  # Страницы (опционально)
    )
    
    # Книга: A. Author1, B. Author2, Title of Book. City, Country: Publisher, Year.
    IEEE_BOOK_PATTERN = re.compile(
        r'(?P<authors>.*?),\s+'  # Авторы, заканчивающиеся запятой
        r'(?P<title>.*?)\.'  # Название книги
        r'\s+(?P<city>.*?),'  # Город
        r'(?:\s+(?P<country>.*?):)?'  # Страна (опционально)
        r'\s+(?P<publisher>.*?),'  # Издательство
        r'\s+(?P<year>\d{4})'  # Год
    )
    
    # Общие шаблоны для извлечения дополнительных данных
    YEAR_PATTERN = re.compile(r'(?:,\s+|,|\s+|.\s+)(\d{4})(?:\s*г\.?)?(?:,|\.|\s|$)')
    VOLUME_PATTERN = re.compile(r'[Тт]\.?\s*(\d+)|[Vv]ol\.?\s*(\d+)')
    ISSUE_PATTERN = re.compile(r'[№Nn]\.?\s*(\d+)|[Nn]o\.?\s*(\d+)')
    PAGES_PATTERN = re.compile(r'[Сс]\.?\s*(\d+)(?:[–-](\d+))?|[Pp]\.?\s*(\d+)(?:[–-](\d+))?|(\d+)[\s]*[-–][\s]*(\d+)')
    URL_PATTERN = re.compile(r'(?:URL:|Режим доступа:)?\s*(https?://[^\s,]+)')
    DOI_PATTERN = re.compile(r'(DOI:?|doi\.org\/)\s*(10\.\d{4,}(?:\.\d+)*\/(?:(?!["&\'])\S)+)', re.IGNORECASE)
    
    @staticmethod
    def parse(text, format_type="auto"):
        """
        Распознавание элементов библиографической ссылки из текста
        
        Args:
            text (str): Текст библиографической ссылки
            format_type (str): Тип формата (auto, ГОСТ, IEEE)
            
        Returns:
            BibliographyItem: Объект с распознанными элементами
        """
        # Создание объекта библиографической записи
        item = BibliographyItem(text)
        
        # Если формат не указан или auto, определяем его автоматически
        if format_type.lower() == "auto" or format_type.lower() == "автоопределение":
            format_type = ReferenceParser._detect_format(text)
        
        # Выбор метода распознавания в зависимости от формата
        if format_type.lower() == "гост" or format_type.lower() == "gost":
            ReferenceParser._parse_gost(text, item)
        elif format_type.lower() == "ieee":
            ReferenceParser._parse_ieee(text, item)
        else:
            # Если формат не распознан, пробуем общий метод
            ReferenceParser._parse_general(text, item)
        
        # Определение языка
        ReferenceParser._detect_language(item)
        
        # Определение типа источника, если еще не определен
        if not item.type:
            ReferenceParser._detect_source_type(item)
        
        # Проверка признаков ВАК/РИНЦ
        ReferenceParser._check_vak_rinc(item)
        
        return item
    
    @staticmethod
    def _process_authors(authors_text):
        """
        Обработка текста с авторами для корректного определения авторов
        с разными форматами инициалов
        
        Args:
            authors_text (str): Текст с авторами
            
        Returns:
            list: Список авторов
        """
        if not authors_text:
            return []
            
        # Предварительная обработка
        authors_text = authors_text.replace(" и ", ", ").replace(" and ", ", ").replace("&", ",")
        
        # Шаблоны для различных форматов авторов
        # ГОСТ: "Фамилия И. О." или "Фамилия И.О."
        gost_pattern = re.compile(r'([А-Яа-яA-Za-z]+)\s+([А-Яа-яA-Za-z]\.(?:\s*[А-Яа-яA-Za-z]\.)?)')
        
        # IEEE: "И. О. Фамилия" или "И.О. Фамилия"
        ieee_pattern = re.compile(r'([А-Яа-яA-Za-z]\.(?:\s*[А-Яа-яA-Za-z]\.)?)\s+([А-Яа-яA-Za-z]+)')
        
        # Проверка наличия шаблона ГОСТ
        if gost_pattern.search(authors_text):
            parts = [part.strip() for part in authors_text.split(',') if part.strip()]
            return parts
        
        # Проверка наличия шаблона IEEE
        if ieee_pattern.search(authors_text):
            parts = [part.strip() for part in authors_text.split(',') if part.strip()]
            return parts
        
        # Если ни один шаблон не подходит, просто разделяем по запятым
        return [part.strip() for part in authors_text.split(',') if part.strip()]
    
    @staticmethod
    def _detect_format(text):
        """
        Автоматическое определение формата библиографической ссылки
        
        Args:
            text (str): Текст библиографической ссылки
            
        Returns:
            str: Определенный формат (ГОСТ, IEEE или unknown)
        """
        # Признаки формата IEEE
        if (ReferenceParser.IEEE_DETECT_PATTERN.search(text) or 
            ('pp.' in text and 'vol.' in text) or 
            ('"' in text and ',' in text and ('pp.' in text or 'vol.' in text or 'no.' in text))):
            return "IEEE"
        
        # Признаки формата ГОСТ
        if ReferenceParser.GOST_DETECT_PATTERN.search(text):
            return "ГОСТ"
        
        # Если формат не определен, возвращаем ГОСТ как наиболее распространенный
        return "ГОСТ"
    
    @staticmethod
    def _parse_gost(text, item):
        """
        Распознавание элементов библиографической ссылки в формате ГОСТ
        
        Args:
            text (str): Текст библиографической ссылки
            item (BibliographyItem): Объект для заполнения
        """
        # Пробуем применить шаблоны для разных типов источников
        # Книга
        book_match = ReferenceParser.GOST_BOOK_PATTERN.search(text)
        if book_match:
            data = book_match.groupdict()
            if data['authors']:
                item.authors = ReferenceParser._process_authors(data['authors']+'.')
            item.title = data['title'] if data['title'] else ""
            item.subtitle = data['subtitle'] if data['subtitle'] else ""
            # Очищаем поле edition от суффикса "-е изд."
            if data['edition']:
                edition = data['edition'].strip()
                # Удаляем суффикс "-е изд." если он есть
                edition = re.sub(r'\s*-\s*е\s*изд\.?$', '', edition, flags=re.IGNORECASE)
                item.edition = edition
            item.city = data['city'] if data['city'] else ""
            item.publisher = data['publisher'] if data['publisher'] else ""
            item.year = data['year'] if data['year'] else ""
            item.pages = data['pages'] if data['pages'] else ""
            item.type = 'book'
            return
        
        # Статья в журнале
        article_match = ReferenceParser.GOST_ARTICLE_PATTERN.search(text)
        if article_match:
            data = article_match.groupdict()
            if data['authors']:
                item.authors = ReferenceParser._process_authors(data['authors']+'.')
            item.title = data['title'] if data['title'] else ""
            item.journal = data['journal'] if data['journal'] else ""
            item.year = data['year'] if data['year'] else ""
            item.volume = data['volume'] if data['volume'] else ""
            item.issue = data['issue'] if data['issue'] else ""
            item.pages = data['pages'] if data['pages'] else ""
            item.type = 'article'
            return
        
        # Статья в сборнике
        collection_match = ReferenceParser.GOST_COLLECTION_PATTERN.search(text)
        if collection_match:
            data = collection_match.groupdict()
            if data['authors']:
                item.authors = ReferenceParser._process_authors(data['authors']+'.')
            item.title = data['title'] if data['title'] else ""
            item.journal = data['collection'] if data['collection'] else ""
            item.publisher = data['publisher'] if data['publisher'] else ""
            item.year = data['year'] if data['year'] else ""
            item.pages = data['pages'] if data['pages'] else ""
            item.type = 'article'
            return
        
        # Веб-ресурс
        web_match = ReferenceParser.GOST_WEB_PATTERN.search(text)
        if web_match:
            data = web_match.groupdict()
            if data['authors']:
                item.authors = ReferenceParser._process_authors(data['authors']+'.')
            item.title = data['title'] if data['title'] else ""
            item.url = data['url'] if data['url'] else ""
            item.type = 'web'
            return
        
        # Автореферат диссертации
        thesis_match = ReferenceParser.GOST_THESIS_PATTERN.search(text)
        if thesis_match:
            data = thesis_match.groupdict()
            if data['authors']:
                item.authors = ReferenceParser._process_authors(data['authors']+'.')
            item.title = data['title'] if data['title'] else ""
            item.year = data['year'] if data['year'] else ""
            item.pages = data['pages'] if data['pages'] else ""
            item.type = 'thesis'
            return
        
        # Если ни один из шаблонов не подошел, но есть признаки статьи ('//')
        if '//' in text and not item.journal:
            # Разбираем по разделителю '//'
            parts = text.split('//')
            if len(parts) >= 2:
                # Первая часть обычно содержит авторов и название
                first_part = parts[0].strip()
                # Вторая часть обычно содержит название журнала и метаданные
                second_part = parts[1].strip()
                
                # Извлекаем название журнала до первой точки или тире
                journal_match = re.search(r'^([^\.—]+)', second_part)
                if journal_match:
                    item.journal = journal_match.group(1).strip()
                
                # Если авторы не определены, пробуем извлечь из первой части
                if not item.authors:
                    # Ищем авторов до первой точки
                    author_match = re.search(r'^(.*?)\.\s+', first_part)
                    if author_match:
                        item.authors = ReferenceParser._process_authors(author_match.group(1)+'.')
                    
                    # Извлекаем название после авторов (после первой точки)
                    title_match = re.search(r'^.*?\.\s+(.*?)(?:\s+/\s+.*?)?$', first_part)
                    if title_match:
                        item.title = title_match.group(1).strip()
                
                # Если журнал определен, значит это статья
                if item.journal:
                    item.type = 'article'
                    
                # Извлекаем дополнительную информацию из второй части
                year_match = re.search(r'—\s+(\d{4})', second_part)
                if year_match:
                    item.year = year_match.group(1)
                
                volume_match = re.search(r'Т\.\s+(\d+)', second_part)
                if volume_match:
                    item.volume = volume_match.group(1)
                
                issue_match = re.search(r'№\s+(\d+)', second_part)
                if issue_match:
                    item.issue = issue_match.group(1)
                
                pages_match = re.search(r'С\.\s*(\d+(?:.\d+)?)', second_part)
                if pages_match:
                    item.pages = pages_match.group(1)
                
                return
        
        # Дополнительная информация
        # Издательство
        publisher_match = re.search(r'(?:[\s:]+)([^:,\.]+(?:Издательство|Изд-во|Press|Publishing)[^:,\.]+)(?:,|\.|$)', text, re.IGNORECASE)
        if publisher_match:
            item.publisher = publisher_match.group(1).strip()
            item.type = 'book'
        
        # Год, том, номер, страницы, URL, DOI
        year_match = ReferenceParser.YEAR_PATTERN.search(text)
        if year_match:
            item.year = year_match.group(1)
        
        volume_match = ReferenceParser.VOLUME_PATTERN.search(text)
        if volume_match:
            item.volume = volume_match.group(1) or volume_match.group(2)
        
        issue_match = ReferenceParser.ISSUE_PATTERN.search(text)
        if issue_match:
            item.issue = issue_match.group(1) or issue_match.group(2)
        
        pages_match = ReferenceParser.PAGES_PATTERN.search(text)
        if pages_match:
            groups = pages_match.groups()
            if groups[0] and groups[1]:  # C. X-Y
                item.pages = f"{groups[0]}–{groups[1]}"
            elif groups[2] and groups[3]:  # P. X-Y
                item.pages = f"{groups[2]}–{groups[3]}"
            elif groups[4] and groups[5]:  # X-Y
                item.pages = f"{groups[4]}–{groups[5]}"
            elif groups[0]:  # C. X
                item.pages = groups[0]
            elif groups[2]:  # P. X
                item.pages = groups[2]
        
        url_match = ReferenceParser.URL_PATTERN.search(text)
        if url_match:
            item.url = url_match.group(1).rstrip('.')
            if not item.type:
                item.type = 'web'
        
        doi_match = ReferenceParser.DOI_PATTERN.search(text)
        if doi_match:
            item.doi = doi_match.group(2)
    
    @staticmethod
    def _parse_ieee(text, item):
        """
        Распознавание элементов библиографической ссылки в формате IEEE
        
        Args:
            text (str): Текст библиографической ссылки
            item (BibliographyItem): Объект для заполнения
        """
        # Удаляем номер ссылки, если есть
        cleaned_text = re.sub(r'^\[\d+\]\s*', '', text)
        
        # Проверяем наличие цитаты в кавычках для определения названия
        title_match = re.search(r'"([^"]+)"', cleaned_text)
        if title_match:
            item.title = title_match.group(1).strip()
            
            # Разбиваем текст по названию
            parts = cleaned_text.split(f'"{item.title}"')
            
            # Текст перед названием обычно содержит авторов
            if parts and parts[0]:
                authors_text = parts[0].strip()
                if authors_text.endswith(','):
                    authors_text = authors_text[:-1]
                item.authors = ReferenceParser._process_authors(authors_text)
            
            # Текст после названия может содержать журнал, том, номер, страницы и т.д.
            if len(parts) > 1 and parts[1]:
                after_title = parts[1].strip()
                
                # Журнал часто идет сразу после названия до следующей запятой
                journal_match = re.search(r'^\s*,\s*([^,]+)', after_title)
                if journal_match:
                    item.journal = journal_match.group(1).strip()
                    item.type = 'article'
        else:
            # Если нет названия в кавычках, пробуем стандартные шаблоны
            # Статья в журнале
            article_match = ReferenceParser.IEEE_ARTICLE_PATTERN.search(cleaned_text)
            if article_match:
                data = article_match.groupdict()
                if data['authors']:
                    item.authors = ReferenceParser._process_authors(data['authors'])
                item.title = data['title'] if data['title'] else ""
                item.journal = data['journal'] if data['journal'] else ""
                item.volume = data['volume'] if data['volume'] else ""
                item.issue = data['issue'] if data['issue'] else ""
                if data['pages']:
                    item.pages = data['pages']
                elif data['page']:
                    item.pages = data['page']
                item.year = data['year'] if data['year'] else ""
                item.type = 'article'
                return
                
            # Статья в сборнике конференции
            conference_match = ReferenceParser.IEEE_CONFERENCE_PATTERN.search(cleaned_text)
            if conference_match:
                data = conference_match.groupdict()
                if data['authors']:
                    item.authors = ReferenceParser._process_authors(data['authors'])
                item.title = data['title'] if data['title'] else ""
                item.journal = data['conference'] if data['conference'] else ""
                if data['pages']:
                    item.pages = data['pages']
                elif data['page']:
                    item.pages = data['page']
                item.year = data['year'] if data['year'] else ""
                item.type = 'conference'
                return
                
            # Книга
            book_match = ReferenceParser.IEEE_BOOK_PATTERN.search(cleaned_text)
            if book_match:
                data = book_match.groupdict()
                if data['authors']:
                    item.authors = ReferenceParser._process_authors(data['authors'])
                item.title = data['title'] if data['title'] else ""
                item.publisher = data['publisher'] if data['publisher'] else ""
                item.year = data['year'] if data['year'] else ""
                item.type = 'book'
                return
        
        # Дополнительная информация
        # Том, номер, страницы, год, DOI
        volume_match = re.search(r'vol\.\s*(\d+)', cleaned_text, re.IGNORECASE)
        if volume_match:
            item.volume = volume_match.group(1)
            if not item.type:
                item.type = 'article'
        
        issue_match = re.search(r'no\.\s*(\d+)', cleaned_text, re.IGNORECASE)
        if issue_match:
            item.issue = issue_match.group(1)
            if not item.type:
                item.type = 'article'
        
        pages_match = re.search(r'pp\.\s*(\d+)[-–](\d+)|p\.\s*(\d+)', cleaned_text, re.IGNORECASE)
        if pages_match:
            if pages_match.group(1) and pages_match.group(2):
                item.pages = f"{pages_match.group(1)}–{pages_match.group(2)}"
            elif pages_match.group(3):
                item.pages = pages_match.group(3)
        
        # Если страницы не найдены с помощью предыдущего поиска, 
        # попробуем найти их с помощью общего PAGES_PATTERN
        if not item.pages:
            pages_match = ReferenceParser.PAGES_PATTERN.search(cleaned_text)
            if pages_match:
                groups = pages_match.groups()
                if groups[0] and groups[1]:  # C. X-Y
                    item.pages = f"{groups[0]}–{groups[1]}"
                elif groups[2] and groups[3]:  # P. X-Y
                    item.pages = f"{groups[2]}–{groups[3]}"
                elif groups[4] and groups[5]:  # X-Y
                    item.pages = f"{groups[4]}–{groups[5]}"
                elif groups[0]:  # C. X
                    item.pages = groups[0]
                elif groups[2]:  # P. X
                    item.pages = groups[2]
        
        year_match = re.search(r'\b(19|20)\d{2}\b', cleaned_text)
        if year_match:
            item.year = year_match.group(0)
        
        doi_match = re.search(r'doi:?\s*(10\.\d{4,}(?:\.\d+)*\/(?:(?!["&\'])\S)+)', cleaned_text, re.IGNORECASE)
        if doi_match:
            item.doi = doi_match.group(1)
        
        # Определение типа источника по содержимому текста
        if 'IEEE' in cleaned_text and not item.type:
            item.type = 'article'
    
    @staticmethod
    def _parse_general(text, item):
        """
        Общий метод распознавания элементов библиографической ссылки
        
        Args:
            text (str): Текст библиографической ссылки
            item (BibliographyItem): Объект для заполнения
        """
        # Для общего метода пробуем сначала шаблоны ГОСТ, затем IEEE
        # Если ни один из них не подходит, используем базовый анализ
        
        # Пробуем шаблоны ГОСТ
        ReferenceParser._parse_gost(text, item)
        
        # Если не удалось распознать авторов или название, пробуем IEEE
        if not item.authors and not item.title:
            ReferenceParser._parse_ieee(text, item)
        
        # Если всё ещё нет данных, используем базовый анализ
        if not item.authors and not item.title:
            # Разбиваем текст по точкам для анализа
            parts = text.split('.')
            
            # Первая часть обычно содержит авторов и/или название
            if parts:
                first_part = parts[0].strip()
                
                # Если в первой части есть запятые и это не URL
                if ',' in first_part and not re.search(r'https?:|www\.', first_part, re.IGNORECASE):
                    # Анализируем как список, возможно авторов
                    potential_items = [p.strip() for p in first_part.split(',') if p.strip()]
                    
                    # Проверяем, есть ли в списке инициалы
                    has_initials = any(re.search(r'[А-Яа-яA-Za-z]\.\s*[А-Яа-яA-Za-z]\.', p) for p in potential_items)
                    
                    if has_initials:
                        # Вероятно, это авторы
                        item.authors = potential_items
                        
                        # Название может быть во второй части
                        if len(parts) > 1:
                            item.title = parts[1].strip()
                    else:
                        # Иначе считаем первую часть названием
                        item.title = first_part
                else:
                    # Если нет запятых, считаем первую часть названием
                    item.title = first_part
        
        # Дополнительно ищем информацию о годе, томе, номере, страницах и т.д.
        # если они еще не были найдены
        if not item.year:
            year_match = re.search(r'\b(19|20)\d{2}\b', text)
            if year_match:
                item.year = year_match.group(0)
        
        if not item.publisher:
            publisher_match = re.search(r'(?:[\s:]+)([^:,\.]+(?:Издательство|Изд-во|Press|Publishing)[^:,\.]+)(?:,|\.|$)', text, re.IGNORECASE)
            if publisher_match:
                item.publisher = publisher_match.group(1).strip()
                if not item.type:
                    item.type = 'book'
        
        if not item.pages:
            pages_match = ReferenceParser.PAGES_PATTERN.search(text)
            if pages_match:
                groups = pages_match.groups()
                if groups[0] and groups[1]:  # C. X-Y
                    item.pages = f"{groups[0]}–{groups[1]}"
                elif groups[2] and groups[3]:  # P. X-Y
                    item.pages = f"{groups[2]}–{groups[3]}"
                elif groups[4] and groups[5]:  # X-Y
                    item.pages = f"{groups[4]}–{groups[5]}"
                elif groups[0]:  # C. X
                    item.pages = groups[0]
                elif groups[2]:  # P. X
                    item.pages = groups[2]
        
        if not item.url:
            url_match = ReferenceParser.URL_PATTERN.search(text)
            if url_match:
                item.url = url_match.group(1).rstrip('.')
                if not item.type:
                    item.type = 'web'
        
        if not item.doi:
            doi_match = ReferenceParser.DOI_PATTERN.search(text)
            if doi_match:
                item.doi = doi_match.group(2)
                if not item.type:
                    item.type = 'article'
    
    @staticmethod
    def _detect_language(item):
        """
        Определение языка библиографической ссылки
        
        Args:
            item (BibliographyItem): Объект библиографической записи
        """
        # Подсчет русских и латинских букв в заголовке
        if item.title:
            ru_pattern = re.compile(r'[а-яА-ЯёЁ]')
            en_pattern = re.compile(r'[a-zA-Z]')
            
            ru_count = len(ru_pattern.findall(item.title))
            en_count = len(en_pattern.findall(item.title))
            
            if ru_count > en_count:
                item.language = 'ru'
            elif en_count > ru_count:
                item.language = 'en'
    
    @staticmethod
    def _detect_source_type(item):
        """
        Определение типа источника, если не был определен ранее
        
        Args:
            item (BibliographyItem): Объект библиографической записи
        """
        if item.journal or item.volume or item.issue:
            item.type = 'article'
        elif item.publisher:
            item.type = 'book'
        elif item.url:
            item.type = 'web'
        else:
            item.type = 'book'  # по умолчанию
    
    @staticmethod
    def _check_vak_rinc(item):
        """
        Проверка признаков ВАК/РИНЦ
        
        Args:
            item (BibliographyItem): Объект библиографической записи
        """
        # Предположим, что есть некий словарь или список ВАК/РИНЦ журналов
        # В реальном приложении здесь должна быть проверка по базе данных
        
        vak_journals = [
            'Вестник МГУ', 'Известия РАН', 'Доклады Академии наук', 
            'Вопросы философии', 'Вопросы экономики'
        ]
        
        rinc_journals = [
            'Научный журнал', 'Системный администратор', 'Прикладная информатика',
            'Вестник СПбГУ', 'Вестник МГТУ'
        ]
        
        if item.journal:
            # Компилируем регулярные выражения для более эффективного поиска
            vak_patterns = [re.compile(re.escape(vj.lower())) for vj in vak_journals]
            rinc_patterns = [re.compile(re.escape(rj.lower())) for rj in rinc_journals]
            
            journal_lower = item.journal.lower()
            item.is_vak = any(pattern.search(journal_lower) for pattern in vak_patterns)
            item.is_rinc = any(pattern.search(journal_lower) for pattern in rinc_patterns)

# Примеры использования:
# reference = "Иванов А.А., Петров Б.Б. Название книги. М.: Издательство, 2022. 300 с."
# item = ReferenceParser.parse(reference)
# print(item.authors)  # ['Иванов А.А.', 'Петров Б.Б.']
# print(item.title)    # 'Название книги'
# print(item.year)     # '2022' 