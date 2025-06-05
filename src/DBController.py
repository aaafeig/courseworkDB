import logging
import psycopg2
from .Config import Config
from .Utils import Utils
from logging import FileHandler
from abc import abstractmethod
from .interfaces import Controller

loger = logging.getLogger("log_utils")
file_handler = FileHandler("logs/controller.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s: %(message)s"
)
file_handler.setFormatter(file_formatter)
loger.addHandler(file_handler)
loger.setLevel(logging.DEBUG)

class ControllerImpl(Controller):

    """Абстрактный базовый класс, который хранит общие параметры"""

    def __init__(self, path_file='data/file_workers.json') -> None:
        self._path_file = path_file
        self._emps = []
        self._vacancies = Utils.reader_file(self.path_file)
        try:
            self._conn = psycopg2.connect(**Config.config())
            self._cur = self._conn.cursor()
        except Exception as e:
            print(f"Ошибка при подключении к базе данных: {e}")

    @property
    def vacancies(self) -> list[dict]:
        return self._vacancies

    @vacancies.setter
    def vacancies(self, new_vacancies: list[dict]):
        self._vacancies = new_vacancies

    @property
    def conn(self) -> psycopg2.extensions.connection:
        return self._conn

    @property
    def cur(self) -> psycopg2.extensions.cursor:
        return self._cur

    @property
    def path_file(self) -> str:
        return self._path_file

    @property
    def emps(self) -> list[dict]:
        return self._emps

    @emps.setter
    def emps(self, new_emps: list[dict]) -> None:
        self._emps = new_emps

class DBControllerEmployers(ControllerImpl):


    def _create_table(self) -> None:
        try:
            with self.conn:
                self.cur.execute("""
                        CREATE TABLE IF NOT EXISTS employers (
                            emp_id SERIAL,
                            name_employer VARCHAR(100) NOT NULL
                        )
                    """)
        except Exception as e:
            print(f"Ошибка при создании таблицы: {e}")


    def save(self) -> None:
        self.emps = Utils._uniq(self.path_file)
        self._create_table()
        try:
            with self.conn:
                for emp in self.emps:
                    self.cur.execute("INSERT INTO employers (name_employer) VALUES (%s)",
                 (emp,))
                self.conn.commit()
            print("Работодатели сохранены")
        except Exception as e:
            print(f"Ошибка при сохранении работодателей: {e}")



class DBControllerVacancies(ControllerImpl):

    def _create_table(self) -> None:
        try:
            with self.conn:
                self.cur.execute("""CREATE TABLE IF NOT EXISTS vacancies (
            vacancy_id VARCHAR(30) PRIMARY KEY,
            name_employer VARCHAR(100),
            title VARCHAR(100) NOT NULL,
            description TEXT, 
            salary_from INTEGER,
            salary_to INTEGER,
            currency VARCHAR(3),
            url VARCHAR(150)
        )
        """)
        except Exception as e:
            print(f"Ошибка при создании таблицы: {e}")


    def save(self) -> None:
        self._create_table()
        try:
            with self.conn:
                for vacancy in self.vacancies:
                    salary = vacancy.get('salary', {})
                    self.cur.execute("INSERT INTO vacancies (vacancy_id, name_employer, title, description, salary_from, salary_to, currency, url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                                 (vacancy.get('id'), vacancy.get('employer'), vacancy.get('name'), vacancy.get('description'),
                                  salary.get('from'), salary.get('to'),
                                  salary.get('currency'), vacancy.get('url')))
                self.conn.commit()
            print("Вакансии сохранены")
        except Exception as e:
            print(f"Ошибка при сохранении вакансий: {e}")

