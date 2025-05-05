#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.reference_parser import ReferenceParser
from models.bibliography_item import BibliographyItem

def test_reference_parsing():
    """Тестирование распознавания библиографических ссылок"""
    
    # Тестовые данные - ссылки в разных форматах с разными вариантами инициалов
    test_references = [
        # ГОСТ с инициалами без пробела
        "Иванов А.В., Петров В.М. Название книги. М.: Издательство, 2022. 300 с.",
        
        # ГОСТ с инициалами, разделенными пробелами
        "Иванов А. В., Петров В. М. Название книги. М.: Издательство, 2022. 300 с.",
        
        # ГОСТ с одним автором и инициалами через пробел
        "Сидоров С. И. Название статьи // Журнал. 2021. Т. 10. № 2. С. 15-28.",
        
        # APA с инициалами через пробел
        "Smith, J. K., Brown, A. B. (2020). Title of the article. Journal of Science, 15(2), 123-145.",
        
        # MLA с несколькими авторами
        "Doe, John K., and Jane A. Smith. \"Title of the Book.\" Publisher, 2019.",
        
        # Chicago с инициалами через пробел
        "Johnson, M. L., and Wilson, B. K. \"Article Title,\" Journal Name, 25(3), 2018.",
        
        # IEEE с несколькими авторами и инициалами перед фамилией
        "P. R. Smith, K. L. Jones, \"Paper Title,\" IEEE Journal, vol. 12, no. 3, pp. 45-52, 2023.",
        
        # Еще один пример IEEE
        "A. B. Johnson and C. D. Wilson, \"Security Analysis of IoT Protocols,\" IEEE Trans. Network Security, vol. 35, no. 2, pp. 112-125, 2022."
    ]
    
    # Вывод результатов
    print("Результаты распознавания библиографических ссылок:\n")
    
    for i, ref in enumerate(test_references):
        print(f"Ссылка {i+1}: {ref}")
        
        # Распознавание
        item = ReferenceParser.parse(ref)
        
        # Вывод результатов
        print(f"  Авторы: {item.authors}")
        print(f"  Название: {item.title}")
        print(f"  Год: {item.year}")
        print(f"  Тип: {item.type}")
        if item.journal:
            print(f"  Журнал: {item.journal}")
        if item.publisher:
            print(f"  Издательство: {item.publisher}")
        print()

if __name__ == "__main__":
    test_reference_parsing() 