from flask import Flask, request, redirect, render_template, session, url_for,make_response,flash,jsonify  
from joblib import load
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask_mail import Mail, Message
from datetime import datetime
import numpy as np

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose, AdminIndexView
from flask_admin.actions import action
from itsdangerous import BadSignature
import joblib
import xgboost as xgb
import numpy as np
import pickle


app = Flask(__name__, template_folder='templates', static_folder='static')

ADMIN_EMAIL = 'oleh.shevchenko@nure.ua'
ADMIN_PASSWORD = '228'

app.secret_key = '9d9f0b6ee5f44e7dbd4c4a2eb1f3d1db' 


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:2287@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'oleh.shevchenko@nure.ua'
app.config['MAIL_PASSWORD'] = 'kjmv vjlr ldrm blmx'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


db = SQLAlchemy(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])



@app.route('/')
def index():
    user_email = session.get('user_email')
    return render_template('service.html', user_email=user_email)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')


        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect('/admin')
        

        if not email or not password:
            return render_template('transparent-login-form.html', error='Missing credentials'), 400

        user = User.query.filter_by(email=email).first()

        if user:
            if user.check_password(password):
                if user.confirmed:
                    session['user_email'] = user.email
                    response = make_response(redirect(url_for('success_page')))
                    response.set_cookie('user_email', user.email, max_age=60*60*24*30)  # Save cookie for 30 days
                    return response
                else:

                    flash('Please confirm your email address.', 'warning')
                    return render_template('transparent-login-form.html'), 401
            else:
                return render_template('transparent-login-form.html', error='Invalid credentials'), 401
        else:

            new_user = User(email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()


            flash('A confirmation email has been sent to your email address.', 'info')
            return redirect(url_for('index'))  

    else:
        if 'user_email' in session:

            return redirect(url_for('success_page'))


        return render_template('transparent-login-form.html')


file_path = 'static/model/regressor_bikes.pkl'
model_job = None

if os.path.isfile(file_path):
    model_job = load(file_path)
    print(f'All right: {model_job}') 
    booster = model_job.get_booster()
    num_features = len(booster.feature_names)
    print(f"The model expects {num_features} features.")
else:
    print(f"Error: The file {file_path} does not exist.")



@app.route('/predict', methods=['POST'])
def predict():

    hour = request.form.get('hour', type=float)
    temperature = request.form.get('temperature', type=float)
    humidity = request.form.get('humidity', type=float)
    solar_radiation = request.form.get('solarRadiation', type=float)
    rainfall = request.form.get('rainfall', type=float)
    snowfall = request.form.get('snowfall', type=float)
    day = request.form.get('day',  type=int)
    month = request.form.get('month', type=int)


    holiday = ['holiday', 'no_holiday']
    chosen_holiday = request.form.get('holiday')
    holiday_encoded = [1 if chosen_holiday == h else 0 for h in holiday]

    features = [
        hour,
        temperature,
        humidity,
        solar_radiation,
        rainfall,
        snowfall,
        day,
        month
    ] + holiday_encoded

    features = [features]
    print(features)

    y_pred = model_job.predict(features)
    y_pred = np.round(y_pred,0)
    y_pred_list = y_pred.tolist() 

    return jsonify(predicted_value=y_pred_list[0])



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True,host='0.0.0.0')



    


