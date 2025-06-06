# Job Vacancy Analytics System

## 📋 Описание проекта
Система для сбора, хранения и анализа вакансий с сайта HeadHunter. Проект позволяет автоматизировать процесс мониторинга вакансий от крупнейших IT-компаний России, сохранять данные в PostgreSQL и проводить различные виды анализа.

## 🎯 Возможности
- Автоматический сбор вакансий с HeadHunter API
- Хранение данных в PostgreSQL
- Анализ зарплат и вакансий
- Поиск по ключевым словам

## Документация

### Parser (API Client)
Отвечает за получение данных с HeadHunter API:
```python
class HeadHunterAPI:
    def load_vacancies() -> None
        """Загружает вакансии в файл"""
```

### Database Manager
Управляет операциями с базой данных:
```python
class DatabaseManager:
    def get_companies_and_vacancies_count() -> List[Dict]
        """Возвращает список компаний и количество их вакансий"""

    def get_all_vacancies() -> List[Dict]
        """Возвращает все вакансии с деталями"""

    def get_avg_salary() -> float
        """Возвращает среднюю зарплату"""

    def get_vacancies_with_higher_salary() -> List[Dict]
        """Возвращает вакансии с зарплатой выше средней"""

    def get_vacancies_with_keyword(keyword: str) -> List[Dict]
        """Поиск вакансий по ключевому слову"""
```

## 🚀 Установка и настройка

### Предварительные требования
- Python 3.10+
- PostgreSQL 12+
- Poetry (менеджер пакетов)

### Установка
1. Клонируйте репозиторий:
```bash
git clone https://github.com/aaafeig/courseworkDB
cd courseworkDB
```

2. Установите зависимости:
```bash
poetry install
```

3. Создайте файл конфигурации `.ini`:
```ini
DB_NAME=your_database
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

## 💻 Использование

### Загрузка вакансий
```python
from src.API import HeadHunterAPI
from src.DBmanager import DatabaseManager

# Создаем экземпляр парсера
parser = HeadHunterAPI("vacancies.json")

# Загружаем вакансии
parser.load_vacancies()

# Работаем с базой данных
db = DatabaseManager()

# Получаем статистику по компаниям
companies_stats = db.get_companies_and_vacancies_count()

# Получаем среднюю зарплату
avg_salary = db.get_avg_salary()

# Ищем вакансии по ключевому слову
python_vacancies = db.get_vacancies_with_keyword("Python")
```

## 🔧 Технологии
- Python 3.10+
- PostgreSQL
- requests
- psycopg2
- Poetry

⭐️ Если вам понравился проект, не забудьте поставить звездочку на GitHub!
