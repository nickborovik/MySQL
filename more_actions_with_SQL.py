import pymysql
from pymysql.cursors import DictCursor

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='123456',
    db='sys',
    charset='utf8mb4',
    cursorclass=DictCursor)

print('Welcome to guests DB. Enter option to continue: ')
option = ''

try:
    with connection.cursor() as cursor:
        while option != 'exit':
            print('\n- show: for showing current data in DB')
            print('- add: for adding new guest to DB')
            print('- edit: for editing data in DB')
            print('- del: for deleting data from DB')
            print('- exit: for exiting program\n')
            option = input()

            # showing all DB info with phone numbers
            if option == 'show':
                sql = 'SELECT * FROM `guests` LEFT JOIN `phones` USING (`guest_Id`)'
                cursor.execute(sql)
                result = cursor.fetchall()
                print(*result, sep='\n')

            # adding new line to DB with phones
            elif option == 'add':
                firstName = input('Input guest First Name: ')
                lastName = input('Input guest Last Name: ')
                email = input('Input guest Email: ')
                phones = input('Input guest Phones: (use space to separate them) ').split()

                sql = 'INSERT INTO `guests` (`guest_FirstName`, `guest_LastName`, `guest_Email`) VALUES (%s, %s, %s)'
                cursor.execute(sql, (firstName, lastName, email))
                connection.commit()

                sql = 'SELECT `guest_Id` FROM `guests` WHERE `guest_Email`=%s'
                cursor.execute(sql, email)
                result = cursor.fetchone()

                for phone in phones:
                    sql = 'INSERT INTO `phones` (`guest_Id`, `phone_Number`) VALUES (%s, %s)'
                    cursor.execute(sql, (result['guest_Id'], phone))
                    connection.commit()
                print('Success')

            # editing one of the fields in DB
            # elif option == 'edit':
            #     field = input('What field you want to edit? (select one: firstName, lastName, email, phone) ')
            #     if field == 'firstName':
            #         sql = 'UPDATE `guests` SET '

            # deleting guest from DB:
            elif option == 'delete':
                guestEmail = input('\nPlease enter guest email: ')
                sql = 'SELECT * FROM `guests` LEFT JOIN `phones` USING (`guest_Id`) WHERE `guest_Email`=%s'
                cursor.execute(sql, guestEmail)
                print('Here all records for this guest:')
                print(*cursor.fetchall(), sep='\n')
                action = input('Do you want to delete this guest? (y/n) ')
                if action == 'y' or action == 'Y':
                    sql = 'DELETE FROM `guests` WHERE `guest_Email`=%s'
                    cursor.execute(sql, guestEmail)
                    connection.commit()
                    print('Success')
            # case for 'else'
            else:
                pass
finally:
    connection.close()