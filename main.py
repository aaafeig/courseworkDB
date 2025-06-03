from src.API import HH
from src.DBController import DBControllerEmployers, DBControllerVacancies
from src.DBmanager import DBManager

def main():
    parse_vacancies()
    get_vacancies()

    while True:
        print("1. Получить список компаний и количество вакансий у каждой компании")
        print("2. Получить список всех вакансий с указанием названия компании, названия вакансии и зарплаты")
        print("3. Получить среднюю зарплату по всем вакансиям")
        print("4. Получить список всех вакансий, у которых зарплата выше средней")
        print("5. Получить список всех вакансий, в названии которых содержится переданное в метод слово")
        print("6. Выйти из программы")
        
        choice = input("Выберите действие: ")

        if choice == "1":
            print(DBManager().get_companies_and_vacancies_count())
        elif choice == "2":
            print(DBManager().get_all_vacancies())
        elif choice == "3":
            print(DBManager().get_avg_salary())
        elif choice == "4":
            print(DBManager().get_vacancies_with_higher_salary())
        elif choice == "5":
            print(DBManager().get_vacancies_with_keyword(input("Введите слово: ")))
        elif choice == "6":
            break
            

def get_vacancies():
    saver_employers = DBControllerEmployers()
    saver_vacancies = DBControllerVacancies()
    saver_employers.save()
    saver_vacancies.save()

def parse_vacancies():
    parser = HH('data/file_workers.json')
    parser.load_vacancies()


if __name__ == "__main__":
    main()
