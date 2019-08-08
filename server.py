import MySQLdb
from flask import Flask, render_template, request, url_for,redirect

app=Flask(__name__)

connector = MySQLdb.connect(host="localhost",user="root",password="tiger",db="mutex")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/profile/<name>")
def profile(name=None):
    cursor = connector.cursor()
    query = "select * from user where username=%s"
    cursor.execute(query,(name,))
    result = cursor.fetchall()
    return "<h1>"+str(result)+"</h1>"

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == "GET":
        return render_template('index.html')
    else:
        cursor = connector.cursor()
        query = "select * from user where username=%s"
        cursor.execute(query, (request.form['username'],))
        result = cursor.fetchall()
        if not result:
            query = "insert into user values(%s,%s,%s)"
            cursor.execute(query,(request.form['username'],request.form['passwd'],request.form['email'],))
            connector.commit()
            return redirect(url_for('profile', name=request.form['username']))

        else:
            return "<h1> User already exists...!</h1>"
        return "<h1>" + str(result) + "</h1>"

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        cursor = connector.cursor()
        query = "select * from user where username=%s"
        cursor.execute(query, (request.form['username'],))
        result = cursor.fetchall()
        if not result:
            return "<h1> User does not exists...!</h1>"
        else:
            if result[0][1]==request.form['passwd']:
                return redirect(url_for('profile',name=request.form['username']))
            else:
                return "<h1>Password is incorrect...!</h1>"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=2019, debug=True)


