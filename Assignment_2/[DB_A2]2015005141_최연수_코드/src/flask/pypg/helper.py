import psycopg2 as pg
import psycopg2.extras
import re

# docker inside
docker_in = {
    'host': "postgres",
    'user': "dbuser",
    'dbname': "dbapp",
    'password': "1234"
}
# localhost == 127.0.0.1
# postgres://dbuser:1234@postgres/dbapp
# postgres://postgres:????@127.0.0.1/postgres
pg_local = {
    'host': "localhost", # localhost / 192.168.99.100
    'user': "postgres",  # dbuser
    'dbname': "postgres",  # dbapp
    'password': "1234"     # 1234
    #, 'port' : '54321'
}

db_connector = docker_in

connect_string = "host={host} user={user} dbname={dbname} password={password}".format(
    **db_connector)
print(connect_string)

def read_tables():
    tables = []
    with pg.connect(connect_string) as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT table_name FROM information_schema.tables
        WHERE table_schema = 'public'""")
            for table in cur.fetchall():
                tables.append(table)
    return tables


def read_dbs():
    sql = '''SELECT datname FROM pg_database;'''
    with pg.connect(connect_string) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            for db in cur.fetchall():
                print(db)


def call_table(table_name):
    try :
        conn = pg.connect(connect_string)
        cur = conn.cursor()
        with open('contact.csv','r') as f:
            next(f)
            cur.copy_from(f, f'{table_name}', sep=',')
            conn.commit()
            conn.close()
    except pg.OperationlError as e:
        print(e)




def create_table(table_name):
    sql = f'''CREATE TABLE if not exists {table_name} (
                name varchar(60),
                number varchar(60),
                PRIMARY KEY (name , number)
            )
    '''
    try:
        conn = pg.connect(connect_string)
        cur = conn.cursor()
        cur.execute(sql)

        conn.commit()
        conn.close()
    except pg.OperationalError as e:
        print(e)

def delete_table(table_name):
    sql = f'''DROP TABLE {table_name}
    '''
    try:
        conn = pg.connect(connect_string)
        cur = conn.cursor()
        cur.execute(sql)


        conn.commit()
        conn.close()
    except pg.OperationalError as e:
        print(e)

def select(table_name, name):
    sql = f'''SELECT name, number
              FROM {table_name}
              WHERE name LIKE \'{name}%\'  
    '''
    try:
        conn = pg.connect(connect_string)
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(sql)
        result = cur.fetchall()

        conn.commit()
        conn.close()
        return result
    except Exception as e:
        print(e)
        return []

def count(table_name, name):
    sql = f'''SELECT COUNT(*)
              FROM {table_name}
              WHERE name LIKE \'{name}%\'
    '''
    try:
        conn = pg.connect(connect_string)
        cur = conn.cursor()
        cur.execute(sql)

        result = cur.fetchall()
        conn.commit()
        conn.close()

        return result[0][0]
    except pg.OperationalError as e:
        print(e)

def count2(table_name, name,number):
    sql = f'''SELECT COUNT(*)
              FROM {table_name}
              WHERE number = \'{number}\' AND name = \'{name}\'
    '''
    try:
        conn = pg.connect(connect_string)
        cur = conn.cursor()
        cur.execute(sql)

        result = cur.fetchall()
        conn.commit()
        conn.close()

        return result[0][0]
    except pg.OperationalError as e:
        print(e)



def insert(table_name, name, number):
    sql = f'''INSERT INTO {table_name} 
              VALUES (  \'{name}\', \'{number}\');
           '''
    print(sql)
    try:
        conn = pg.connect(connect_string)
        cur = conn.cursor()
        cur.execute(sql)

        conn.commit()
        conn.close()

    except Exception as e:
        print(e)
        return []
    return 0


def delete(table_name,name):
    sql = f'''DELETE FROM {table_name}
              WHERE {table_name}.number = (SELECT number FROM {table_name} 
                                            WHERE name = \'{name}\' LIMIT 1)
              ;
        '''
    try:
        conn = pg.connect(connect_string)
        cur = conn.cursor()
        cur.execute(sql)

        conn.commit()
        conn.close()

    except Exception as e:
        print(e)
        return []
    return 0

def delete_for_upd(table_name, name, number):
    sql = f'''DELETE FROM {table_name}
              WHERE name = \'{name}\' AND number = \'{number}\';
        '''
    try:
        conn = pg.connect(connect_string)
        cur = conn.cursor()
        cur.execute(sql)

        conn.commit()
        conn.close()

    except Exception as e:
        print(e)
        return []
    return 0


def read_students(students):
    sql = f'''SELECT name,number FROM {students};
           '''
    print(sql)
    try:
        conn = pg.connect(connect_string) # DB연결(로그인)
        # cur = conn.cursor() # DB 작업할 지시자 정하기
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(sql) # sql 문을 실행
        result = cur.fetchall()         
        # DB에 저장하고 마무리
        conn.commit()
        conn.close()
        return result
    except Exception as e:
        print(e)
        return []            

