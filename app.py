from flask import Flask, request, render_template, g, redirect
import sqlite3
import modulea
import db


app = Flask('hhh')
print(app)

DATABASE = './sqlite3.db'


def connect_db():
    return sqlite3.connect(DATABASE)


@app.before_request
def init_db():
    has_db = hasattr(g, 'db')
    if has_db == False:
        g.db = connect_db()
        init_table()


def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row))for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv


def init_table():
    with g.db as con:
       cur = con.cursor()
       try:
           cur.execute('CREATE TABLE IF NOT EXISTS students(id integer primary key autoincrement,name VARCHAR(200),age int(10),num varchar(32))')
       except Exception as err:
           print('inert data error:', err)
       else:
           con.commit()


@app.route('/', methods=['GET', 'POST'])
def index():
    has_db = hasattr(g, 'db')
    print('has db: ', has_db)
    return render_template('a.html', x=has_db)


@app.route('/db', methods=['GET', 'POST'])
def db_form():
    sql_insert = 'SELECT * FROM students'
    result = query_db(sql_insert)
    return render_template('all.html',ids = result[0],
                                      na = result[1],
                                      ag = result[2],
                                      nu = result[3])


@app.route('/db_insert', methods=['POST'])
def db_insert():
    na = request.form['name']
    ag = int(request.form['age'])
    nu = request.form['num']
    with g.db as con:
        cur = con.cursor()
        try:
            sql = 'INSERT INTO students(name,age,num) VALUES(?,?,?)'
            cur.execute(sql, (na, ag, nu))
        except Exception as err:
            print('inert data error:', err)
        else:
            con.commit()
    return redirect('db_values')


@app.route('/db_update', methods=['POST'])
def db_update():
    try:
        ona = request.form['oldname']
    except Exception as err:
        print("inert data error :", err)
    nna = request.form['newname']
    nag = int(request.form['newage'])
    nnu = request.form['newnum']
    with g.db as con:
        cur = con.cursor()
        cur.execute("update students set name = (?),age = (?),num = (?) where name = (?)",(nna,nag,nnu,ona))
        con.commit()
    return redirect('db_values')
    

@app.route('/db_del', methods=['POST'])
def db_del():
    deid = int(request.form['id'])
    with g.db as con:
        cur = con.cursor()
        cur.execute("DELETE FROM students WHERE id=(?)", (deid,))
        con.commit()
    return redirect('db_values')


@app.route('/db_select', methods=['POST'])
def db_select():
    sid = int(request.form['id'])
    sql_insert = 'SELECT * FROM students WHERE id = (?)'
    result = query_db(sql_insert,(sid,))
    return render_template('db-result.html', result=result)


@app.route('/db_values', methods=['GET'])
def db_value():
    sql_insert = 'SELECT * FROM students'
    result = query_db(sql_insert)
    return render_template('db-result.html', result=result)


if __name__ == '__main__':
    print('in app.py: ',__name__)
    app.run(host='0.0.0.0', port=80)
