from abc import ABC, abstractmethod
import psycopg2

class Parser(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def load_vacancies(self):
        pass


class Controller(ABC):
    
    @abstractmethod
    def __init__(self) -> None:
        pass
    
    @abstractmethod
    def _create_table(self) -> None:
        pass

    @abstractmethod
    @property
    def vacancies(self) -> list[dict]:
        pass

    @abstractmethod
    @vacancies.setter
    def vacancies(self, new_vacancies: list[dict]):
        pass 

    @abstractmethod
    @property
    def conn(self) -> psycopg2.extensions.connection:
        pass

    @abstractmethod
    @property
    def cur(self) -> psycopg2.extensions.cursor:
        pass

    @abstractmethod
    @property
    def path_file(self) -> str:
        pass

    @abstractmethod
    @property
    def emps(self) -> list[dict]:
        pass

    @abstractmethod
    @emps.setter
    def emps(self, new_emps: list[dict]) -> None:
        pass

class Manager(ABC):
    

    @abstractmethod
    def get_companies_and_vacancies_count(self):
        pass

    @abstractmethod
    def get_all_vacancies(self):
        pass

    @abstractmethod
    def get_avg_salary(self):
        pass

    @abstractmethod
    def get_vacancies_with_higher_salary(self):
        pass

    @abstractmethod
    def get_vacancies_with_keyword(self):
        pass