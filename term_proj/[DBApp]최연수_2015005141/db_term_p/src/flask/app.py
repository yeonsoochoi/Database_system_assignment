from flask import Flask, render_template, request, jsonify
from pypg.helper import *
from apicall import hosp_list, pharm_list
import json, datetime
from pprint import pprint

app = Flask(__name__)



# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



@app.route('/')
def index():

    create_table('hospital')
    create_table('pharmacy')
    create_table('patients')
    hosptable_from_api('hosp_api')
    phartable_from_api('phar_api')
    create_reservation('hosp_reser')
    create_prescription('prescription')
    create_subject('subjects')
    create_star('star')
    create_reservation('store_reser')
    #result = read_students('phar_api')
    #pprint(result)
    #delete_table('star')
    #delete_table('prescription')
    #delete_table('hospital')
    #delete_table('pharmacy')
    #delete_table('subjects')
    #delete_table('patients')
    #delete_table('hosp_api')
    #delete_table('phar_api')
    #delete_table('hosp_reser')
    #delete_table('store_reser')
    return render_template("index.html")


@app.route('/hosp')
def hosp():
    lat = request.args.get('lat', 37.5585146)
    lng = request.args.get('lng', 127.0331892)
    json_data = pharm_list(lat, lng)
    #print(type(lat))
    json_data2 = hosp_list(lat, lng)
    #pprint(json_data)
    #tmp=json_data['response']['body']['items']['item'][1]['yadmNm']
    number = 0
    for row in json_data['response']['body']['items']['item']:
        #insert_to_t('hosp_api', row['yadmNm'], row['sdrCnt'], row['addr'], row['YPos'], row['XPos'])
        insert_to_p_t('phar_api',row['yadmNm'], row['addr'] ,row['YPos'], row['XPos'])

    for row in json_data2['response']['body']['items']['item']:
        insert_to_t('hosp_api', row['yadmNm'], row['sdrCnt'], row['addr'], row['YPos'], row['XPos'])
       

    return render_template("success.html")
   # return render_template("map.html")


@app.route("/register_search", methods=["GET", "POST"])
def register_search():
    if request.method == 'POST':
        info = request.form.get('chk_info')
        local = request.form.get('local')
        domain = request.form.get('domain')
        pwd = request.form.get('pwd')
        tmp1=[]
        tmp2=[]
        tmp3=[]

        if info == 'hosp':
            tmp1 = login('hospital', local, domain, pwd)
            print(tmp1)
            if not tmp1 == []:
                result = read_students('hosp_api')
                return render_template("choose_hosp.html",hospitals=result,name=tmp1[0]['name'],p_num=tmp1[0]['p_num'])
        elif info == 'patient':
            tmp2 = login_p('patients', local, domain, pwd)
            if not tmp2 == []:
                print(type(tmp2[0]['personid']))
                return render_template("map.html",info=info,name=tmp2[0]['name'],p_num=tmp2[0]['p_num'],personid=tmp2[0]['personid'])
        elif info == 'sto':
            tmp3 = login('pharmacy', local, domain, pwd)
            if not tmp3 == []:
                result = read_students('phar_api')
                return render_template("choose_phar.html",phars=result,name=tmp3[0]['name'],p_num=tmp3[0]['p_num'])
        else:
            return render_template("error.html")

        if tmp1 == [] and tmp2 == [] and tmp3 ==[]:
            return render_template("login_alert.html")

   # return render_template("select.html", students=result, number=tmp)
    return render_template("error.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        info1 = request.form.get('chk_info1')
        info2 = request.form.get('chk_info2')
        info3 = request.form.get('chk_info3')

        local = request.form.get('local')
        domain = request.form.get('domain')
        pwd = request.form.get('pwd')
        name = request.form.get('name')
        p_num = request.form.get('p_num')
        lat = request.form.get('lat')
        lng = request.form.get('lng')

        if  (not re.match('^010', p_num)) or ( len(p_num) != 11):
            return render_template("error.html")


        if info1 == 'hosp':
            insert('hospital',local,domain,pwd ,name,p_num,lat,lng)
        if info2 == 'patient':
            insert('patients',local,domain,pwd,name,p_num,lat,lng)
        if info3 == 'sto':
            insert('pharmacy',local,domain,pwd,name,p_num,lat,lng)

    return render_template("success.html")



@app.route("/reservated_h", methods=["POST"])
def reservated_h():
    if request.method == 'POST':
        hosp_name = request.form.get('hosp_name')
        name = request.form.get('name')
        info = request.form.get('info')
        p_num = request.form.get('p_num')
        date = request.form.get('date')
        time = request.form.get('time')
        personid = request.form.get('personid')
        arr = date.split('/')
        arr2 = time.split(':')
        year = arr[2]
        month = arr[0]
        day = arr[1]
        hour = arr2[0]
        minute = arr2[1]
        r_day = year + month + day
        tmp = get_day(int(year),int(month),int(day))
        
        if tmp == 'mon':
            tmp2 = open_hour_m('hosp_api', hour ,hosp_name)
            print(tmp2[0]['count'])
            if tmp2[0]['count'] != 0:
                reservation('hosp_reser', hosp_name ,name, p_num , int(r_day), int(hour), int(minute),personid)
                return render_template("reser_success.html",info=info, name=name,p_num=p_num,personid=personid)
            else:
                return render_template("time_error.html",info=info, name=name,p_num=p_num,personid=personid)
        elif tmp == 'tue':
            tmp2 = open_hour_t('hosp_api', hour ,hosp_name)
            print(tmp2[0]['count'])
            if tmp2[0]['count'] != 0:
                reservation('hosp_reser', hosp_name ,name, p_num,int(r_day), int(hour), int(minute),personid)
                return render_template("reser_success.html",info=info, name=name,p_num=p_num,personid=personid)
            else:
                return render_template("time_error.html",info=info, name=name,p_num=p_num,personid=personid)
        elif tmp == 'wed':
            tmp2 = open_hour_w('hosp_api', hour ,hosp_name)
            print(tmp2[0]['count'])
            if tmp2[0]['count'] != 0:
                reservation('hosp_reser', hosp_name ,name, p_num,int(r_day), int(hour), int(minute),personid)
                return render_template("reser_success.html",info=info, name=name,p_num=p_num,personid=personid)
            else:
                return render_template("time_error.html",info=info, name=name,p_num=p_num,personid=personid)
        elif tmp == 'thu':
            tmp2 = open_hour_th('hosp_api', hour ,hosp_name)
            print(tmp2[0]['count'])
            if tmp2[0]['count'] != 0:
                reservation('hosp_reser', hosp_name ,name, p_num,int(r_day), int(hour), int(minute),personid)
                return render_template("reser_success.html",info=info, name=name,p_num=p_num,personid=personid)
            else:
                return render_template("time_error.html",info=info, name=name,p_num=p_num,personid=personid)
        elif tmp == 'fri':
            tmp2 = open_hour_f('hosp_api', hour ,hosp_name)
            print(tmp2[0]['count'])
            if tmp2[0]['count'] != 0:
                reservation('hosp_reser', hosp_name ,name, p_num,int(r_day), int(hour), int(minute),personid)
                return render_template("reser_success.html",info=info, name=name,p_num=p_num,personid=personid)
            else:
                return render_template("time_error.html",info=info, name=name,p_num=p_num,personid=personid)
        elif tmp == 'sat':
            tmp2 = open_hour_s('hosp_api', hour ,hosp_name)
            print(tmp2[0]['count'])
            if tmp2[0]['count'] != 0:
                reservation('hosp_reser', hosp_name ,name, p_num,int(r_day), int(hour), int(minute),personid)
                return render_template("reser_success.html",info=info, name=name,p_num=p_num,personid=personid)
            else:
                return render_template("time_error.html",info=info, name=name,p_num=p_num,personid=personid)
        elif tmp == 'sun':
            tmp2 = open_hour_su('hosp_api', hour ,hosp_name)
            print(tmp2[0]['count'])
            if tmp2[0]['count'] != 0:
                reservation('hosp_reser', hosp_name ,name, p_num,int(r_day), int(hour), int(minute),personid)
                return render_template("reser_success.html",info=info, name=name,p_num=p_num,personid=personid)
            else:
                return render_template("time_error.html",info=info, name=name,p_num=p_num,personid=personid)
        else:
            return render_template("error.html")
        


@app.route("/to_map",methods=["GET","POST"])
def to_map():
    if request.method == 'POST':
        name = request.form.get('name')
        info = request.form.get('info')
        p_num = request.form.get('p_num')
        personid = request.form.get('personid')
    return render_template("map.html",name=name,info=info,p_num=p_num,personid=personid)


@app.route("/to_reservated_h",methods=["POST"])
def to_reservated_h():
    if request.method == 'POST':
        hosp_name = request.form.get('hosp_name')
        name = request.form.get('name')
        info = request.form.get('info')
        p_num = request.form.get('p_num')
        personid = request.form.get('personid')
    return render_template("select_time.html",hosp_name=hosp_name,name=name,p_num=p_num,info=info,personid=personid)


@app.route("/reservated_p", methods=["POST"])
def reservated_p():
    if request.method == 'POST':
        phar_name = request.form.get('phar_name')
        name = request.form.get('name')
        info = request.form.get('info')
        p_num = request.form.get('p_num')
        personid = request.form.get('personid')
        year = request.form.get('year')
        month = request.form.get('month')
        date = request.form.get('date')
        r_hour = request.form.get('hour')
        r_minute = request.form.get('minute')
        r_day = year + month + date

        reservation('store_reser', phar_name, name, p_num, r_day, r_hour,r_minute,personid)
        
    return render_template("map.html",info=info,name=name,p_num=p_num,personid=personid)



@app.route("/recently_r",methods=["POST"])
def recently_r():
     if request.method == 'POST':
         data = request.get_json()
         result = select_in_r('hosp_reser', str(data['personid']))
    
     return json.dumps(result)

@app.route("/time_update",methods=["POST"])
def time_update():
    hosp_name = request.form.get('hosp_name')
    name = request.form.get('name')
    mon_s = request.form.get('mon_s')
    mon_e = request.form.get('mon_e')
    tue_s = request.form.get('tue_s')
    tue_e = request.form.get('tue_e')
    wed_s = request.form.get('wed_s')
    wed_e = request.form.get('wed_e')
    thu_s = request.form.get('thu_s')
    thu_e = request.form.get('thu_e')
    fri_s = request.form.get('fri_s')
    fri_e = request.form.get('fri_e')
    sat_s = request.form.get('sat_s')
    sat_e = request.form.get('sat_e')
    sun_s = request.form.get('sun_s')
    sun_e = request.form.get('sun_e')

    update_t('hosp_api',hosp_name,int(mon_s),int(mon_e),int(tue_s),int(tue_e),int(wed_s),int(wed_e),
            int(thu_s),int(thu_e),int(fri_s),int(fri_e),int(sat_s),int(sat_e),int(sun_s),int(sun_e))

    return render_template("hospital.html",hosp_name=hosp_name,name=name)



# ------------ login


@app.route("/map_json", methods=["POST"])
def map_json():
    if request.method == 'POST':
        time = request.get_json()
        if time['day'] == 0: #일요일
            result = read_hosp_su('hosp_api',time['hour'])
        elif time['day'] == 1:
            result = read_hosp_m('hosp_api',time['hour'])
        elif time['day'] == 2:
            result = read_hosp_t('hosp_api',time['hour'])
        elif time['day'] == 3:
            result = read_hosp_w('hosp_api',time['hour'])
        elif time['day'] == 4:
            result = read_hosp_th('hosp_api',time['hour'])
        elif time['day'] == 5:
            result = read_hosp_f('hosp_api',time['hour'])
        elif time['day'] == 6:
            result = read_hosp_s('hosp_api',time['hour'])

    return json.dumps(result) 


@app.route("/map_json_c", methods=["POST"])
def map_json_c():
    if request.method == 'POST':
        time = request.get_json()
        if time['day'] == 0: #일요일
            result = read_c_hosp_su('hosp_api',time['hour'])
        elif time['day'] == 1:
            result = read_c_hosp_m('hosp_api',time['hour'])
        elif time['day'] == 2:
            result = read_c_hosp_t('hosp_api',time['hour'])
        elif time['day'] == 3:
            result = read_c_hosp_w('hosp_api',time['hour'])
        elif time['day'] == 4:
            result = read_c_hosp_th('hosp_api',time['hour'])
        elif time['day'] == 5:
            result = read_c_hosp_f('hosp_api',time['hour'])
        elif time['day'] == 6:
            result = read_c_hosp_s('hosp_api',time['hour'])

    return json.dumps(result) 




#----------- search

@app.route("/hosp_search", methods=["POST"])
def hosp_search():
    if request.method == 'POST':
        name = request.get_json()
        result = select_h('hosp_api', name['hosp_name'])
        print(result)        
    return json.dumps(result)

@app.route("/store_search", methods=["POST"])
def store_search():
    if request.method == 'POST':
        name = request.get_json()
        print(name)
        result = select('phar_api', name['phar_name'])
        
    return json.dumps(result)

@app.route("/subject_search",methods=["POST"])
def subject_search():
    if request.method == 'POST':
        data = request.get_json()
        result = search_subject('subjects', data['hosp_name'])
        print(result)
    return json.dumps(result)


@app.route("/read_subject",methods=["POST"])
def read_subject():
    if request.method == 'POST':
        data = request.get_json()
        result = search_subject_sub('subjects',data['subject'])
        print(result)
    return json.dumps(result)



@app.route("/change_subject",methods=["GET","POST"])
def change_subject():
    hosp_name = request.form.get('hospital_name')
    subject = request.form.get('subject')
    add_subject('subjects',hosp_name,subject)
    print(hosp_name)

    return render_template("hospital.html",hosp_name=hosp_name)




#-----reservation


@app.route("/reservation_status",methods=["POST"])
def reservation_status():
     if request.method == 'POST':
         data = request.get_json()
         result = select_name('hosp_reser',data['hosp_name'])
         print(result)
     return json.dumps(result)

@app.route("/reservation_status_phar",methods=["POST"])
def reservation_status_phar():
     if request.method == 'POST':
         data = request.get_json()
         result = select_name('store_reser',data['phar_name'])
         print(result)
     return json.dumps(result)



@app.route("/reservation_status_patient",methods=["POST"])
def reservation_status_patient():
     if request.method == 'POST':
         data = request.get_json()
         print("test")
         print(data['name'])
         result = select_name_patient('hosp_reser',data['name'])
         print(result)
         print("test")
     return json.dumps(result)


@app.route("/store_prescription",methods=["GET","POST"])
def store_prescription():
    if request.method == 'POST':
        date = request.form.get('p_time')
        hosp_name = request.form.get('hosp_name')
        name = request.form.get('name')
        md1 = request.form.get('md1')
        n1 = request.form.get('n1')
        f1 = request.form.get('f1')
        d1 = request.form.get('d1')
        md2 = request.form.get('md2')
        n2 = request.form.get('n2')
        f2 = request.form.get('f2')
        d2 = request.form.get('d2')
        md3 = request.form.get('md3')
        n3 = request.form.get('n3')
        f3 = request.form.get('f3')
        d3 = request.form.get('d3')
        phar_name = request.form.get('phar_name')
        phar_t_name = request.form.get('phar_t_name')
        etc = request.form.get('etc')
        pid = request.form.get('rid')
        print(etc)

        prescription('prescription',date,hosp_name,name,md1,n1,f1,d1,md2,n2,f2,d2,md3,n3,f3,d3,phar_name,phar_t_name,etc,pid)
        change_f_2_t('hosp_reser',pid)

    return render_template("hospital.html",hosp_name=hosp_name,name=name)

@app.route("/star",methods=["POST"])
def star():
    if request.method == 'POST':
        data = request.get_json()
        personid = data['personid']
        result = read_stars('star',int(personid))
        return json.dumps(result)


@app.route("/new_star",methods=["POST"])
def new_star():
    if request.method == 'POST':
        hosp_name = request.form.get('hosp_name')
        name = request.form.get('name')
        info = request.form.get('info')
        p_num = request.form.get('p_num')
        personid = request.form.get('personid')
        result = read_stars('star',personid)
        if result == []:
            insert_star('star',hosp_name,personid)
        else:
            update_star('star',hosp_name,personid)

    return render_template("map.html",name=name,p_num=p_num,info=info,personid=personid)





@app.route("/delete_reser",methods=["GET","POST"])
def delete_reser():
    if request.method == 'POST':
        rid = request.form.get('rid')
        name = request.form.get('name')
        hosp_name = request.form.get('hosp_name')
        delete_reservation('hosp_reser',rid)
    return render_template("hospital.html",hosp_name=hosp_name,name=name) # name, hosp_name return 필요? ***********************************


@app.route("/to_prescription",methods=["GET","POST"])
def to_prescription():
    rid = request.form.get('rid')
    name = request.form.get('name')
    hosp_name = request.form.get('hosp_name')
    r_day = request.form.get('r_day')
    r_hour = request.form.get('r_hour')
    r_minute = request.form.get('r_minute')
    print(r_day)
    r_date = str(r_day) + " " + str(r_hour) + ":" + str(r_minute)
    print(r_date)

    return render_template("prescription.html",name=name,hosp_name=hosp_name,r_date=r_date,rid=rid)





#------ etc

@app.route("/map_json_store",methods=["POST"])
def mapp_json_store():
    if request.method == 'POST':
        result = read_students('phar_api')
        return json.dumps(result)


@app.route("/to_insert")
def to_insert():
    return render_template("insert.html")



@app.route("/to_hospital",methods=["GET","POST"])
def to_hospital():
    name = request.form.get('name')
    hosp_name = request.form.get('hosp_name')
    print(hosp_name)
    p_num = request.form.get('p_num')
    info = request.form.get('chk_info')
    if info == 'no':
        return render_template("hospital.html", name=name, hosp_name=hosp_name, p_num=p_num)
    else:
        return render_template("update_timetable.html",hosp_name=hosp_name,name=name)



@app.route("/to_phar",methods=["GET","POST"])
def to_phar():
    name = request.form.get('name')
    phar_name = request.form.get('phar_name')
    p_num = request.form.get('p_num')
    info = request.form.get('chk_info')
    
    return render_template("phar.html", name=name, phar_name=phar_name, p_num=p_num)


@app.route("/change_pres",methods=["GET","POST"])
def change_pres():
    info = request.form.get('chk_info')
    name = request.form.get('name')
    phar_name = request.form.get('phar_name')
    
    phar_reser_f_2_t('phar_api',info, phar_name)

    
    return render_template("phar.html", name=name, phar_name=phar_name)











@app.route("/table_list")
def table_list():

    result = read_students('hosp_api')
    pprint(result)

    return render_template("select.html", hospitals=result,number=0)


@app.route("/reset")
def reset():
    delete_table('students')
    create_table('students')
    call_table('students')
    return render_template("success.html")












@app.route("/insert_new", methods=["GET", "POST"])
def insert_new():
    if request.method == 'POST':
        name = request.form.get('name')
        number = request.form.get('number')
        if name =='' or number == '':
            return render_template("error.html")
        elif re.match('^010', number) and len(number) == 11:
          #  insert('students', name, number)
            return render_template("success.html")
        else:
            return render_template("error.html")


@app.route("/delete_new", methods=["GET", "POST"])
def delete_new():
    if request.method == 'POST':
        name = request.form.get('name')
        tmp = count('students', name)
        if(tmp == 0) or name == '':
            return render_template("error.html")

        delete('students', name)
        return render_template("success.html")




@app.route("/register-json", methods=["POST"])
def register_json():
     pprint(request.__dict__)
     return "OK"


@app.route("/students")
def students():    
    students = json.dumps(read_students('students'))
    return students







if __name__ == ("__main__"):
  # docker
  app.run(debug=True, host='0.0.0.0', port=5090)
  # other
  # app.run(debug=True)





