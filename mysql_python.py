import pymysql
from pymysql.cursors import DictCursor

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='123456',
    db='sys',
    charset='utf8mb4',
    cursorclass=DictCursor)

try:
    with connection.cursor() as cursor:
        answer = input("Would you like to add new guest to DB? (y/n) ")
        if answer == 'y' or answer == 'Y':
            first_name = input('Input guest First Name: ')
            last_name = input('Input guest Last Name: ')
            email = input('Input guest Email: ')
            phones = input('Input guest Phones: (use space to separate them) ').split()

            sql = "INSERT INTO guests (first_name, last_name, email) VALUES (%s, %s, %s)"
            cursor.execute(sql, (first_name, last_name, email))
            connection.commit()

            sql = "INSERT INTO phones (guest_id, phone_number) VALUES "

            for phone in phones:
                if phone == phones[-1]:
                    sql += '(LAST_INSERT_ID(), {})'.format(phone)
                else:
                    sql += '(LAST_INSERT_ID(), {}), '.format(phone)
            cursor.execute(sql)
            connection.commit()

        else:
            print('Ok. here what you have in DB: ')

    with connection.cursor() as cursor:
        sql = "SELECT * FROM guests LEFT JOIN phones USING (guest_id)"
        cursor.execute(sql)
        result = cursor.fetchall()
        print(*result, sep='\n')
finally:
    connection.close()