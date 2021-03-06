import os
import logging
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
@app.route('/home')
def home():
    '''
    Returns the 4 most recently added hikes from the database.
    Renders home page.
    '''
    # get the 4 most recently added hikes from the db
    latest_hikes = list(mongo.db.hikes.find())[-4:]
    return render_template('home.html', latest_hikes=latest_hikes)


@app.route('/get_hikes')
def get_hikes():
    '''
    Calculates the total amount of hikes in the database.
    Calculates the sum of all the hike lengths in the database.
    Calculates the total amount of hikes for each area in the database.
    Renders the hikes.html template.
    '''
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
    hikes_per_area = []
    areas = list(mongo.db.areas.find())
    for area in areas:
        hikes_per_area.append({
            'name': area['name'],
            'num': mongo.db.hikes.find(
                    {'area': area['name']}).count()})

    return render_template('hikes.html',
                           hikes=hikes,
                           sum_hike_lengths=sum_hike_lengths,
                           total_hikes=total_hikes,
                           hikes_per_area=hikes_per_area)


@app.route('/register', methods=['GET', 'POST'])
def register():
    '''
    Renders registration page.
    Redirects to register page if username already exists in
    the database and registration fails.
    Redirects to the hikes page if registration is successful.
    '''
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
    '''
    Renders the login page.
    Redirects to the profile page if login successful.
    Redirects to the login page if login unsuccessful.
    '''
    if request.method == 'POST':
        # check if username already exists in the db
        existing_user = mongo.db.users.find_one(
            {'username': request.form.get('username')})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                                    existing_user['password'],
                                    request.form.get('password')):
                session['user'] = request.form.get('username')
                flash('Welcome, {}'.format(
                    request.form.get('username')),
                    category='success')
                return redirect(url_for('profile', username=session['user']))

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
    '''
    Removes user from session cookies.
    '''
    flash('You have been logged out', category='success')
    session.pop('user')
    return redirect(url_for('login'))


@app.route('/profile/<username>', methods=['GET', 'POST'])
def profile(username):
    '''
    Renders the profile page.
    Returns the hike details that the logged-in user has completed.
    Returns the total number of hikes the logged-in user has completed.
    Returns the total length of all the hikes the logged-in user has completed.
    '''
    hikes = mongo.db.hikes.find()
    '''loop through all hikes in db,
    all hikes that the user has hiked
    are appended to users_hikes array
    '''
    users_hikes = []
    total_hikes_length = 0

    ##TODO Refactor code to remove triple nested for loop
    for hike in hikes:
        for hiker in hike['hiked_by']:
            for name in hiker.keys():
                if name == session['user']:
                    users_hikes.append(hike)
                    # calculate total length of all hikes user has hiked
                    total_hikes_length += hike['length']

    total_hikes = len(users_hikes)

    if session['user']:
        return render_template(
                            'profile.html',
                            hikes=hikes,
                            users_hikes=users_hikes,
                            total_hikes=total_hikes,
                            total_hikes_length=total_hikes_length)
    return redirect(url_for('login'))


@app.route('/hike/<hike_id>')
def hike(hike_id):
    '''
    Renders the relevent hike page.
    Returns the names of the hikers that have completed the hike.
    Returns the date the logged-in user completed the hike.
    '''
    hike = mongo.db.hikes.find_one({'_id': ObjectId(hike_id)})
    hikers = []
    user_hike_date = ''
    for hiker in hike['hiked_by']:
        for name, date in hiker.items():
            hikers.append(name)
            # Find the date the logged-in user completed the hike
            if name == session['user']:
                user_hike_date = date
    return render_template(
                            'hike.html',
                            hike=hike,
                            hikers=hikers,
                            user_hike_date=user_hike_date)


@app.route('/add_hike', methods=['GET', 'POST'])
def add_hike():
    '''
    Renders the add hike page.
    Redirects to the hikes page when a hike is
    successfully added to the database.
    '''
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
    # areas and times required to populate the dropdown menus of the form
    areas = mongo.db.areas.find().sort('name', 1)
    times = mongo.db.times.find().sort('time', 1)
    return render_template('add_hike.html', areas=areas, times=times)


@app.route('/edit_hike/<hike_id>', methods=['GET', 'POST'])
def edit_hike(hike_id):
    '''
    Renders the edit hike page.
    Redirects to the hike page when a hike is successfully edited.
    '''
    hike = mongo.db.hikes.find_one({'_id': ObjectId(hike_id)})
    hikers = hike['hiked_by']
    original_hike_date = ''

    ##TODO replace triple nested for loop with mongodb query
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
    return render_template(
                            'edit_hike.html',
                            hike=hike,
                            areas=areas,
                            times=times,
                            original_hike_date=original_hike_date)


@app.route('/delete_hike/<hike_id>', methods=['GET', 'POST'])
def delete_hike(hike_id):
    '''
    Renders the delete a hike page.
    Deletes a hike from the database.
    Redirect to the hikes page after the
    successfull deletion of a hike.
    '''
    if request.method == 'POST':
        mongo.db.hikes.remove({'_id': ObjectId(hike_id)})
        flash('Hike successfully deleted', category='success')
        return redirect(url_for('get_hikes'))
    hike = mongo.db.hikes.find_one({'_id': ObjectId(hike_id)})
    return render_template('delete_hike.html', hike=hike)


@app.route('/complete_hike/<hike_id>', methods=['GET', 'POST'])
def complete_hike(hike_id):
    '''
    Renders the complete hike page.
    Updates the hiked_by field of the database.
    '''
    hike = mongo.db.hikes.find_one({'_id': ObjectId(hike_id)})
    if request.method == 'POST':
        mongo.db.hikes.update(
            {'name': hike['name']},
            {'$push': {
                        'hiked_by':
                        {session['user']: request.form.get('date')}}})
        flash('Hike Completed', category='success')
        return redirect(url_for('hike', hike_id=hike['_id']))
    return render_template('complete_hike.html', hike=hike)


@app.route('/incomplete_hike/<hike_id>', methods=['GET', 'POST'])
def incomplete_hike(hike_id):
    '''
    Renders the complete hike page.
    Updates the hiked_by field of the database.
    '''
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


def role_required(role_name):
    '''
    Checks if the current user is an admin or not.
    Throws a 403 error if not an admin.
    Throws a 403 error if not logged-in.
    '''
    def decorator(func):
        @wraps(func)
        def authorize(*args, **kwargs):
            logged_in = True
            try:
                if session['user'] != 'admin':
                    abort(403)
            except Exception as e:
                logging.info(e)
                logged_in = False
            if not logged_in:
                abort(403)
            return func(*args, **kwargs)
        return authorize
    return decorator


@app.errorhandler(403)
def error_403(e):
    '''
    Renders the custom 403 error page.
    '''
    return render_template('403.html')


@app.errorhandler(404)
def error_404(e):
    '''
    Renders the custom 404 error page.
    '''
    return render_template('404.html')


@app.route('/dashboard')
@role_required('admin')
def dashboard():
    '''
    Renders the dashboard page.
    Returns the hike areas and times from the database.
    '''
    areas = list(mongo.db.areas.find().sort('name', 1))
    times = list(mongo.db.times.find().sort('time', 1))
    return render_template('dashboard.html', areas=areas, times=times)


@app.route('/add_area', methods=['GET', 'POST'])
@role_required('admin')
def add_area():
    '''
    Renders the add area page.
    Redirects to the dashboard on successful adding of an area.
    '''
    if request.method == 'POST':
        area = {'name': request.form.get('name')}
        mongo.db.areas.insert_one(area)
        flash('Area successfully added', category='success')
        return redirect(url_for('dashboard'))
    return render_template('add_area.html')


@app.route('/edit_area/<area_id>', methods=['GET', 'POST'])
@role_required('admin')
def edit_area(area_id):
    '''
    Renders the edit area page.
    Redirects to the dashboard on successful editing of an area.

    '''
    area = mongo.db.areas.find_one({'_id': ObjectId(area_id)})
    if request.method == 'POST':
        area = {
            'name': request.form.get('name')
        }
        mongo.db.areas.update({'_id': ObjectId(area_id)}, area)
        flash('Area successfully edited', category='success')
        return redirect(url_for('dashboard'))
    return render_template('edit_area.html', area=area)


@app.route('/delete_area/<area_id>', methods=['GET', 'POST'])
@role_required('admin')
def delete_area(area_id):
    '''
    Renders the delete area page.
    Redirects to the dashboard on successful deletion of an area.
    '''
    if request.method == 'POST':
        mongo.db.areas.remove({'_id': ObjectId(area_id)})
        flash('Area successfully deleted', category='success')
        return redirect(url_for('dashboard'))
    area = mongo.db.areas.find_one({'_id': ObjectId(area_id)})
    return render_template('delete_area.html', area=area)


@app.route('/add_time', methods=['GET', 'POST'])
@role_required('admin')
def add_time():
    '''
    Renders the add time page.
    Redirects to the dashboard on successful adding of a time.
    '''
    if request.method == 'POST':
        time = {'time': request.form.get('time')}
        mongo.db.times.insert_one(time)
        flash('Time successfully added', category='success')
        return redirect(url_for('dashboard'))
    return render_template('add_time.html')


@app.route('/edit_time/<time_id>', methods=['GET', 'POST'])
@role_required('admin')
def edit_time(time_id):
    '''
    Renders the edit time page.
    Redirects to the dashboard on successful editing of a time.
    '''
    time = mongo.db.times.find_one({'_id': ObjectId(time_id)})
    if request.method == 'POST':
        time = {
            'time': request.form.get('time')
        }
        mongo.db.times.update({'_id': ObjectId(time_id)}, time)
        flash('Time successfully edited', category='success')
        return redirect(url_for('dashboard'))
    return render_template('edit_time.html', time=time)


@app.route('/delete_time/<time_id>', methods=['GET', 'POST'])
def delete_time(time_id):
    '''
    Renders the delete time page.
    Redirects to the dashboard on successful deletion of a time.
    '''
    if request.method == 'POST':
        mongo.db.times.remove({'_id': ObjectId(time_id)})
        flash('Time successfully deleted', category='success')
        return redirect(url_for('dashboard'))
    time = mongo.db.times.find_one({'_id': ObjectId(time_id)})
    return render_template('delete_time.html', time=time)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=False)
