from flask import Flask, render_template, redirect, url_for, jsonify
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField, SelectField
from wtforms.validators import InputRequired, Email, Length
import numpy as np
import pickle
import paypalrestsdk

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRETKEY'
bootstrap = Bootstrap(app)

paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  "client_id": "AY5WiJ0F0gTZGKSEO5nlomYaGjEF7jmsL7IUrUTt3HaJkczOpx87Ftb5UH3sAiP09HB55PzCnRJXBuU7",
  "client_secret": "EDAzX4j4AjE_P68ncqj5DufjaG4a0NBHDrErvxx5PLrF9qjkDeUSvj__bqynr0PbBs_8pos_INbq8Aw7" })

#######################################################

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

class PredictForm(FlaskForm):
    menopause = SelectField(u'menopause',choices=[(0, "premeno"),(1, "ge40"),(2, "lt40")], coerce=str)
    tumor_size = SelectField(u'tumor_size',choices=[(0, "0-4"),(1, "5-9"),(2, "10-14"),(3, "15-19"),(4, "20-24"),(5, "25-29"),(6, "30-34"),(7, "35-39"),(8, "40-44"),(9, '45-49'), (10,'50-54')], coerce=str)
    inv_nodes = SelectField(u'inv_nodes',choices=[(0, '0-2'),(1, '3-5'),(2, '6-8'),(3, '9-11'),(4, '12-14'),(5, '15-17'),(6,'24-26')], coerce=str)
    breast = SelectField(u'breast',choices=[(0, "left"),(1, "right")], coerce=str)
    breast_quad = SelectField(u'breast_quad',choices=[(0, "left_low"),(1, "right_up"),(2, "left_up"),(3, "right_low"),(4, "central")], coerce=str)
    deg_malig = SelectField(u'deg_malig',choices=[(3, "3"),(2, "2"),(1, "1")], coerce=str)
    irradiat = SelectField(u'irradiat',choices=[(0, "no"),(1, "yes")], coerce=str)
    node_caps = SelectField(u'node_caps',choices=[(0, "no"),(1, "yes")], coerce=str)
    age = SelectField(u'age',choices=[(0, '20-29'),(1, '30-39'),(2, '40-49'),(3, '50-59'),(4, '60-69'),(5, '70-79')], coerce=str)

class PredictFormFer(FlaskForm):
    Season = SelectField(u'Season in which the analysis was performed',choices=[(-1, "winter"),(-0.33, "spring"),(0.33, "Summer"),(1,"fall")], coerce=str)
    Age = SelectField(u'Age at the time of analysis',choices=[(0, "<24"),(1, ">24")], coerce=str)
    ChildDisease = SelectField(u'Childish diseases (ie , chicken pox, measles, mumps, polio) ',choices=[(0, 'Yes'),(1, 'No')], coerce=str)
    Accident = SelectField(u'Accident or serious trauma',choices=[(0, "Yes"),(1, "No")], coerce=str)
    Surgury = SelectField(u'Surgical intervention',choices=[(0, "Yes"),(1, "No")], coerce=str)
    HighFever = SelectField(u'High fevers in the last year',choices=[(-1, " less than three months ago"),(0, "more than three months ago"),(1, "no")], coerce=str)
    Alcohol = SelectField(u'Frequency of alcohol consumption',choices=[(0, "High"),(1, "Low")], coerce=str)
    Smoking = SelectField(u'Smoking habit',choices=[(0, "occasional"),(1, "daily"),(-1,"never")], coerce=str)
    SittingHours = SelectField(u'Number of hours spent sitting per day',choices=[(0, '< 3 hours'),(1, '> 3 hours')], coerce=str)

#######################################################

@app.route('/')
def homepage():
    return render_template('home.html') 

#######################################################

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = form.username.data
        print(form.username.data + ' ' + form.password.data)
        return redirect(url_for('dashboard'))

    return render_template('login.html', form=form)

#######################################################

@app.route('/signup', methods=['GET', 'POST'])  
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        print(form.username.data + ' ' + form.email.data + ' ' + form.password.data)
        return redirect(url_for('login'))

    return render_template('signup.html', form=form)

#######################################################

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

#######################################################

@app.route('/payment', methods=['POST'])
def payment():

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://localhost:5000/execute",
            "cancel_url": "http://localhost:5000/dashboard"},
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "medicalprediction",
                    "sku": "12345",
                    "price": "100.00",
                    "currency": "INR",
                    "quantity": 1}]},
            "amount": {
                "total": "100.00",
                "currency": "INR"},
            "description": "This is the payment transaction description."}]})

    if payment.create():
        print('Payment success!')
    else:
        print(payment.error)

    return jsonify({'paymentID' : payment.id})

#######################################################

@app.route('/execute', methods=['POST'])
def execute():

    payment = paypalrestsdk.Payment.find(request.form['paymentID'])

    if payment.execute({'payer_id' : request.form['payerID']}):
        print('Execute success!')
        return render_template('Fertility.html')
    else:
        print(payment.error)
        return render_template('dashboard.html')


#######################################################

@app.route('/BC', methods=['GET', 'POST'])
def BC():
    text_res = "Press Submit"
    form = PredictForm()
    if form.is_submitted():
        input_list = [ form.age.data, form.menopause.data, form.tumor_size.data, form.inv_nodes.data, form.node_caps.data, form.deg_malig.data, form.breast.data, form.breast_quad.data, form.irradiat.data]
        input_list = [int(i) for i in input_list]
        input_vector = np.array(input_list).reshape(1,-1)
        loaded_model = pickle.load(open("models/bc_svm.pkl", 'rb'))
        res = loaded_model.predict(input_vector)[0]
        print(res)
        if res == 0:
            text_res = "no recurrence events"
            print("predicted class: "+ " no recurrence events ")
        else:
            text_res = " recurrence events"
            print("predicted class: "+ " recurrence events ")


    return render_template('BC.html', form=form, text_res = text_res)

#######################################################

@app.route('/Fertility', methods=['GET', 'POST'])
def Fertility():
    text_res = "Press Submit"
    form = PredictFormFer()
    if form.is_submitted():
        input_list = [ form.Season.data, form.Age.data, form.ChildDisease.data, form.Accident.data, form.Surgury.data, form.HighFever.data, form.Alcohol.data, form.Smoking.data, form.SittingHours.data]
        input_list = [int(i) for i in input_list]
        input_vector = np.array(input_list).reshape(1,-1)
        loaded_model = pickle.load(open("models/fer_svm.pkl", 'rb'))
        res = loaded_model.predict(input_vector)[0]
        print(res)
        if res == 0:
            text_res = "Normal"
            print("predicted class: "+ " normal ")
        else:
            text_res = "Altered"
            print("predicted class: "+ " altered ")


    return render_template('Fertility.html', form=form, text_res = text_res)    

#######################################################

@app.route('/paypal')
def paypal():
    return render_template('paypal.html') 

#######################################################

@app.route('/logout')
def logout():
    return render_template('home.html') 

#######################################################

if __name__ == '__main__':
    app.run(debug = True)


