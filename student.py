from flask import Flask, request, render_template, g, redirect
import sqlite3
import modulea
import db

student = Flask('student')
print(student)

DATABASE = './sqlite4.db'

def connect_db():
    return sqlite3.connect(DATABASE)

@student.before_request
def init_db():
    has_db = hasattr(g, 'db')
    if has_db == False:
        g.db = connect_db()
        # init_table()


def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row))for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv


def init_table():
    sql = 'CREATE TABLE students(id integer primary key autoincrement,name VARCHAR(200),age int(10),num varchar(32))'
    result = query_db(sql)
    print('init table result: ', result)


@student.route('/st', methods=['GET', 'POST'])
def db_form():
#    sql_value = 'SELECT * FROM students'
#    result = query_db(sql_value)
    return render_template('all.html')


@student.route('/st_insert', methods=['POST'])
def st_insert():
    na = request.form['name']
    ag = request.form['age']
    nu = request.form['num']
    sql_insert = 'INSERT INTO students(name,age,num) VALUES(na,ag,nu)'
    return redirect('st_values')

    
@student.route('/st_update', methods=['POST'])
def st_update():
    ona = request.form['oldname']
    nna = request.form['newname']
#    oag = request.form['oldage']
    nag = request.form['newage']
#    onu = request.form['oldnum']
    nnu = request.form['newnum']
    with sqlite3.connect('./sqlite4.db') as con:
        cur = con.cursor()
        cur.execute("update test set name = (?),age = (?),num = (?) where name = (?)",(nna,nag,nnu,ona))
        con.commit()
    return redirect('st_values')


@student.route('/st_del', methods = ['POST'])
def st_del():
    sid = request.form['id']
    with g.db as con:
        cur = con.cursor()
        cur.execute("DELETE FROM students WHERE id=(?)",(sid,))
        con.commit()
    return redirect('st_values')


@student.route('/st_select', methods=['POST'])
def st_select():
    sid = request.form['id']
    with g.db as con:
        cur = con.cursor()
        cur.execute('SELECT * FROM students WHRER id = (?)',(sid,))
        con.commit()
    return redirect('st_values')


@student.route('/st_values', methods=['GET'])
def st_value():
    sql_value = 'SELECT * FROM students'
    result = query_db(sql_value)
    return render_template('db-result.html', result=result)


#if __name__ == '__main__':
#    print('in app.py: ',__name__)
#    app.run(host='0.0.0.0', port=80)