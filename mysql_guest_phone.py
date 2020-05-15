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
        ans = input("Would you like to add new guest to DB? (y/n) ")
        if ans == 'y' or ans == 'Y':
            firstName = input('Input guest First Name: ')
            lastName = input('Input guest Last Name: ')
            email = input('Input guest Email: ')
            phones = input('Input guest Phones: (use space to separate them) ').split()

            sql = "INSERT INTO `guests` (`guest_FirstName`, `guest_LastName`, `guest_Email`) VALUES (%s, %s, %s)"
            cursor.execute(sql, (firstName, lastName, email))
            connection.commit()

            sql = "SELECT `guest_Id` FROM `guests` WHERE `guest_Email`=%s"
            cursor.execute(sql, email)
            result = cursor.fetchone()

            for phone in phones:
                sql = "INSERT INTO `phones` (`guest_Id`, `phone_Number`) VALUES (%s, %s)"
                cursor.execute(sql, (result['guest_Id'], phone))
                connection.commit()

        else:
            print('Ok. here what you have in DB: ')

    with connection.cursor() as cursor:
        sql = "SELECT * FROM `guests` LEFT JOIN `phones` USING (`guest_Id`)"
        cursor.execute(sql)
        result = cursor.fetchall()
        print(*result, sep='\n')
finally:
    connection.close()