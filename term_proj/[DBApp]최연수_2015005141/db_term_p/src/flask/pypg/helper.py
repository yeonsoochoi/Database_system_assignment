import psycopg2 as pg
import psycopg2.extras
import re,datetime

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
                local varchar(30),
                domain varchar(30),
                pwd varchar(30),
                name varchar(30),
                p_num varchar(30),
                lat varchar(20),
                lng varchar(20),
                PRIMARY KEY (local, domain),
                personid SERIAL 
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


def hosptable_from_api(table_name):
    sql = f'''CREATE TABLE if not exists {table_name} (
                    name varchar(150),
                    doctorcnt varchar(20),
                    address varchar(500),
                    latitude varchar(20),
                    longitude varchar(20),
                    mon_s int DEFAULT '8',
                    mon_e int DEFAULT '17',
                    tue_s int DEFAULT '8',
                    tue_e int DEFAULT '17',
                    wed_s int DEFAULT '8',
                    wed_e int DEFAULT '17',
                    thu_s int DEFAULT '8',
                    thu_e int DEFAULT '17',
                    fri_s int DEFAULT '8',
                    fri_e int DEFAULT '17',
                    sat_s int DEFAULT '8',
                    sat_e int DEFAULT '17',
                    sun_s int DEFAULT '8',
                    sun_e int DEFAULT '17',
                    hid SERIAL PRIMARY KEY
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


def phartable_from_api(table_name):
    sql = f'''CREATE TABLE if not exists {table_name} (
                        name varchar(100),
                        address varchar(310),
                        latitude varchar(20),
                        longitude varchar(20),
                        prescription varchar(5) DEFAULT 't',
                        pid SERIAL PRIMARY KEY
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





def insert_to_t(table_name,name, doctorcnt, address, latitude, longitude):
    sql = f'''INSERT INTO {table_name} 
              VALUES (  \'{name}\', \'{doctorcnt}\',\'{address}\',\'{latitude}\',\'{longitude}\');
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


def insert_to_p_t(table_name, name, address, latitude, longitude):
    sql = f'''INSERT INTO {table_name} 
              VALUES (  \'{name}\', \'{address}\' ,\'{latitude}\',\'{longitude}\');
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


def create_reservation(table_name):
    sql = f'''CREATE TABLE if not exists {table_name}(
                        inst_name varchar(100),
                        name varchar(100),
                        p_num varchar(20),
                        r_day int,
                        r_hour int,
                        r_minute int,
                        personid varchar(5),
                        prescription varchar(5) DEFAULT 'f',
                        rid SERIAL PRIMARY KEY
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


def create_subject(table_name):
    sql = f'''CREATE TABLE if not exists {table_name}(
                        hosp_name varchar(150),
                        subject varchar(20),
                        PRIMARY KEY (hosp_name, subject)
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

def create_star(table_name):
    sql = f'''CREATE TABLE if not exists {table_name}(
                        hosp_name varchar(150),
                        personid int
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


def update_star(table_name, hosp_name, personid):
    sql = f'''UPDATE {table_name} SET hosp_name = '{hosp_name}'
                WHERE personid = {personid};
    
    '''
    try:
        conn = pg.connect(connect_string) # DB연결(로그인)
        # cur = conn.cursor() # DB 작업할 지시자 정하기
        cur = conn.cursor()
        cur.execute(sql) # sql 문을 실행         
        # DB에 저장하고 마무리
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)

def insert_star(table_name,hosp_name, personid):
    sql = f'''INSERT INTO {table_name} 
              VALUES (  \'{hosp_name}\', {personid});
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




def search_subject(table_name,hosp_name):
    sql = f'''SELECT hosp_name,subject
              FROM {table_name}
              WHERE hosp_name = \'{hosp_name}\'  
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

def search_subject_sub(table_name,subject):
    sql = f'''SELECT hosp_name,subject
              FROM {table_name}
              WHERE subject = \'{subject}\'  
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



def add_subject(table_name,hosp_name,subject):
    sql = f'''INSERT INTO {table_name} 
              VALUES (  \'{hosp_name}\', \'{subject}\');
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




    
def reservation(table_name, inst_name, name,p_num, r_day , hour, minute,personid):
    sql = f'''INSERT INTO {table_name} 
              VALUES (  \'{inst_name}\',\'{name}\',\'{p_num}\',{r_day},{hour},{minute},\'{personid}\');
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




def login(table_name,local,domain,pwd):
    sql = f'''SELECT name,p_num
              FROM {table_name}
              WHERE local = \'{local}\' AND
                    domain = \'{domain}\' AND
                    pwd = \'{pwd}\'
'''
    try:
        conn = pg.connect(connect_string)
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(sql)
        
        result = cur.fetchall()
        print(result)
        conn.commit()
        conn.close()

        return result
    except pg.OperationalError as e:
        print(e)

def login_p(table_name,local,domain,pwd):
    sql = f'''SELECT name,p_num,personid
              FROM {table_name}
              WHERE local = \'{local}\' AND
                    domain = \'{domain}\' AND
                    pwd = \'{pwd}\'
'''
    try:
        conn = pg.connect(connect_string)
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(sql)
        
        result = cur.fetchall()
        print(result)
        conn.commit()
        conn.close()

        return result
    except pg.OperationalError as e:
        print(e)






def c_login(table_name,local,domain,pwd):
    sql = f'''SELECT COUNT(*)
              FROM {table_name}
              WHERE local = \'{local}\' AND
                    domain = \'{domain}\' AND
                    pwd = \'{pwd}\'
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


def insert(table_name, local, domain, pwd, name, p_num, lat, lng):
    sql = f'''INSERT INTO {table_name} 
              VALUES (\'{local}\', \'{domain}\',\'{pwd}\',\'{name}\',\'{p_num}\',\'{lat}\',\'{lng}\');
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



def select_h(table_name, name):
    sql = f'''SELECT name, address, doctorcnt
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

def select_s(table_name,subject):
    sql = f'''SELECT hosp_name, subject
              FROM {table_name}
              WHERE subject = \'{subject}\';  
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



def select(table_name, name):
    sql = f'''SELECT name, address, prescription
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

def select_in_r(table_name, personid):
    sql = f'''SELECT inst_name
              FROM {table_name}
              WHERE personid = \'{personid}\'
              ORDER BY r_day DESC LIMIT 1;
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

def select_name(table_name, inst_name):
    sql = f'''SELECT inst_name, name, p_num , r_day, r_hour, r_minute, prescription ,rid
              FROM {table_name}
              WHERE inst_name =  '{inst_name}'
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




def select_name_patient(table_name, name):
    sql = f'''SELECT inst_name, name, p_num ,rid
              FROM {table_name}
              WHERE name =  ' {name} '
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


def select_time(table_name,name):
    sql = f'''SELECT *
              FROM {table_name}
              WHERE name =  ' {name} '
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

def get_day(year,month,day):
    dayString = ["mon","tue","wed","thu","fri","sat","sun"]
    return dayString[datetime.date(year,month,day).weekday()]

# -----------------open hour

def open_hour_m(table_name,reser_time, name):
    sql = f'''SELECT COUNT(*)
              FROM {table_name}
              WHERE name = '{name}' AND mon_s <= {reser_time} AND mon_e > {reser_time}
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

def open_hour_t(table_name,reser_time, name):
    sql = f'''SELECT COUNT(*)
              FROM {table_name}
              WHERE name = '{name}' AND tue_s <= {reser_time} AND tue_e > {reser_time}
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

def open_hour_w(table_name,reser_time, name):
    sql = f'''SELECT COUNT(*)
              FROM {table_name}
              WHERE name = '{name}' AND wed_s <= {reser_time} AND wed_e > {reser_time}
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


def open_hour_th(table_name,reser_time, name):
    sql = f'''SELECT COUNT(*)
              FROM {table_name}
              WHERE name = '{name}' AND thu_s <= {reser_time} AND thu_e > {reser_time}
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

def open_hour_f(table_name,reser_time, name):
    sql = f'''SELECT COUNT(*)
              FROM {table_name}
              WHERE name = '{name}' AND fri_s <= {reser_time} AND fri_e > {reser_time}
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

def open_hour_s(table_name,reser_time, name):
    sql = f'''SELECT COUNT(*)
              FROM {table_name}
              WHERE name = '{name}' AND sat_s <= {reser_time} AND sat_e > {reser_time}
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

def open_hour_su(table_name,reser_time, name):
    sql = f'''SELECT COUNT(*)
              FROM {table_name}
              WHERE name = '{name}' AND sun_s <= {reser_time} AND sun_e > {reser_time}
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



def delete_reservation(table_name, rid):
    sql = f'''DELETE 
            FROM {table_name} 
              WHERE rid = {rid};
    '''
    try:
        conn = pg.connect(connect_string)
        cur = conn.cursor()
        cur.execute(sql)

        conn.commit()
        conn.close()
    except Exception as e:
        print(e)


#-----문 연 애들


def read_hosp_su(table_name,hour):
    sql = f'''SELECT * FROM {table_name}
                WHERE sun_s <= {hour} AND sun_e > {hour};
           '''
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


def read_hosp_m(table_name,hour):
    sql = f'''SELECT * FROM {table_name}
                WHERE mon_s <= {hour} AND mon_e > {hour};
           '''
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


def read_hosp_t(table_name,hour):
    sql = f'''SELECT * FROM {table_name}
                WHERE tue_s <= {hour} AND tue_e > {hour};
           '''
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

def read_hosp_w(table_name,hour):
    sql = f'''SELECT * FROM {table_name}
                WHERE wed_s <= {hour} AND wed_e > {hour};
           '''
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

def read_hosp_th(table_name,hour):
    sql = f'''SELECT * FROM {table_name}
                WHERE thu_s <= {hour} AND thu_e > {hour};
           '''
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

def read_hosp_f(table_name,hour):
    sql = f'''SELECT * FROM {table_name}
                WHERE fri_s <= {hour} AND fri_e > {hour};
           '''
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


def read_hosp_s(table_name,hour):
    sql = f'''SELECT * FROM {table_name}
                WHERE sat_s <= {hour} AND sat_e > {hour};
           '''
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


#---------문 닫은애들

def read_c_hosp_su(table_name,hour):
    sql = f'''SELECT * FROM {table_name}
                WHERE sun_s > {hour} OR sun_e <= {hour};
           '''
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


def read_c_hosp_m(table_name,hour):
    sql = f'''SELECT * FROM {table_name}
                WHERE mon_s > {hour} OR mon_e <= {hour};
           '''
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


def read_c_hosp_t(table_name,hour):
    sql = f'''SELECT * FROM {table_name}
                WHERE tue_s > {hour} OR tue_e <= {hour};
           '''
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

def read_c_hosp_w(table_name,hour):
    sql = f'''SELECT * FROM {table_name}
                WHERE wed_s > {hour} OR wed_e <= {hour};
           '''
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

def read_c_hosp_th(table_name,hour):
    sql = f'''SELECT * FROM {table_name}
                WHERE thu_s > {hour} OR thu_e <= {hour};
           '''
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

def read_c_hosp_f(table_name,hour):
    sql = f'''SELECT * FROM {table_name}
                WHERE fri_s > {hour} OR fri_e <= {hour};
           '''
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


def read_c_hosp_s(table_name,hour):
    sql = f'''SELECT * FROM {table_name}
                WHERE sat_s > {hour} OR sat_e <= {hour};
           '''
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


def update_t(table_name,hosp_name,mon_s,mon_e,tue_s,tue_e,wed_s,wed_e,thu_s,thu_e,fri_s,fri_e,sat_s,sat_e,sun_s,sun_e):
    sql = f'''UPDATE {table_name} SET mon_s = {mon_s}, mon_e = {mon_e}, tue_s = {tue_s}, tue_e = {tue_e}, wed_s = {wed_s}, wed_e = {wed_e},
                                      thu_s = {thu_s}, thu_e = {thu_e}, fri_s = {fri_s}, fri_e = {fri_e}, sat_s = {sat_s}, sat_e = {sat_e},
                                      sun_s = {sun_s}, sun_e = {sun_e}
                WHERE name = '{hosp_name}';
    
    '''
    try:
        print(sql)
        conn = pg.connect(connect_string) # DB연결(로그인)
        # cur = conn.cursor() # DB 작업할 지시자 정하기
        cur = conn.cursor()
        cur.execute(sql) # sql 문을 실행         
        # DB에 저장하고 마무리
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)


def create_prescription(table_name):
    sql = f'''CREATE TABLE if not exists {table_name} (
                date varchar(15),
                hosp_name varchar(150),
                name varchar(30),
                md1 varchar(30),
                n1 varchar(30),
                f1 varchar(20),
                d1 varchar(20),
                md2 varchar(30),
                n2 varchar(30),
                f2 varchar(20),
                d2 varchar(20),
                md3 varchar(30),
                n3 varchar(30),
                f3 varchar(20),
                d3 varchar(20),
                phar_name varchar(100),
                medi_date varchar(15),
                etc varchar(5000),
                pid varchar(5)
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


def prescription(table_name,date,hosp_name,name,md1,n1,f1,d1,md2,n2,f2,d2,md3,n3,f3,d3,phar_name,medi_date,etc,pid):
    sql = f'''INSERT INTO {table_name} 
              VALUES (\'{date}\', \'{hosp_name}\',\'{name}\',\'{md1}\',\'{n1}\',\'{f1}\',\'{d1}\',\'{md2}\',\'{n2}\',\'{f2}\',\'{d2}\',
                        \'{md3}\',\'{n3}\',\'{f3}\',\'{d3}\',\'{phar_name}\',\'{medi_date}\',\'{etc}\',\'{pid}\');
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


def change_f_2_t(table_name,rid):
    sql = f'''UPDATE {table_name} 
                SET prescription = 't' WHERE rid = {rid}
    '''
    try:
        conn = pg.connect(connect_string)
        cur = conn.cursor()
        cur.execute(sql)


        conn.commit()
        conn.close()
    except pg.OperationalError as e:
        print(e)


def phar_reser_f_2_t(table_name,info,phar_name):
    sql = f'''UPDATE {table_name} 
                SET prescription = '{info}' WHERE name = '{phar_name}'
    '''
    try:
        conn = pg.connect(connect_string)
        cur = conn.cursor()
        cur.execute(sql)


        conn.commit()
        conn.close()
    except pg.OperationalError as e:
        print(e)


def read_stars(table_name,personid):
    sql = f'''SELECT * FROM {table_name}
                WHERE personid = {personid};
           '''
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


def read_students(table_name):
    sql = f'''SELECT * FROM {table_name};
           '''
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



