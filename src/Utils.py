import json
import logging
from logging import FileHandler

loger = logging.getLogger("log_utils")
file_handler = FileHandler("logs/utils.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
loger.addHandler(file_handler)
loger.setLevel(logging.DEBUG)


class Utils:

    @staticmethod
    def reader_file(file_path: str) -> list[dict]:
        """Метод для сохранения данных из указанного файла в атрибут Controller`а"""

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print(f"Файл {file_path} содержит невалидный JSON. Будет возвращен пустой список.")
            return []

    @staticmethod
    def _uniq(path_file: str) -> list[dict]:
        """Метод для удаления дубликатов из списка"""

        emps = []
        for i in Utils.reader_file(path_file):
            if i.get("employer") not in emps:
                emps.append(i.get("employer"))
            else:
                continue

        loger.debug(emps)
        return emps
