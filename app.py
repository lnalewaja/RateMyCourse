from flask import Flask, redirect, render_template, url_for, session

app = Flask(__name__)
app.secret_key = 'super_secret_key'

courses = [
    {
        'course_id': 'ITSC-3146',
        'course_name': 'Intro to Operating Systems and Networking',
        'description': 'Class Description',
        'teacher': 'Harini Ramaprasad',
        'comments': [
            'This course was hard.',
            'It was so much work!',
            'I thought it was not too bad.'
        ]
    },
    {
        'course_id': 'ITSC-3155',
        'course_name': 'Intro to Software Engineering',
        'description': 'Class Description',
        'teacher': 'Jacob Krevat',
        'comments': [
            'This course was hard.',
            'It was so much work!',
            'I thought it was not too bad.'
        ]
    }
]

@app.get('/')
def index():
    # Loads the Home Page.
    return render_template('index.html')

@app.get('/courses')
def load_courses():
    # Loads Courses Page - shows all courses.
    return render_template('coureses.html')

@app.get('/courses/new')
def add_page():
    # Loads the New Course Page - has for to add a new course.
    return render_template('new_course_page.html')

@app.post('/courses/new')
def add_course():
    # Makes post request to create new course.
    # add code here to add course to the database
    return redirect('/courses')

@app.get('/courses/<int:course_id>')
def couse_page():
    # Loads the Course Details Page - Shows specific details and reviews of the selected course.
    return render_template('course_details.html')

@app.get('/courses/<int:course_id>/edit')
def edit_course():
    # Loads the Edit Page.
    # Make sure previous details are autofilled into the form.
    return render_template('course_edit_page.html')

@app.post('/courses/<int:course_id>/edit')
def submit_edit_course():
    # Makes post request to change the courses data on the database.
    # Add code to pull the data from the html edit page and make changes to the course
    return redirect('/courses/<int:course_id>')


@app.route('/login')
def login():
    #This is for after someone logs in the navbar will change to say "Welcome, John" or whatever
    # After successful login, set the user's name in the session.
    session['username'] = 'John Doe'  # Example user name
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    #This is for after someone logs in the navbar will change to say "Welcome, John" or whatever
    # After successful login, set the user's name in the session.
    session['username'] = ''  # Example user name
    return redirect(url_for('index'))