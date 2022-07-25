from flask import Flask, request, render_template, redirect
import sqlite3
import uuid

app = Flask(__name__)

@app.route('/disp_students', methods=['GET'])
def get_students():

    stu = sqlite3.connect('students.db')
    cur = stu.cursor()
    cur.execute('select * from students')

    return render_template('results.html', content = cur.fetchall())


@app.route('/greater', methods=['GET'])
def get_greater():
    stu = sqlite3.connect('students.db')
    cur = stu.cursor()
    cur.execute('select * from students st where st.st_grade >= 85')

    return render_template('results.html', content = cur.fetchall())


@app.route('/updatestu', methods=['POST'])
def update_stu():
    stu = sqlite3.connect('students.db')
    cur = stu.cursor()
    if(request.method == 'POST'):
        u_sid = request.form['st_id']
        u_name = request.form['name']
        u_grade = request.form['grade']
        print(u_sid, u_name, u_grade)
        cur.execute("update students set st_name = '{0}', st_grade = {1} where stu_id = '{2}'".format(u_name, u_grade, u_sid))
        stu.commit()
        stu.close()
        return redirect('/',code=302)


@app.route('/deletestu', methods=['POST'])
def delete_stu():
    stu = sqlite3.connect('students.db')
    cur = stu.cursor()
    if(request.method == 'POST'):
        st_id = request.form['del']
        print(st_id)
        cur.execute('delete from students where stu_id = ?', [st_id])
        stu.commit()
        stu.close()
        return redirect('/',  code=302)

@app.route('/', methods=['GET', 'POST'])
def start():
    if(request.method == 'POST'):
        stu = sqlite3.connect('students.db')
        cur = stu.cursor()
        cur.execute('create table if not exists students (stu_id varchar(255), st_name varchar(255), st_grade integer(2));')
        stu.commit()

        st_id = uuid.uuid4()

        name = request.form['name']
        grade = request.form['grade']

        cur.execute("insert into students(stu_id, st_name, st_grade) values (?,?,?)", [str(st_id), str(name), int(grade)])

        stu.commit()

        stu.close()


    return render_template('Home.html')
 
app.run(host='localhost', port=5005, debug=True)