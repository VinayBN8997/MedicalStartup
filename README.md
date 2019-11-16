# Medical-Startup
Flask <br />
Stripe <br />
Machine-Learning <br />
HTML BOOTSTRAP <br />

# REQUIREMENTS

flask <br />
numpy <br />
pandas <br />
flask_bootstrap <br />
flask_wtf <br />
wtforms <br />
pickle <br />
paypalrestsdk <br />
seaborn (plotting inside notebook (optional)) <br />
sklearn <br />
gunicorn <br />
SQLAlchemy <br />
stripe <br />

# SCREEN SHOTS

<img width="1266" alt="INDEX" src="https://user-images.githubusercontent.com/33830482/66667380-88f8a680-ec70-11e9-81f6-55696a306dc5.png">
<img width="1268" alt="SIGNUP" src="https://user-images.githubusercontent.com/33830482/66667406-944bd200-ec70-11e9-951f-2b714b1cd797.png">
<img width="1267" alt="LOGIN" src="https://user-images.githubusercontent.com/33830482/66667408-94e46880-ec70-11e9-8483-999c9e420f5a.png">
<img width="1270" alt="DASHBOARD" src="https://user-images.githubusercontent.com/33830482/68994691-fcaf5400-08ab-11ea-8519-8f516b9e5de7.png">
<img width="1276" alt="BREAST CANCER" src="https://user-images.githubusercontent.com/33830482/68994811-13a27600-08ad-11ea-8ba2-b250e61671bd.png">
<img width="1270" alt="STRIPE" src="https://user-images.githubusercontent.com/33830482/68994695-033dcb80-08ac-11ea-9c5d-64e7b3f8ef92.png">
<img width="1268" alt="FERTILITY" src="https://user-images.githubusercontent.com/33830482/66667412-957cff00-ec70-11e9-8bc9-1e55db3d30a8.png">

# Huruku deployment

### Creating app

mkdir medical <br />
cd medical <br />
virtualenv medical <br />
source medical/bin/activate <br />
pip install Flask gunicorn <br />

### To test: gunicorn Hello:app

pip freeze > requirements.py <br />
touch Procfile <br />
web: gunicorn app:app <br />

### Git

git add . <br />
git commit -m "initial_commit" <br />
heroku create medical-project <br />
git push heroku master <br />

### Herorku Link:
Please feel free to check the live demo using the link
https://medical-ml-startup.herokuapp.com
