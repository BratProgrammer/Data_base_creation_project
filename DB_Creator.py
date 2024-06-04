import psycopg2

import Parser
    
# Метод создания бд
def create_data_base():
    try:
        # Подключение к базе университета (ПАРОЛЬ и ИМЯ ПОЛЬЗОВАТЕЛЯ ИЗМЕНЕНЫ!!! Host, port, database то же. На всякий случай)
        connection = psycopg2.connect(user='некое имя пользователя',  # Имя пользователя (ИЗМЕНЕНО)
                            password='некий пароль',  # Пароль для пользователя (ИЗМЕНЕНО)
                            host='111.125.211.305',  # Адрес (ИЗМЕНЕНО)
                            port='6783',  # Порт (ИЗМЕНЕНО)
                            database='база, тоже некая')  # Имя БД (ИЗМЕНЕНО)

        conn_string = "postgres://(некое имя пользователя):(некий пароль)@111.125.211.305:6783/(база, тоже некая)"
        connection = psycopg2.connect(conn_string)
        cursor = connection.cursor()
        create_cars_table_sql_request= """CREATE TABLE cars (
                                        car_id integer PRIMARY KEY,
                                        model varchar NOT NULL,
                                        brand varchar NOT NULL,
                                        car_type varchar NOT NULL,
                                        year_of_create integer NOT NULL,
                                        UNIQUE (model, brand, car_type, year_of_create)
                                        );"""
        create_test_results_table_sql_request = """CREATE TABLE test_results (
                                                        car_id integer PRIMARY KEY,
                                                        small_overlap_front integer,
                                                        moderate_overlap_front integer,
                                                        side integer,
                                                        headlights integer,
                                                        front_crash integer,
                                                        seat_belt_reminders integer,
                                                        LATCH_ease_of_use integer
                                                        );"""

        create_grades_table_sql_request = """CREATE TABLE grades (
                                            grade_int integer PRIMARY KEY,
                                            grade_symbol varchar NOT NULL,
                                            UNIQUE (grade_symbol, grade_int)
                                            );"""

        create_top_safety_pick_table_sql_request = """CREATE TABLE top_safety_pick (
                                                        car_id integer PRIMARY KEY,
                                                        average_grade float NOT NULL
                                                        );"""

        create_top_safety_pick_plus_table_sql_request = """CREATE TABLE top_safety_pick_plus (
                                                                car_id integer PRIMARY KEY,
                                                                average_grade float NOT NULL
                                                                );"""

        # Cоздание таблиц
        cursor.execute(create_cars_table_sql_request)
        connection.commit()
        cursor.execute(create_test_results_table_sql_request)
        connection.commit()
        cursor.execute(create_grades_table_sql_request)
        connection.commit()
        cursor.execute(create_top_safety_pick_table_sql_request)
        connection.commit()
        cursor.execute(create_top_safety_pick_plus_table_sql_request)
        connection.commit()

        connection.close()
    except ConnectionError:
        print("Не удалось подключиться к базе данных")


def set_data_to_db(cars, cars_results, grades, top_safety_pick_cars, top_safety_pick_plus_cars):
    try:
        # Подключение к базе университета (ПАРОЛЬ и ИМЯ ПОЛЬЗОВАТЕЛЯ ИЗМЕНЕНЫ!!! Host, port, database то же. На всякий случай, инфобез как никак)
        connection = psycopg2.connect(user='некое имя пользователя',  # Имя пользователя (ИЗМЕНЕНО)
                                      password='некий пароль',  # Пароль для пользователя (ИЗМЕНЕНО)
                                      host='111.125.211.305',  # Адрес (ИЗМЕНЕНО)
                                      port='6783',  # Порт (ИЗМЕНЕНО)
                                      database='база, тоже некая')  # Имя БД (ИЗМЕНЕНО)

        conn_string = "postgres://(некое имя пользователя):(некий пароль)@111.125.211.305:6783/(база, тоже некая)"
        connection = psycopg2.connect(conn_string)
        cursor = connection.cursor()
        for i in range(len(cars)):
            add_car_request = f"""INSERT INTO cars(car_id, model, brand, car_type, year_of_create) VALUES({i + 1}, '{str(cars[i]["model"]).strip()}', '{cars[i]["brand"]}', '{cars[i]["type"]}', {int(cars[i]["year"])});"""
            cursor.execute(add_car_request)
            connection.commit()

        for i in range(len(cars_results)):
            add_car_results_request = f"""INSERT INTO test_results
            (car_id, small_overlap_front, moderate_overlap_front, side, headlights, front_crash, seat_belt_reminders, LATCH_ease_of_use)
            VALUES({i + 1}, '{cars_results[i]["Small overlap front"]}', '{cars_results[i]["Moderate overlap front"]}', '{cars_results[i]["Side"]}', '{cars_results[i]["Headlights"]}', '{cars_results[i]["Front crash prevention: pedestrian"]}', '{cars_results[i]["Seat belt reminders"]}', '{cars_results[i]["LATCH ease of use"]}');"""
            cursor.execute(add_car_results_request)
            connection.commit()

        for i in range(len(grades)):
            add_grade_request = f"""INSERT INTO grades (grade_int, grade_symbol) VALUES({i}, '{grades[i]}');"""
            cursor.execute(add_grade_request)
            connection.commit()

        for i in range(len(top_safety_pick_cars)):
            add_top_safety_pick_car_request = f"""INSERT INTO top_safety_pick (car_id, average_grade) VALUES({top_safety_pick_cars[i]['car_id']}, '{top_safety_pick_cars[i]['average']}');"""
            cursor.execute(add_top_safety_pick_car_request)
            connection.commit()

        for i in range(len(top_safety_pick_plus_cars)):
            add_top_safety_pick_plus_car_request = f"""INSERT INTO top_safety_pick_plus (car_id, average_grade) VALUES({top_safety_pick_plus_cars[i]['car_id']}, '{top_safety_pick_plus_cars[i]['average']}');"""
            cursor.execute(add_top_safety_pick_plus_car_request)
            connection.commit()

        connection.close()
    except ConnectionError:
        print("Не удалось подключиться к базе данных")


if __name__ == '__main__':
    create_data_base()
    cars, cars_results, grades, top_safety_pick_cars, top_safety_pick_plus_cars = Parser.get_data_from_site()
    set_data_to_db(cars, cars_results, grades, top_safety_pick_cars, top_safety_pick_plus_cars)

