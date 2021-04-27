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
    # count number of hikes in the db
    total_hikes = mongo.db.hikes.count_documents({})
    # sum the lengths of all the hikes in the db
    sum_hike_lengths = mongo.db.hikes.aggregate([{
        '$group': {
            '_id': 'null',
            'total': {
                '$sum': '$length'
            }
        }
    }])
    sum_hike_lengths = (list(sum_hike_lengths)[0]['total'])

    # count number of hikes in each area
    dublin_hikes_count = mongo.db.hikes.find(
        {'area': 'Dublin Mountains'}).count()
    wicklow_hikes_count = mongo.db.hikes.find(
        {'area': 'Wicklow Mountains'}).count()
    kerry_hikes_count = mongo.db.hikes.find(
        {'area': 'Kerry Mountains'}).count()

    return render_template('hikes.html',
                           hikes=hikes,
                           sum_hike_lengths=sum_hike_lengths,
                           total_hikes=total_hikes,
                           dublin_hikes_count=dublin_hikes_count,
                           wicklow_hikes_count=wicklow_hikes_count,
                           kerry_hikes_count=kerry_hikes_count)


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
    if request.method == 'POST':
        # check if username already exists in the db
        existing_user = mongo.db.users.find_one(
            {'username': request.form.get('username')})
            
        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                existing_user['password'], request.form.get('password')):
                session['user'] = request.form.get('username')
                flash('Welcome, {}'.format(
                    request.form.get('username')),
                    category='success')
                return redirect(url_for('get_hikes'))

            else:
                # invalid password match
                flash('Incorrect username and/or password', category='danger')
                return redirect(url_for('login'))
        else:
            # username does not exist
            flash('Incorrect username and/or password', category='danger')
            return redirect(url_for('login'))

    return render_template('login.html')


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
