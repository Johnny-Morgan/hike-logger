import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists('env.py'):
    import env

app = Flask(__name__)


app.config['MONGO_DBNAME'] = os.environ.get('MONGO_DBNAME')
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
app.secret_key = os.environ.get('SECRET_KEY')

mongo = PyMongo(app)


@app.route('/')
@app.route('/get_hikes')
def get_hikes():
    hikes = mongo.db.hikes.find()
    return render_template('hikes.html', hikes=hikes)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # check if username already exists in the database
        user = request.form.get('username')
        existing_user = mongo.db.users.find_one(
            {'username': request.form.get('username')})

        if existing_user:
            flash('The username "' + user + '" already exists',
                  category='danger')
            return redirect(url_for("register"))

        register = {'username': request.form.get('username'),
                    'password': generate_password_hash(
                        request.form.get('password'))
                    }

        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session['user'] = request.form.get('username')
        flash('Registration Successful!', category='success')
        return redirect(url_for('get_hikes'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
