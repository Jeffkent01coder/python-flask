from flask import Flask, render_template, request, session
import pymysql

app = Flask(__name__)
app.secret_key = '123kk'


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        id_no = request.form['id_no']
        password = request.form['password']
        gender = request.form['gender']
        country = request.form['country']

        conn = pymysql.connect("localhost", "root", "", "users")
        cursor = conn.cursor()
        sql = "INSERT INTO user (username, email, phone, id_no, password, gender, country) VALUES(%s, %s, %s, %s, %s, " \
              "%s, %s) "
        result = cursor.execute(sql, (username, email, phone, id_no, password, gender, country))
        conn.commit()
        if result:
            return render_template("view.html")
        else:
            return render_template("register.html")
    else:
        return render_template("register.html")


@app.route("/view")
def view():
    conn = pymysql.connect("localhost", "root", "", "users")
    cursor = conn.cursor()
    query = "SELECT * FROM user"
    cursor.execute(query)
    if cursor.rowcount < 1:
        return render_template("view.html", msg="No information found")
    else:
        rows = cursor.fetchall()
        return render_template("view.html", rows=rows)


@app.route('/login', methods=['POST', 'GET'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        conn = pymysql.connect("localhost", "root", "", "users")
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM user WHERE username= %s AND password = %s ', (username, password,))
        result = cursor.fetchone()
        if result:
            session['logged'] = True

            session['username'] = result[0]
            msg = 'logged in successfully'
            return render_template("view_profile.html", result=result)
        else:
            msg = 'input correct user details'
            return render_template("login.html")
    else:

        return render_template("login.html")


@app.route('/view_profile', methods=['POST', 'GET'])
def view_profile():
    if 'logged' in session:
        conn = pymysql.connect("localhost", "root", "", "users")
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user WHERE username= %s', (session['username']))
        result = cursor.fetchone()
        return render_template('view_profile.html', result=result)
    else:
        return render_template("login.html")


if __name__ == "__main__":
    app.debug = True
    app.run()