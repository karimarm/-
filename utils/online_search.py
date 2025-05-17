# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

# import re
# import requests
# from bs4 import BeautifulSoup
# import time
# from models.bibliography_item import BibliographyItem

# class OnlineSearch:
#     """
#     Класс для поиска библиографических источников в онлайн-библиотеках.
#     Поддерживает поиск в Google Scholar, eLIBRARY.RU, Scopus и других источниках.
#     """
    
#     @staticmethod
#     def search(query, source="all", max_results=10):
#         """
#         Поиск источников по запросу в выбранных онлайн-библиотеках
        
#         Args:
#             query (str): Поисковой запрос
#             source (str): Источник для поиска ("all", "scholar", "elibrary", "scopus", "cyberleninka")
#             max_results (int): Максимальное количество результатов
            
#         Returns:
#             list: Список найденных библиографических элементов
#         """
#         results = []
        
#         if source == "all" or source == "scholar":
#             try:
#                 scholar_results = OnlineSearch._search_scholar(query, max_results)
#                 results.extend(scholar_results)
#             except Exception as e:
#                 print(f"Ошибка при поиске в Google Scholar: {e}")
        
#         if source == "all" or source == "elibrary":
#             try:
#                 elibrary_results = OnlineSearch._search_elibrary(query, max_results)
#                 results.extend(elibrary_results)
#             except Exception as e:
#                 print(f"Ошибка при поиске в eLIBRARY.RU: {e}")
        
#         if source == "all" or source == "scopus":
#             try:
#                 scopus_results = OnlineSearch._search_scopus(query, max_results)
#                 results.extend(scopus_results)
#             except Exception as e:
#                 print(f"Ошибка при поиске в Scopus: {e}")
        
#         if source == "all" or source == "cyberleninka":
#             try:
#                 cyberleninka_results = OnlineSearch._search_cyberleninka(query, max_results)
#                 results.extend(cyberleninka_results)
#             except Exception as e:
#                 print(f"Ошибка при поиске в КиберЛенинка: {e}")
        
#         # Ограничиваем количество результатов
#         return results[:max_results]
    
#     @staticmethod
#     def _search_scholar(query, max_results=5):
#         """
#         Поиск в Google Scholar
        
#         Args:
#             query (str): Поисковой запрос
#             max_results (int): Максимальное количество результатов
            
#         Returns:
#             list: Список найденных библиографических элементов
#         """
#         base_url = "https://scholar.google.com/scholar"
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
#         }
        
#         params = {
#             'q': query,
#             'hl': 'ru',
#             'as_sdt': '0,5',
#             'num': max_results
#         }
        
#         response = requests.get(base_url, headers=headers, params=params)
        
#         if response.status_code != 200:
#             raise Exception(f"Ошибка запроса: {response.status_code}")
        
#         soup = BeautifulSoup(response.text, 'lxml')
#         results = []
        
#         for item in soup.select('.gs_ri')[:max_results]:
#             bibitem = BibliographyItem()
            
#             # Заголовок
#             title_elem = item.select_one('.gs_rt')
#             if title_elem:
#                 bibitem.title = title_elem.get_text(strip=True)
#                 # Удаляем [PDF], [КНИГА] и т.д. из заголовка
#                 bibitem.title = re.sub(r'^\[.*?\]\s*', '', bibitem.title)
            
#             # Авторы, журнал, издательство, год
#             details_elem = item.select_one('.gs_a')
#             if details_elem:
#                 details_text = details_elem.get_text(strip=True)
                
#                 # Авторы обычно идут до первого тире
#                 authors_parts = details_text.split('-', 1)
#                 if len(authors_parts) > 0:
#                     authors_text = authors_parts[0].strip()
#                     bibitem.authors = [a.strip() for a in authors_text.split(',')]
                
#                 # Год обычно указан в скобках
#                 year_match = re.search(r'\b(19|20)\d{2}\b', details_text)
#                 if year_match:
#                     bibitem.year = year_match.group(0)
                
#                 # Попытка извлечь журнал или издательство
#                 if len(authors_parts) > 1:
#                     source_text = authors_parts[1].strip()
                    
#                     # Если в тексте есть "Т." или "Vol.", это скорее всего журнал
#                     if re.search(r'\b[Тт]\.\s*\d+|\b[Vv]ol\.\s*\d+', source_text):
#                         bibitem.journal = source_text
#                         bibitem.type = 'article'
#                     else:
#                         bibitem.publisher = source_text
#                         bibitem.type = 'book'
            
#             # URL
#             link_elem = item.select_one('.gs_rt a')
#             if link_elem and 'href' in link_elem.attrs:
#                 bibitem.url = link_elem['href']
            
#             results.append(bibitem)
            
#         return results
    
#     @staticmethod
#     def _search_elibrary(query, max_results=5):
#         """
#         Поиск в eLIBRARY.RU
        
#         Args:
#             query (str): Поисковой запрос
#             max_results (int): Максимальное количество результатов
            
#         Returns:
#             list: Список найденных библиографических элементов
#         """
#         results = []
        
#         # Поиск в eLIBRARY требует авторизации, поэтому реализуем упрощенную версию
#         # В реальном проекте нужна более сложная логика с учетом авторизации
        
#         # Заглушка для демонстрации
#         if query.strip():
#             # Создаем несколько примеров найденных результатов
#             for i in range(min(3, max_results)):
#                 bibitem = BibliographyItem()
#                 bibitem.title = f"Результат поиска в eLIBRARY по запросу '{query}' #{i+1}"
#                 bibitem.authors = ["Автор А.А.", "Соавтор В.В."]
#                 bibitem.year = "2022"
#                 bibitem.journal = "Вестник науки"
#                 bibitem.type = "article"
#                 bibitem.is_rinc = True
                
#                 if i % 2 == 0:
#                     bibitem.is_vak = True
                
#                 results.append(bibitem)
        
#         return results
    
#     @staticmethod
#     def _search_scopus(query, max_results=5):
#         """
#         Поиск в Scopus
        
#         Args:
#             query (str): Поисковой запрос
#             max_results (int): Максимальное количество результатов
            
#         Returns:
#             list: Список найденных библиографических элементов
#         """
#         results = []
        
#         # Scopus требует API-ключ или авторизацию, поэтому реализуем упрощенную версию
#         # В реальном проекте нужен API-ключ Elsevier
        
#         # Заглушка для демонстрации
#         if query.strip():
#             # Создаем несколько примеров найденных результатов
#             for i in range(min(3, max_results)):
#                 bibitem = BibliographyItem()
#                 bibitem.title = f"Scopus search result for '{query}' #{i+1}"
#                 bibitem.authors = ["Smith J.K.", "Brown A.B."]
#                 bibitem.year = "2023"
#                 bibitem.journal = "International Journal of Science"
#                 bibitem.type = "article"
#                 bibitem.language = "en"
#                 bibitem.doi = f"10.1000/s00000-{100+i}"
                
#                 results.append(bibitem)
        
#         return results
    
#     @staticmethod
#     def _search_cyberleninka(query, max_results=5):
#         """
#         Поиск в КиберЛенинка
        
#         Args:
#             query (str): Поисковой запрос
#             max_results (int): Максимальное количество результатов
            
#         Returns:
#             list: Список найденных библиографических элементов
#         """
#         base_url = "https://cyberleninka.ru/search"
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
#         }
        
#         params = {
#             'q': query,
#             'page': 1
#         }
        
#         try:
#             response = requests.get(base_url, headers=headers, params=params)
            
#             if response.status_code != 200:
#                 return []
            
#             soup = BeautifulSoup(response.text, 'lxml')
#             results = []
            
#             for item in soup.select('.search-results .search-results__item')[:max_results]:
#                 bibitem = BibliographyItem()
                
#                 # Заголовок
#                 title_elem = item.select_one('h2.title')
#                 if title_elem:
#                     bibitem.title = title_elem.get_text(strip=True)
                
#                 # Авторы
#                 authors_elem = item.select('.authors .author')
#                 if authors_elem:
#                     bibitem.authors = [author.get_text(strip=True) for author in authors_elem]
                
#                 # Журнал
#                 journal_elem = item.select_one('.journal')
#                 if journal_elem:
#                     bibitem.journal = journal_elem.get_text(strip=True)
#                     bibitem.type = 'article'
                
#                 # Год
#                 year_match = re.search(r'\b(19|20)\d{2}\b', item.get_text())
#                 if year_match:
#                     bibitem.year = year_match.group(0)
                
#                 # URL
#                 link_elem = item.select_one('h2.title a')
#                 if link_elem and 'href' in link_elem.attrs:
#                     bibitem.url = 'https://cyberleninka.ru' + link_elem['href']
                
#                 # КиберЛенинка - источник РИНЦ
#                 bibitem.is_rinc = True
                
#                 results.append(bibitem)
                
#             return results
#         except Exception as e:
#             print(f"Ошибка при поиске в КиберЛенинка: {e}")
#             return []
    
#     @staticmethod
#     def get_full_info(item):
#         """
#         Получение полной информации о библиографическом элементе
#         на основе URL или DOI
        
#         Args:
#             item (BibliographyItem): Библиографический элемент для дополнения
            
#         Returns:
#             BibliographyItem: Дополненный библиографический элемент
#         """
#         # Если есть DOI, ищем информацию через Crossref API
#         if item.doi:
#             try:
#                 doi_info = OnlineSearch._get_doi_info(item.doi)
#                 if doi_info:
#                     # Обновляем недостающие поля
#                     if not item.title and 'title' in doi_info:
#                         item.title = doi_info['title'][0]
                    
#                     if not item.authors and 'author' in doi_info:
#                         item.authors = [f"{a.get('family', '')} {a.get('given', '')}" for a in doi_info['author']]
                    
#                     if not item.year and 'issued' in doi_info:
#                         dates = doi_info['issued'].get('date-parts', [[]])[0]
#                         if dates and len(dates) > 0:
#                             item.year = str(dates[0])
                    
#                     if not item.journal and 'container-title' in doi_info:
#                         item.journal = doi_info['container-title'][0]
#                         item.type = 'article'
                    
#                     if not item.volume and 'volume' in doi_info:
#                         item.volume = doi_info['volume']
                    
#                     if not item.issue and 'issue' in doi_info:
#                         item.issue = doi_info['issue']
                    
#                     if not item.pages and 'page' in doi_info:
#                         item.pages = doi_info['page']
                    
#                     if not item.publisher and 'publisher' in doi_info:
#                         item.publisher = doi_info['publisher']
#             except Exception as e:
#                 print(f"Ошибка при получении информации по DOI: {e}")
        
#         # Если есть URL, пытаемся извлечь информацию из веб-страницы
#         elif item.url:
#             try:
#                 # Реализация парсера для извлечения информации со страницы
#                 # Эта функциональность требует специфических парсеров для разных сайтов
#                 pass
#             except Exception as e:
#                 print(f"Ошибка при получении информации по URL: {e}")
        
#         return item
    
#     @staticmethod
#     def _get_doi_info(doi):
#         """
#         Получить метаданные DOI через Crossref API
        
#         Args:
#             doi (str): DOI идентификатор
            
#         Returns:
#             dict: Метаданные статьи или None в случае ошибки
#         """
#         url = f"https://api.crossref.org/works/{doi}"
#         headers = {
#             'User-Agent': 'БиблиоАналитика/1.0 (https://github.com/yourusername/biblioanalitics; mailto:your.email@example.com)'
#         }
        
#         try:
#             response = requests.get(url, headers=headers)
#             if response.status_code == 200:
#                 data = response.json()
#                 return data.get('message', {})
#             return None
#         except Exception as e:
#             print(f"Ошибка при обращении к Crossref API: {e}")
#             return None 