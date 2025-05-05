#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from utils.reference_parser import ReferenceParser
from models.bibliography_item import BibliographyItem
import requests
import json

def debug_ieee_parsing():
    """Отладка разбора IEEE ссылок"""
    
    # Тестовые примеры IEEE формата
    test_cases = [
        'P. R. Smith, K. L. Jones, "Paper Title," IEEE Journal, vol. 12, no. 3, pp. 45-52, 2023.',
        'A. B. Johnson and C. D. Wilson, "Security Analysis of IoT Protocols," IEEE Trans. Network Security, vol. 35, no. 2, pp. 112-125, 2022.'
    ]
    
    for i, test_case in enumerate(test_cases):
        print(f"\n\n=== TEST CASE {i+1} ===")
        print(f"Input: {test_case}")
        
        # Разбор отдельных авторов
        print("\nDEBUG: Processing individual author patterns:")
        
        # Извлекаем блок авторов
        quote_match = re.search(r'["«]', test_case)
        if quote_match:
            authors_block = test_case[:quote_match.start()].strip()
            print(f"Authors block: |{authors_block}|")
            
            # Нормализуем "and"
            authors_block = re.sub(r'\s+and\s+', ', ', authors_block)
            print(f"After 'and' replacement: |{authors_block}|")
            
            # Разделяем авторов по запятым
            raw_authors = [a.strip() for a in authors_block.split(',') if a.strip()]
            print(f"Raw authors: {raw_authors}")
            
            # Проверка каждого автора
            for author in raw_authors:
                print(f"\nTesting author: |{author}|")
                
                # Проверка шаблонов
                pattern1 = r'^([A-Z]\.)\s+([A-Z]\.)\s+([A-Za-z-]+)$'
                match1 = re.search(pattern1, author)
                print(f"Pattern 1 (P. R. Smith): {bool(match1)}")
                if match1:
                    print(f"  Groups: {match1.groups()}")
                    print(f"  Result: {match1.group(3)} {match1.group(1)} {match1.group(2)}")
                
                pattern2 = r'^([A-Z]\.[A-Z]\.)\s+([A-Za-z-]+)$'
                match2 = re.search(pattern2, author)
                print(f"Pattern 2 (P.R. Smith): {bool(match2)}")
                if match2:
                    print(f"  Groups: {match2.groups()}")
                    print(f"  Result: {match2.group(2)} {match2.group(1)}")
                
                pattern3 = r'^([A-Z]\.)\s+([A-Za-z-]+)$'
                match3 = re.search(pattern3, author)
                print(f"Pattern 3 (P. Smith): {bool(match3)}")
                if match3:
                    print(f"  Groups: {match3.groups()}")
                    print(f"  Result: {match3.group(2)} {match3.group(1)}")
            
            # Полное тестирование преобразования
            print("\nFull conversion test:")
            
            processed_authors = []
            for author in raw_authors:
                # Печатаем первые два символа для проверки на пробелы
                print(f"First 3 characters of |{author}|: |{author[:3]}|")
                
                # Используем несколько различных паттернов для большей гибкости
                
                # 1. Два инициала и фамилия
                # P. R. Smith
                match = re.search(r'^([A-Z]\.)\s+([A-Z]\.)\s+([A-Za-z-]+)$', author)
                if match:
                    result = f"{match.group(3)} {match.group(1)} {match.group(2)}"
                    processed_authors.append(result)
                    print(f"Matched pattern 1: {result}")
                    continue
                
                # 2. Два инициала без пробела между ними
                # P.R. Smith
                match = re.search(r'^([A-Z]\.[A-Z]\.)\s+([A-Za-z-]+)$', author)
                if match:
                    result = f"{match.group(2)} {match.group(1)}"
                    processed_authors.append(result)
                    print(f"Matched pattern 2: {result}")
                    continue
                
                # 3. Один инициал и фамилия
                # P. Smith
                match = re.search(r'^([A-Z]\.)\s+([A-Za-z-]+)$', author)
                if match:
                    result = f"{match.group(2)} {match.group(1)}"
                    processed_authors.append(result)
                    print(f"Matched pattern 3: {result}")
                    continue
                
                # Если не совпадает ни один шаблон, пробуем более общий подход
                words = author.split()
                if len(words) >= 2 and words[0][-1] == '.':
                    if len(words) >= 3 and words[1][-1] == '.':
                        # Похоже на два инициала и фамилию
                        result = f"{' '.join(words[2:])} {words[0]} {words[1]}"
                        processed_authors.append(result)
                        print(f"Matched general pattern with 2 initials: {result}")
                        continue
                    else:
                        # Похоже на один инициал и фамилию
                        result = f"{' '.join(words[1:])} {words[0]}"
                        processed_authors.append(result)
                        print(f"Matched general pattern with 1 initial: {result}")
                        continue
                
                # Если ничего не сработало, добавляем как есть
                processed_authors.append(author)
                print(f"No match, keeping as is: {author}")
            
            print(f"\nFinal processed authors: {processed_authors}")
        else:
            print("No quotes found to delimit authors block")
        
        # Пробуем полный парсинг через ReferenceParser
        print("\nFull parsing test:")
        item = BibliographyItem(test_case)
        ReferenceParser._parse_ieee(test_case, item)
        
        print("Parsed item:")
        print(f"  Authors: {item.authors}")
        print(f"  Title: {item.title}")
        print(f"  Journal: {item.journal}")
        print(f"  Year: {item.year}")
        print(f"  Type: {item.type}")
        
def test_google_scholar_api():
    """Тестирование API Google Scholar"""
    api_key = "68177d586e93f8e402be3d8c"
    query = "ГОСТ библиография"
    
    # Формирование URL запроса
    url = "https://api.serpdog.io/scholar"
    params = {
        'api_key': api_key,
        'q': query,
        'num': 5,
        'hl': 'ru'
    }
    
    try:
        # Выполнение запроса
        response = requests.get(url, params=params)
        
        # Проверка статуса ответа
        if response.status_code == 200:
            print("✅ API работает! Статус ответа: 200 OK")
            
            # Парсинг ответа
            data = response.json()
            
            # Проверка содержимого ответа
            if 'scholar_results' in data:
                results = data['scholar_results']
                print(f"Найдено результатов: {len(results)}")
                
                # Вывод первого результата для примера
                if results:
                    first_result = results[0]
                    print("\nПример первого результата:")
                    print(f"Заголовок: {first_result.get('title', 'Нет данных')}")
                    print(f"Ссылка: {first_result.get('title_link', 'Нет данных')}")
                    print(f"Данные авторов: {first_result.get('displayed_link', 'Нет данных')}")
            else:
                print("⚠️ Ответ API не содержит результатов поиска.")
                print("Содержимое ответа:")
                print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print(f"❌ Ошибка API! Код ответа: {response.status_code}")
            print("Содержимое ответа:")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Ошибка при выполнении запроса: {e}")

if __name__ == "__main__":
    debug_ieee_parsing()
    test_google_scholar_api() 