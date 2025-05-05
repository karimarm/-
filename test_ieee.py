#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

print("Запуск скрипта тестирования IEEE...")

def parse_ieee_authors(text):
    """
    Тестовая функция для разбора авторов в формате IEEE
    """
    print(f"Исходный текст: {text}")
    
    # Ищем авторов до кавычек
    quote_match = re.search(r'["«]', text)
    
    if quote_match:
        authors_block = text[:quote_match.start()].strip()
        print(f"Блок авторов: {authors_block}")
        
        # Заменяем "and" на запятую
        authors_block = re.sub(r'\s+and\s+', ', ', authors_block)
        print(f"После замены 'and': {authors_block}")
        
        # Разделяем авторов по запятым
        raw_authors = [a.strip() for a in authors_block.split(',') if a.strip()]
        print(f"Список авторов после разделения: {raw_authors}")
        
        processed_authors = []
        
        for raw_author in raw_authors:
            print(f"\nОбработка автора: {raw_author}")
            
            # 1. P. R. Smith (инициалы с пробелами)
            match = re.search(r'^([A-Z]\.\s+[A-Z]\.)\s+([A-Za-z-]+)$', raw_author)
            if match:
                author = f"{match.group(2)} {match.group(1)}"
                print(f"Соответствует паттерну 1: {author}")
                processed_authors.append(author)
                continue
            
            # 2. P.R. Smith (инициалы без пробела)
            match = re.search(r'^([A-Z]\.[A-Z]\.)\s+([A-Za-z-]+)$', raw_author)
            if match:
                author = f"{match.group(2)} {match.group(1)}"
                print(f"Соответствует паттерну 2: {author}")
                processed_authors.append(author)
                continue
            
            # 3. P. Smith (один инициал)
            match = re.search(r'^([A-Z]\.)\s+([A-Za-z-]+)$', raw_author)
            if match:
                author = f"{match.group(2)} {match.group(1)}"
                print(f"Соответствует паттерну 3: {author}")
                processed_authors.append(author)
                continue
            
            # 4. P R Smith (инициалы без точек)
            match = re.search(r'^([A-Z])\s+([A-Z])\s+([A-Za-z-]+)$', raw_author)
            if match:
                author = f"{match.group(3)} {match.group(1)}. {match.group(2)}."
                print(f"Соответствует паттерну 4: {author}")
                processed_authors.append(author)
                continue
            
            # 5. P Smith (один инициал без точки)
            match = re.search(r'^([A-Z])\s+([A-Za-z-]+)$', raw_author)
            if match:
                author = f"{match.group(2)} {match.group(1)}."
                print(f"Соответствует паттерну 5: {author}")
                processed_authors.append(author)
                continue
            
            print(f"Не соответствует ни одному паттерну, добавляем как есть: {raw_author}")
            processed_authors.append(raw_author)
        
        print(f"\nИтоговый список авторов: {processed_authors}")
        return processed_authors
    else:
        print("Не найдены кавычки для разделения секции авторов")
        return []

# Тестовые данные
test_cases = [
    'P. R. Smith, K. L. Jones, "Paper Title," IEEE Journal, vol. 12, no. 3, pp. 45-52, 2023.',
    'A. B. Johnson and C. D. Wilson, "Security Analysis of IoT Protocols," IEEE Trans. Network Security, vol. 35, no. 2, pp. 112-125, 2022.'
]

# Запуск тестов
for i, tc in enumerate(test_cases):
    print(f"\n\n=== Тест {i+1} ===")
    parse_ieee_authors(tc)

# Специальные тесты для отдельных авторов
print("\n\n=== Проверка отдельных авторов ===")
individual_authors = [
    "P. R. Smith",
    "K. L. Jones",
    "A. B. Johnson",
    "C. D. Wilson"
]

for author in individual_authors:
    print(f"\nТест автора: {author}")
    
    # 1. P. R. Smith (инициалы с пробелами)
    match = re.search(r'^([A-Z]\.\s+[A-Z]\.)\s+([A-Za-z-]+)$', author)
    if match:
        print(f"Соответствует паттерну 1: {match.group(2)} {match.group(1)}")
        continue
    
    # 2. P.R. Smith (инициалы без пробела)
    match = re.search(r'^([A-Z]\.[A-Z]\.)\s+([A-Za-z-]+)$', author)
    if match:
        print(f"Соответствует паттерну 2: {match.group(2)} {match.group(1)}")
        continue
    
    # 3. P. Smith (один инициал)
    match = re.search(r'^([A-Z]\.)\s+([A-Za-z-]+)$', author)
    if match:
        print(f"Соответствует паттерну 3: {match.group(2)} {match.group(1)}")
        continue
    
    print("Не соответствует ни одному паттерну") 