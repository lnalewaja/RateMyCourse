from flask import Flask, redirect, render_template, url_for, session, request
from werkzeug.security import check_password_hash, generate_password_hash

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
            'This course was hard.',
            'It was so much work!',
            'This course was hard.',
            'It was so much work!',
            'This course was hard.',
            'It was so much work!',
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
    search_query = request.args.get('search_query', '')  # Get the search query from the request
    if search_query:
        # Filter courses based on the search query
        filtered_courses = [course for course in courses if search_query.lower() in course['course_name'].lower()]
        return render_template('courses.html', courses=filtered_courses, search_query=search_query)
    else:
        return render_template('courses.html', courses=courses)


@app.get('/courses/new')
def add_page():
    # Loads the New Course Page - has for to add a new course.
    return render_template('new_course_page.html')

@app.post('/courses/new')
def add_course():
    # Makes post request to create new course.
    # add code here to add course to the database
    return redirect('/courses')

@app.get('/courses/<string:course_id>')
def course_page(course_id):
    for course in courses:
        if course['course_id'] == course_id:
            return render_template('course_details.html', course=course)
    return 'Course not found', 404

@app.get('/courses/<string:course_id>/edit')
def edit_course():
    # Loads the Edit Page.
    # Make sure previous details are autofilled into the form.
    return render_template('course_edit_page.html')

@app.post('/courses/<string:course_id>/edit')
def submit_edit_course():
    # Makes post request to change the courses data on the database.
    # Add code to pull the data from the html edit page and make changes to the course
    return redirect('/courses/<int:course_id>')


users = {
    'test_user': {
        'username': 'test_user',
        'password_hash': generate_password_hash('test_password')
    }
}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users.get(username)

        # Check if user exists and password is correct
        if user and check_password_hash(user['password_hash'], password):
            # If valid, we could log them in and store the user id in the session
            session['username'] = user['username']
            return redirect(url_for('index'))
        else:
            # If user doesn't exist or password is wrong, reload the page with an error
            return render_template('login.html', error="Invalid username or password")
    
    # For a GET request, just render the template
    return render_template('login.html')

@app.route('/logout')
def logout():
    #This is for after someone logs out it'll go back to showing Log in Sign up buttons
    session['username'] = ''  
    return redirect(url_for('index'))