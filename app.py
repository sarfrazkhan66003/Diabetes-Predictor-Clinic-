from flask import Flask, request, render_template, redirect, url_for, session
import pickle
import numpy as np
import pandas as pd
import os
import random
import string

application = Flask(__name__)
app = application

app.secret_key = "myverysecretkey"

# Load ML Model
scaler = pickle.load(open(r"C:\Users\DELL\Desktop\Sarfu\PW Data Science\Project\Diabetes-Deployment-With-BeanStalk-main\Model\standardScalar.pkl", "rb"))
model = pickle.load(open(r"C:\Users\DELL\Desktop\Sarfu\PW Data Science\Project\Diabetes-Deployment-With-BeanStalk-main\Model\modelForPrediction.pkl", "rb"))


# --------------------------
# Generate Random User ID & Password
# --------------------------

def generate_user_id():
    return "USR" + ''.join(random.choices(string.digits, k=12))

def generate_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))


# --------------------------
# ROUTE: Registration Page
# --------------------------

@app.route('/register')
def register():
    return render_template("register.html")


@app.route('/save_registration', methods=['POST'])
def save_registration():

    name = request.form['name']
    age = request.form['age']
    address = request.form['address']
    mobile = request.form['mobile']
    problem = request.form['problem']

    user_id = generate_user_id()
    password = generate_password()

    file_path = "patients_register.xlsx"

    new_row = {
        "PatientName": name,
        "Age": age,
        "Address": address,
        "Mobile": mobile,
        "Problem": problem,
        "UserID": user_id,
        "Password": password
    }

    # Save to Excel
    if not os.path.exists(file_path):
        df = pd.DataFrame([new_row])
        df.to_excel(file_path, index=False)
    else:
        df = pd.read_excel(file_path)
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_excel(file_path, index=False)

    return render_template("login.html",
                           message="Registration Successful! Use the given User ID & Password to Login.",
                           user_id=user_id,
                           password=password)


# --------------------------
# LOGIN PAGE
# --------------------------

@app.route('/')
def login():
    return render_template('login.html')


@app.route('/login_user', methods=['POST'])
def login_user():

    user_id = request.form['user_id']
    password = request.form['password']

    if not os.path.exists("patients_register.xlsx"):
        return render_template("login.html", error="No registered patients found.")

    df = pd.read_excel("patients_register.xlsx")

    user_data = df[(df['UserID'] == user_id) & (df['Password'] == password)]

    if not user_data.empty:
        session['user'] = user_id
        session['patient_name'] = user_data['PatientName'].values[0]
        return redirect(url_for("home"))

    else:
        return render_template("login.html", error="Invalid User ID or Password")


# --------------------------
# HOME (Prediction Page)
# --------------------------

@app.route('/home')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    return render_template("home.html", patient=session['patient_name'])


# --------------------------
# PREDICTION ROUTE
# --------------------------

@app.route('/predictdata', methods=['POST'])
def predict_datapoint():

    if 'user' not in session:
        return redirect(url_for('login'))

    # Patient inputs
    Pregnancies = float(request.form['Pregnancies'])
    Glucose = float(request.form['Glucose'])
    BloodPressure = float(request.form['BloodPressure'])
    SkinThickness = float(request.form['SkinThickness'])
    Insulin = float(request.form['Insulin'])
    BMI = float(request.form['BMI'])
    DiabetesPedigreeFunction = float(request.form['DiabetesPedigreeFunction'])
    Age = float(request.form['Age'])

    X = scaler.transform([[Pregnancies, Glucose, BloodPressure, SkinThickness,
                           Insulin, BMI, DiabetesPedigreeFunction, Age]])

    prediction = model.predict(X)

    if prediction[0] == 1:
        result = "Diabetic"
    else:
        result = "Non-Diabetic"

    # SAVE PREDICTION TO EXCEL
    file_path = "patients_data.xlsx"
    new_row = {
        "UserID": session['user'],
        "PatientName": session['patient_name'],
        "Glucose": Glucose,
        "BMI": BMI,
        "Age": Age,
        "Prediction": result
    }

    if not os.path.exists(file_path):
        df = pd.DataFrame([new_row])
        df.to_excel(file_path, index=False)
    else:
        df = pd.read_excel(file_path)
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_excel(file_path, index=False)

    return render_template("single_prediction.html",
                           result=result,
                           patient_name=session['patient_name'])


# --------------------------
# LOGOUT
# --------------------------

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# --------------------------
# Run App
# --------------------------

if __name__ == '__main__':
    app.run(debug=True)
