import os
from functools import wraps
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for, abort)
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


@app.route('/logout')
def logout():
    # remove user from session cookies
    flash('You have been logged out', category='success')
    session.pop('user')
    return redirect(url_for('login'))


@app.route('/profile/<username>', methods=['GET', 'POST'])
def profile(username):
    hikes = mongo.db.hikes.find()

    '''loop through all hikes in db,
    all hikes that the user has hiked
    are appended to users_hikes array'''
    users_hikes = []
    total_hikes_length = 0

    for hike in hikes:
        for hiker in hike['hiked_by']:
            for name in hiker.keys():
                if name == session['user']:
                    users_hikes.append(hike)
                    # calculate total length of all hikes user has hiked
                    total_hikes_length += hike['length']

    total_hikes = len(users_hikes)

    if session['user']:
        return render_template('profile.html',
                                hikes=hikes,
                                users_hikes=users_hikes,
                                total_hikes=total_hikes,
                                total_hikes_length=total_hikes_length)
    return redirect(url_for('login'))


@app.route('/hike/<hike_id>')
def hike(hike_id):
    hike = mongo.db.hikes.find_one({'_id': ObjectId(hike_id)})
    hikers = []
    user_hike_date = ''
    for hiker in hike['hiked_by']:
        for name, date in hiker.items():
            hikers.append(name)
            if name == session['user']:
                user_hike_date = date
    return render_template('hike.html', hike=hike, hikers=hikers, user_hike_date=user_hike_date)


@app.route('/add_hike', methods=['GET', 'POST'])
def add_hike():
    if request.method == 'POST':
        hike = {
            'name': request.form.get('name'),
            'area': request.form.get('area'),
            'length': float(request.form.get('length')),
            'time': request.form.get('time'),
            'notes': request.form.get('notes'),
            'added_by': session['user'],
            'img_url': request.form.get('photo')
        }
        mongo.db.hikes.insert_one(hike)
        mongo.db.hikes.update(
            {'name': hike['name']},
            {'$push':
                {'hiked_by':
                    {session['user']: request.form.get('date')}}})
        flash('Hike successfully added', category='success')
        return redirect(url_for('get_hikes'))
    areas = mongo.db.areas.find().sort('name', 1)
    times = mongo.db.times.find().sort('time', 1)
    return render_template('add_hike.html', areas=areas, times=times)


@app.route('/edit_hike<hike_id>', methods=['GET', 'POST'])
def edit_hike(hike_id):
    hike = mongo.db.hikes.find_one({'_id': ObjectId(hike_id)})
    hikers = hike['hiked_by']
    original_hike_date = ''

    ##TODO replace nested for loop with mongodb query
    for hiker in hikers:
        for name in hiker.keys():
            if name == session['user']:
                # save original hike date to populate date input of form
                original_hike_date = hiker[name]
                # update users hike date with new date from form
                hiker[name] = request.form.get('date')

    if request.method == 'POST':
        submit = {
            'name': request.form.get('name'),
            'area': request.form.get('area'),
            'length': float(request.form.get('length')),
            'time': request.form.get('time'),
            'notes': request.form.get('notes'),
            'added_by': session['user'],
            'img_url': request.form.get('photo'),
            'hiked_by': hikers
        }
        mongo.db.hikes.update({'_id': ObjectId(hike_id)}, submit)
        flash('Hike successfully edited', category='success')
        return redirect(url_for('hike', hike_id=hike['_id']))

    # areas and times required to populate the form
    areas = mongo.db.areas.find().sort('name', 1)
    times = mongo.db.times.find().sort('time', 1)
    return render_template('edit_hike.html', hike=hike, areas=areas, times=times, original_hike_date=original_hike_date)


@app.route('/delete_hike<hike_id>', methods=['GET', 'POST'])
def delete_hike(hike_id):
    if request.method == 'POST':
        mongo.db.hikes.remove({'_id': ObjectId(hike_id)})
        flash('Hike successfully deleted', category='success')
        return redirect(url_for('get_hikes'))
    hike = mongo.db.hikes.find_one({'_id': ObjectId(hike_id)})
    return render_template('delete_hike.html', hike=hike)


@app.route('/complete_hike/<hike_id>', methods=['GET', 'POST'])
def complete_hike(hike_id):
    hike = mongo.db.hikes.find_one({'_id': ObjectId(hike_id)})
    if request.method == 'POST':
        mongo.db.hikes.update(
            {'name': hike['name']},
            {'$push': {'hiked_by': {session['user']: request.form.get('date')}}})
        flash('Hike Completed', category='success')
        return redirect(url_for('hike', hike_id=hike['_id']))
    return render_template('complete_hike.html', hike=hike)


@app.route('/incomplete_hike/<hike_id>', methods=['GET', 'POST'])
def incomplete_hike(hike_id):
    hike = mongo.db.hikes.find_one({'_id': ObjectId(hike_id)})
    user_hike_date = ''
    for hiker in hike['hiked_by']:
        for name, date in hiker.items():
            if name == session['user']:
                user_hike_date = date
    if request.method == 'POST':
        mongo.db.hikes.update(
            {'name': hike['name']},
            {'$pull': {'hiked_by': {session['user']: user_hike_date}}})
        flash('Hike marked as incomplete', category='success')
        return redirect(url_for('hike', hike_id=hike['_id']))
    return render_template('incomplete_hike.html', hike=hike)


# CREDIT - https://stackoverflow.com/questions/25233188/what-is-the-best-way-to-protect-a-flask-endpoint
def role_required(role_name):
    def decorator(func):
        @wraps(func)
        def authorize(*args, **kwargs):
            if session['user'] != 'admin':
                abort(403)
            return func(*args, **kwargs)
        return authorize
    return decorator


@app.errorhandler(403)
def resource_not_found(e):
    return render_template('403.html')


@app.route('/dashboard')
@role_required('admin')
def dashboard():
    areas = list(mongo.db.areas.find().sort('name', 1))
    times = list(mongo.db.times.find().sort('time', 1))
    return render_template('dashboard.html', areas=areas, times=times)


@app.route('/add_area', methods=['GET', 'POST'])
@role_required('admin')
def add_area():
    if request.method == 'POST':
        area = {'name': request.form.get('name')}
        mongo.db.areas.insert_one(area)
        flash('Area successfully added', category='success')
        return redirect(url_for('dashboard'))

    return render_template('add_area.html')


@app.route('/delete_area<area_id>', methods=['GET', 'POST'])
def delete_area(area_id):
    if request.method == 'POST':
        mongo.db.areas.remove({'_id': ObjectId(area_id)})
        flash('Area successfully deleted', category='success')
        return redirect(url_for('dashboard'))
    area = mongo.db.areas.find_one({'_id': ObjectId(area_id)})
    return render_template('delete_area.html', area=area)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
