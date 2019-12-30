import psycopg2 as pg

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
    with pg.connect(connect_string) as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT table_name FROM information_schema.tables
        WHERE table_schema = 'public'""")
            for table in cur.fetchall():
                print(table)


def read_dbs():
    sql = '''SELECT datname FROM pg_database;'''
    with pg.connect(connect_string) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            for db in cur.fetchall():
                print(db)

def create_table(table_name):
    sql = f'''CREATE TABLE {table_name} (
                id integer primary key,
                name varchar(20),
                email varchar(20)
            );
    '''
    print(sql)
    try:
        conn = pg.connect(connect_string) # DB연결(로그인)
        cur = conn.cursor() # DB 작업할 지시자 정하기
        cur.execute(sql) # sql 문을 실행
        
        # DB에 저장하고 마무리
        conn.commit()
        conn.close()
    except pg.OperationalError as e:
        print(e)

def main():
    print("pg!")
    read_dbs()
    create_table("student")
    read_tables()


if __name__ == ("__main__"):
    main()