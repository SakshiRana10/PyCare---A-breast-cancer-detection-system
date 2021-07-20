
import numpy as np
import pickle
from flask import Flask, request, render_template,redirect
import numpy.random._pickle
from flask_mysqldb import MySQL
import mysql.connector


app = Flask(__name__)
model = pickle.load(open('pycaremodel.pkl','rb'))

conn = mysql.connector.connect(host="localhost",user="root",password="",database="pycare")
cursor = conn.cursor()
#app.config['MYSQL_HOST'] = 'localhost'
#app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = ''
#app.config['MYSQL_DB'] = 'PyCare'
 
mysql = MySQL(app)

@app.route('/')
def pycare():
    return render_template('MainPage.html')

@app.route('/home')
def home():
    return render_template('pycareindex.html')


@app.route('/predict', methods=['GET','POST'])
def predict():

    if request.method == "GET":
        return render_template('form.html')
    features = [float(i) for i in request.form.values()]
    array_features = [np.array(features)]
    print(array_features)
    print(request.form.values)
    prediction = model.predict(array_features)
    output = prediction

    if output == 1:
        return render_template('form.html', result = 'The patient is not likely to have breast cancer!')
    else:
        return render_template('form.html', result= 'The patient is likely to have breast cancer!')


@app.route('/register', methods = ['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
     
    if request.method == 'POST':
        name=request.form.get('vname')
        password=request.form.get('vpassword')
        confirmpass=request.form.get('vcp')
        email=request.form.get('vemail')
        Address=request.form.get('vAddress')

        cursor.execute("""INSERT INTO `users` VALUES ('{}','{}','{}','{}','{}')""".format(name,password,confirmpass,email,Address))
        conn.commit()
        return render_template('login.html')

@app.route('/login_validation',methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    if request.method == 'POST':
        email=request.form.get('email')
        password=request.form.get('password')

        cursor.execute("""SELECT * from `users` where `email` LIKE'{}' AND `password` like '{}'""".format(email,password))
        users=cursor.fetchall()
        if len(users)>0:
            return redirect('/home')
        else:
            return redirect('/')   

@app.route('/blog')
def blog():
    return render_template('blogpost.html')  

@app.route('/blog1')
def blog1():
    return render_template('blog1.html')  

@app.route('/blog2')
def blog2():
    return render_template('blog2.html')  


@app.route('/blog3')
def blog3():
    return render_template('blog3.html')                

@app.route('/about')
def about():
    return render_template('about.html')     

@app.route('/contact')
def contact():
    return render_template('contact.html')      


if __name__ == '__main__':
   app.run(debug=True)
