from flask import Flask, render_template, request, jsonify
from pypg.helper import *
import json
from pprint import pprint

app = Flask(__name__)


@app.route('/')
def index():
    create_table('students')
    tmp = count('students','김')
    print(tmp)
    if(tmp==0):
        call_table('students')
    tables = read_tables()
    #delete_table('students')
    return render_template("index.html", table=tables[0][0])


@app.route("/table_list")
def table_list():
    result = read_students('students')

    return render_template("list.html", students=result)


@app.route("/reset")
def reset():
    delete_table('students')
    create_table('students')
    call_table('students')
    return render_template("success.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        number = request.form.get('number')

        insert('students', name, number)

    return render_template("insert.html", students=read_students('students'))


@app.route("/register_search", methods=["GET", "POST"])
def register_search():
    if request.method == 'POST':
        name = request.form.get('name')
        result = select('students', name)
        tmp = count('students',name)
        if result ==[]:
            return render_template("insert.html", students='students')
    return render_template("select.html", students=result, number=tmp)


@app.route("/update_new",methods=["GET" , "POST"])
def update_new():
    if request.method == 'POST':
        name = request.form.get('name')
        number = request.form.get('number')
        tmp = count2('students',name,number)

        if(tmp == 0):
            return render_template("error.html")

        if name == '' or number == '':
            return render_template("error.html")
        elif re.match('^010', number) and len(number) == 11:
            delete_for_upd('students', name, number)
            return render_template("update.html",tmp_name=name,tmp_number=number)
        else:
            return render_template("error.html")



@app.route("/insert_new", methods=["GET", "POST"])
def insert_new():
    if request.method == 'POST':
        name = request.form.get('name')
        number = request.form.get('number')
        if name =='' or number == '':
            return render_template("error.html")
        elif re.match('^010', number) and len(number) == 11:
            insert('students', name, number)
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
