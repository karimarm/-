#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import sys
from utils.reference_parser import ReferenceParser
from models.bibliography_item import BibliographyItem

# Устанавливаем кодировку для вывода
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def test_parser():
    """Тестирование обновленного парсера библиографических ссылок"""
    
    # Список тестовых ссылок
    test_references = [
        # Статья с авторами после косой черты
        "Иванов А. А. Название статьи с авторами / А. А. Иванов, Б. Б. Петров // Название журнала. — 2023. — Т. 1. — № 2. — С. 45-50.",
        
        # Статья без авторов после косой черты
        "Иванов А. А. Название статьи без косой черты // Название журнала. — 2023. — Т. 1. — № 2. — С. 45-50.",
        
        # Статья с диапазоном страниц
        "Петров Б. Б. Статья с диапазоном страниц // Научный вестник. — 2022. — С. 123-145.",
        
        # Статья с одной страницей
        "Петров Б. Б. Статья с одной страницей // Научный вестник. — 2022. — С. 123.",
        
        # Автореферат диссертации с авторами после косой черты
        "Сидоров В. В. Название диссертации / В. В. Сидоров : автореф. дис. ... канд. тех. наук / В. В. Сидоров. — Москва, 2022. — 24 с.",
        
        # Веб-ресурс с авторами после косой черты
        "Антонов Г. Г. Название веб-ресурса / Г. Г. Антонов [Электронный ресурс]. — URL: https://example.com (дата обращения: 12.12.2023).",
        
        # Статья в формате IEEE с диапазоном страниц
        'A. Author, B. Author, "Title of paper," Journal Name, vol. 10, no. 2, pp. 45-50, 2023',
    ]
    
    # Парсинг и вывод результатов
    for i, ref in enumerate(test_references):
        print(f"\n\n=== ТЕСТ {i+1} ===")
        print(f"Ссылка:\n{ref}")
        print("-" * 50)
        
        # Определим формат
        format_type = ReferenceParser._detect_format(ref)
        print(f"Определенный формат: {format_type}")
        
        # Парсим ссылку
        item = ReferenceParser.parse(ref, format_type)
        
        # Выводим результаты
        print("\nРезультаты парсинга:")
        print(f"1. Авторы: {item.authors}")
        print(f"2. Название: '{item.title}'")
        print(f"3. Журнал: '{item.journal}'")
        print(f"4. Год: {item.year}")
        print(f"5. Том: {item.volume}")
        print(f"6. Номер: {item.issue}")
        print(f"7. Страницы: {item.pages}")
        print(f"8. Тип: {item.type}")
        
        if item.url:
            print(f"9. URL: {item.url}")
        if item.doi:
            print(f"10. DOI: {item.doi}")
        
        print("=" * 50)

if __name__ == "__main__":
    test_parser() 