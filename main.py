from src.API import HH
from src.DBController import DBControllerEmployers, DBControllerVacancies,Controller

def main():
    # parser = HH('data/file_workers.json')
    # parser.load_vacancies()
    Controller()
    a = DBControllerEmployers()
    b = DBControllerVacancies()
    a.save()
    b.save()


if __name__ == "__main__":
    main()
