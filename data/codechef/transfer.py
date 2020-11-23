import psycopg2

hostname = ''
username = ''
password = ''
database = 'd74uinm10v45m9'

myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )


cursor = myConnection.cursor()



# data = '''Drop table codechef'''
# cursor.execute(data)

data = ''' Create table codechef (
        index int,
        name char(156),
        link char(156),
        submitlink char(156),
        submittedSolutions int,
        accuracy float,
        statuslink char(156),
        difficulty char(156)
        )
        '''
cursor.execute(data)

f = open('codechef.csv', 'r')
cursor.copy_from(f , 'codechef', sep=',')
f.close()


myConnection.commit()

myConnection.close()