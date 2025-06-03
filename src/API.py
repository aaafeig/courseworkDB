import requests
import json

from .interfaces import Parser
class HH(Parser):

    """Класс для парсинга вакансий с сайта HH.ru"""

    def __init__(self, file_worker: str) -> None:

        """Инициализация класса"""

        self.url = "https://api.hh.ru/vacancies"
        self.headers = {"User-Agent": "HH-User-Agent"}
        self.params = {"text": "", "page": 0, "per_page": 100, "only_with_salary": True, "locale": "RU", "salary_currency": "RUR"}
        self.vacancies = []
        self.file_worker = file_worker
        self.employer_ids = ['1057',    # Лаборатория Касперского
            '1740',    # Яндекс
            '84585',   # Битрикс24
            '64174',   # 2ГИС
            '2324020', # Банк Точка
            '87021',   # Яндекс Маркет
            '15478',   # VK
            '41862',   # Контур
            '4934'  ]

    def _get_response(self) -> None:

        self.vacancies = []

        for employer_id in self.employer_ids:
            self.params["page"] = 0
            self.params["employer_id"] = employer_id
            while self.params["page"] < 5:
                response = requests.get(self.url, headers=self.headers, params=self.params)
                if response.status_code != 200:
                    print(f"Ошибка при запросе: {response.status_code}")
                    print(response.text)
                    break

                data = response.json()
                items = data.get("items", [])
                for item in items:
                    if item.get('salary', {}).get('currency') == "RUR":
                        filtered_items = {
                        'id': item.get('id'),
                        'name': item.get('name'),
                        'salary': {
                            'from': item.get('salary', {}).get('from'),
                            'to': item.get('salary', {}).get('to'),
                            'currency': item.get('salary', {}).get('currency')
                        },
                        "description": item.get("snippet", {}).get('responsibility'),
                        'employer': item.get('employer', {}).get('name'),
                        'url': item.get('alternate_url')
                        }
                        self.vacancies.append(filtered_items)
                    else:
                        continue
                self.params["page"] += 1

    def load_vacancies(self) -> None:
        self._get_response()
        with open(self.file_worker, "w", encoding="utf-8") as file:
            json.dump(self.vacancies, file, ensure_ascii=False, indent=2)
        print("Загрузка завершена")
