from flask import Flask, redirect, render_template

app = Flask(__name__)

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

@app.post('/courses/<int:course_id/edit')
def submit_edit_course():
    # Makes post request to change the courses data on the database.
    # Add code to pull the data from the html edit page and make changes to the course
    return redirect('/courses/<int:course_id>')