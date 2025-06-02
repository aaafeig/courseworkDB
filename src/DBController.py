import logging
import psycopg2
from .Config import Config
from .Utils import Utils
from logging import FileHandler
from abc import abstractmethod

loger = logging.getLogger("log_utils")
file_handler = FileHandler("logs/controller.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s: %(message)s"
)
file_handler.setFormatter(file_formatter)
loger.addHandler(file_handler)
loger.setLevel(logging.DEBUG)

class Controller:

    """Абстрактный базовый класс, который хранит общие параметры"""

    def __init__(self, path_file='data/file_workers.json'):
        self._path_file = path_file
        self._emps = []
        self._vacancies = Utils.reader_file(self.path_file)
        self._conn = psycopg2.connect(**Config.config())
        self._cur = self._conn.cursor()


    @abstractmethod
    def _create_table(self):
        pass

    @property
    def vacancies(self):
        return self._vacancies

    @vacancies.setter
    def vacancies(self, new_vacancies: list[dict]):
        self._vacancies = new_vacancies

    @property
    def conn(self):
        return self._conn

    @property
    def cur(self):
        return self._cur

    @property
    def path_file(self):
        return self._path_file

    @property
    def emps(self):
        return self._emps

class DBControllerEmployers(Controller):

    def _uniq(self):
        for i in Utils.reader_file(self.path_file):
            if i.get('employer') not in self.emps:
                self.emps.append(i.get('employer'))
            else:
                continue

        loger.debug(self.emps)


    def _create_table(self):
        with self.conn:
            self.cur.execute("""
                        CREATE TABLE IF NOT EXISTS employers (
                            emp_id SERIAL,
                            name_employer VARCHAR(100) NOT NULL
                        )
                    """)

    def save(self):
        self._uniq()
        self._create_table()
        with self.conn:
            for emp in self.emps:
                self.cur.execute("INSERT INTO employers (name_employer) VALUES (%s)",
                 (emp,))
            self.conn.commit()
        print("Работодатели сохранены")



class DBControllerVacancies(Controller):

    def _create_table(self):
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

    def save(self):
        self._create_table()
        with self.conn:
            for vacancy in self.vacancies:
                salary = vacancy.get('salary', {})
                self.cur.execute("INSERT INTO vacancies (vacancy_id, name_employer, title, description, salary_from, salary_to, currency, url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                                 (vacancy.get('id'), vacancy.get('employer'), vacancy.get('name'), vacancy.get('description'),
                                  salary.get('from'), salary.get('to'),
                                  salary.get('currency'), vacancy.get('url')))
            self.conn.commit()
        print("Вакансии сохранены")

