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
                sql = 'SELECT * FROM guests LEFT JOIN phones USING (guest_id)'
                cursor.execute(sql)
                result = cursor.fetchall()
                print(*result, sep='\n')

            # adding new line to DB with phones
            elif option == 'add':
                first_name = input('Input guest First Name: ')
                last_name = input('Input guest Last Name: ')
                email = input('Input guest Email: ')
                phones = input('Input guest Phones: (use space to separate them) ').split()

                sql = 'INSERT INTO guests (first_name, last_name, email) VALUES (%s, %s, %s)'
                cursor.execute(sql, (first_name, last_name, email))
                connection.commit()

                sql = 'INSERT INTO phones (guest_id, phone_number) VALUES '

                for phone in phones:
                    if phone == phones[-1]:
                        sql += '(LAST_INSERT_ID(), {})'.format(phone)
                    else:
                        sql += '(LAST_INSERT_ID(), {}), '.format(phone)
                cursor.execute(sql)
                connection.commit()
                print('Success')

            # editing one of the fields in DB
            elif option == 'edit':
                sql = 'SELECT * FROM guests LEFT JOIN phones USING (guest_id)'
                cursor.execute(sql)
                result = cursor.fetchall()
                print(*result, sep='\n')

                guest_id = input('What guest you want to edit? (enter guest ID) ')
                sql = 'SELECT * FROM guests LEFT JOIN phones USING (guest_id) WHERE guest_id=%s'
                cursor.execute(sql, guest_id)
                print(*cursor.fetchall(), sep='\n')

                field = input('What field you want to edit? (select one: first_name, last_name, email) ')
                if field == 'first_name' or field == 'last_name' or field == 'email':
                    value = input('Enter new value for this field: ')
                    sql = 'UPDATE guests SET {}=%s WHERE guest_id=%s'.format(field)
                    cursor.execute(sql, (value, guest_id))
                    connection.commit()
                    print('Success')
                else:
                    print('Wrong input, try again!')

            # deleting guest from DB:
            elif option == 'del':
                email = input('\nPlease enter guest email: ')
                sql = 'SELECT * FROM guests LEFT JOIN phones USING (guest_id) WHERE email=%s'
                cursor.execute(sql, email)
                print('Here all records for this guest:')
                print(*cursor.fetchall(), sep='\n')
                action = input('Do you want to delete this guest? (y/n) ')
                if action == 'y' or action == 'Y':
                    sql = 'DELETE FROM guests WHERE email=%s'
                    cursor.execute(sql, email)
                    connection.commit()
                    print('Success')

            # case for anything else
            else:
                pass
finally:
    connection.close()