import psycopg2
import matplotlib.pyplot as plt

# РАБОТАТЬ НЕ БУДЕТ, ТАК КАК ДАННЫЕ ПОДКЛЮЧЕНИЯ ИЗМЕНЕНЫ В ЦЕЛЯХ БЕЗОПАСНОСТИ

if __name__ == '__main__':
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

        get_top_safety_pick_cars_avrg_grade_sql_request = """SELECT AVG(average_grade) FROM top_safety_pick;"""
        cursor.execute(get_top_safety_pick_cars_avrg_grade_sql_request)
        top_safety_pick_cars_avrg = cursor.fetchall()[0][0]

        get_top_safety_pick_plus_cars_avrg_grade_sql_request = """SELECT AVG(average_grade) FROM top_safety_pick_plus;"""
        cursor.execute(get_top_safety_pick_plus_cars_avrg_grade_sql_request)
        top_safety_pick_plus_cars_avrg = cursor.fetchall()[0][0]

        get_other_cars_avrg_grade_sql_request = """SELECT AVG((small_overlap_front + moderate_overlap_front + side + headlights + front_crash + seat_belt_reminders + LATCH_ease_of_use) / 7)
        FROM test_results
        WHERE car_id NOT IN (SELECT car_id FROM top_safety_pick UNION SELECT car_id FROM top_safety_pick_plus);"""
        cursor.execute(get_other_cars_avrg_grade_sql_request)
        top_other_cars_avrg = cursor.fetchall()[0][0]

        groups_for_diogram = ["Top safety pick cars", "Top safety pick plus cars", "Other cars"]
        data = [top_safety_pick_cars_avrg, top_safety_pick_plus_cars_avrg, top_other_cars_avrg]
        plt.bar(groups_for_diogram, data)
        plt.title("Среднее значение средних отценок безопасности разных групп автомобилей")
        plt.show()
    except ConnectionError:
        print("Не удалось подключиться к базе данных")
