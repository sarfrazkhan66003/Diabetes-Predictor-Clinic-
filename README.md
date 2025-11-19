# Diabetes Predictor Clinic 🩺🍃

- A simple, secure, and user-friendly Flask web application that allows patients to register, log in, submit health features, and get a diabetes prediction (Diabetic / Non-Diabetic) from a pre-trained ML model.
  All patient registrations and prediction records are saved to Excel files for easy tracking and offline review.

## Overview ✅

- This project is an end-to-end Flask application that integrates a trained machine learning model for diabetes prediction with a patient registration and authentication flow. It lets clinics or demo setups:
  - Register a patient (name, age, address, mobile, symptoms) and auto-generate UserID + Password. 🧾
  - Let patients log in using the generated credentials. 🔐
  - Allow logged-in patients (or clinic staff) to input features (Glucose, BMI, etc.) and run a pre-trained ML model to predict diabetes. 🤖
  - Save both registration and prediction records to Excel files (patients_register.xlsx and patients_data.xlsx). 💾

## Features ✨

- Patient registration with auto-generated UserID & password. 🆔
- Secure login session using Flask sessions. 🔒
- Input form to collect diabetes features (Pregnancies, Glucose, BP, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age). 📋
- Model inference using a pre-trained scikit-learn model (pickled). 🧠
- Results page showing patient name, prediction (Diabetic / Non-Diabetic) and branding (Developer: Sarfraz Khan). 🏷️
- Saves registration & prediction histories to Excel for easy auditing. 📊
- Easy to deploy locally or on cloud platforms supporting Python/Flask. ☁️

## Tech Stack & Requirements 🧰

- Python 3.10 (recommended) 🐍
- Flask
- pandas
- scikit-learn
- numpy
- openpyxl (for writing .xlsx)
- (Optional) virtualenv / conda for environment management

## requirements.txt

- Flask==2.3.2
- pandas==2.2.2
- numpy==1.26.4
- scikit-learn==1.3.0
- openpyxl==3.1.2

## Algorithm & Model 📈

- This project uses a supervised classification model trained on an appropriate diabetes dataset (e.g., PIMA Indians Diabetes Dataset). 
- Typical steps used while preparing the
- model:
  - Data loading & inspection
  - Data cleaning & imputation (replace zeros in biological columns)
  - Feature scaling (StandardScaler)
  - Train/test split
  - Train classifier (e.g., RandomForestClassifier / LogisticRegression / XGBoost)
  - Evaluate (accuracy, confusion matrix, precision/recall)
  - Save the trained scaler and model using pickle.dump to Model/standardScalar.pkl and Model/modelForPrediction.pkl.
 
- Important notes
  - Save both scaler and model to ensure consistent preprocessing during inference.
  - Keep track of NumPy/scikit-learn versions used to pickle — mixing incompatible versions causes ModuleNotFoundError or other pickle load errors. 🔁
 
## Functions (Code-Level) 🛠️

- Below are the major functions/route handlers in app.py (or application.py) and what they do:
  - generate_user_id() → returns a unique UserID (string) for a patient. 🆔
  - generate_password() → returns a random password for the user. 🔑
  - @app.route('/register') → Render registration page (form collects name, age, address, mobile, problem). 📝
  - @app.route('/save_registration', methods=['POST']) → Save registration form data to patients_register.xlsx and return login page showing generated credentials. 💾
  - @app.route('/') and @app.route('/login') → Render login page. 🔐
  - @app.route('/login_user', methods=['POST']) → Validate credentials from patients_register.xlsx, set session, redirect to /home. ✅
  - @app.route('/home') → Protected route: show prediction form (only if session exists). 🧾
  - @app.route('/predictdata', methods=['POST']) → Preprocess inputs with scaler, predict using model, save prediction to patients_data.xlsx, and render result page. 🤖
  - @app.route('/logout') → Clear session and redirect to login. 👋

## Project Structure 📁

    diabetes-predictor-clinic/
    ├── Model/
    │   ├── modelForPrediction.pkl         # pickled trained classifier
    │   └── standardScalar.pkl             # pickled StandardScaler
    ├── templates/
    │   ├── login.html
    │   ├── register.html
    │   ├── home.html
    │   └── single_prediction.html
    ├── static/                            # optional: css, js, images
    ├── patients_register.xlsx             # created after first registration
    ├── patients_data.xlsx                 # created after first prediction
    ├── requirements.txt
    ├── app.py (or application.py)         # main Flask app
    └── README.md

## Process / Flow 🔁

- High-level steps
  - Patient registers → Excel patients_register.xlsx updated. ✅
  - Patient logs in with generated credentials. 🔒
  - Logged-in patient fills input features. 📝
  - App loads standardScalar.pkl and modelForPrediction.pkl. Preprocess → Predict. 🧠
  - Save prediction to patients_data.xlsx. 💾
  - Show attractive result page with branding. 🎯

## Flow diagram
    
                    ┌──────────────────────┐
                    │ Patient Registration │
                    └──────────┬──────────┘
                               │
                Generate User ID & Password
                               │
                    ┌──────────▼──────────┐
                    │   Login Page        │
                    └──────────┬──────────┘
                               │
                       Authenticated?
                               │
                 ┌────────────┴────────────┐
                 │                          │
               Yes                         No
                 │                          │
     ┌───────────▼───────────┐     ┌───────────────┐
     │ Diabetes Prediction    │    │ Show Error    │
     └───────────┬───────────┘     └───────────────┘
                 │
     ┌───────────▼───────────┐
     │ Show Final Result      │
     └────────────────────────┘


### ASCII sketch:

  - Register --> Save register.xlsx --> Login
  - Login --valid--> Home (prediction form)
  - Home --submit-> Preprocess -> Model -> Save predictions.xlsx -> Result page

## Sample Output 📤

| PatientName | Age | Address | Mobile | Problem         | UserID       | Password |
| ----------- | --- | ------- | ------ | --------------- | ------------ | -------- |
| John Doe    | 45  | Delhi   | 98765  | fatigue,thirsty | USR123456789 | aB9f4E2x |
| UserID       | PatientName | Glucose | BMI  | Age | Prediction |
| ------------ | ----------- | ------- | ---- | --- | ---------- |
| USR123456789 | John Doe    | 148     | 33.6 | 45  | Diabetic   |

## Benefits 🏆

- Easy patient tracking for clinics and demo setups. 📇
- Simple authentication per patient. 🔐
- Offline records in Excel make audits & exports simple. 📁
- Lightweight and easy to host (Heroku, Railway, Render, AWS Elastic Beanstalk). ☁️
- Teachable example to demonstrate model inference in web apps. 🎓

# Key Features

## 1.LogIN/Signup
<img width="1915" height="938" alt="Screenshot 2025-11-19 205231" src="https://github.com/user-attachments/assets/60840191-a028-4fb6-9228-680d4cd552b3" />

## 2.Auto User ID & Password Generator
<img width="668" height="565" alt="Screenshot 2025-11-19 205352" src="https://github.com/user-attachments/assets/167809c4-d6b3-469f-856c-eff21f0c925f" />

## 3.Diabetes Prediction Form
<img width="1919" height="933" alt="Screenshot 2025-11-19 205240" src="https://github.com/user-attachments/assets/b1d45840-b3cd-42a7-a05f-8648d6860c4a" />

## 4.Beautiful UI
<img width="664" height="378" alt="Screenshot 2025-11-19 205331" src="https://github.com/user-attachments/assets/66d68f4b-f45f-4f53-b0b3-4a4852bbdfa3" />



# Conclusion 🧾

- This project demonstrates how to convert an ML model into a user-accessible web service with meaningful UX for patients and clinics.
  It covers registration, authentication, secure model inference, and persistence of data — an excellent template for small healthcare demos or PoCs.
