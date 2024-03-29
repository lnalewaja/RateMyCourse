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
        'rating': 3,  # test rating
        'grade': 'B',  # test grade
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
        'rating': 4,  # test rating
        'grade': 'A',  # test grade
        'comments': [
            'This course was hard.',
            'It was so much work!',
            'I thought it was not too bad.'
        ]
    }
]
users = {
    'test_user': {
        'username': 'test_user',
        'password_hash': generate_password_hash('test_password')
    }
}


@app.get('/')
def index():
    # Loads the Home Page.
    return render_template('index.html', no_search_bar=True)

@app.get('/course_page')
def load_courses():
    search_query = request.args.get('search_query', '')  # Get the search query from the request
    if search_query:
        # Filter courses based on the search query
        filtered_courses = [course for course in courses if search_query.lower() in course['course_name'].lower()]
        return render_template('course_page.html', courses=filtered_courses, search_query=search_query)
    else:
        return render_template('course_page.html', courses=courses)



@app.get('/courses/new')
def add_page():
    # Loads the New Course Page - has for to add a new course.
    return render_template('new_course_page.html')

@app.post('/courses/new')
def add_course():
    # Makes post request to create new course.
    # add code here to add course to the database
    return redirect('/courses')

@app.route('/create_course')
def create_course():
    return render_template('create_course.html')

@app.get('/courses/<string:course_id>')
def course_page(course_id):
    for course in courses:
        if course['course_id'] == course_id:
            return render_template('course_details.html', course=course)
    return 'Course not found', 404

@app.get('/courses/<string:course_id>/edit')
def edit_course(course_id):
    course = next((c for c in courses if c['course_id'] == course_id), None)
    if course:
        return render_template('course_edit_page.html', course=course)
    else:
        return "Course not found", 404


@app.post('/courses/<string:course_id>/edit')
def submit_edit_course(course_id):
    # Fetch the updated data from the form
    new_rating = request.form.get('rating')
    new_grade = request.form.get('final_grade')
    new_comment = request.form.get('new_comment')

    # Convert rating to an integer if it's not empty
    if new_rating:
        new_rating = int(new_rating)



    # Update the course data in the database (or your courses list)
    for course in courses:
        if course['course_id'] == course_id:
            # Update only the fields that have been provided in the form
            if new_rating is not None:
                course['rating'] = new_rating
            if new_grade:
                course['grade'] = new_grade
            # Update existing comments
            for i, comment in enumerate(course['comments']):
                updated_comment = request.form.get(f'comment_{i+1}')  # Get updated comment from form
                if updated_comment:
                    course['comments'][i] = updated_comment
            # Add new comment if provided
            if new_comment:
                course['comments'].append(new_comment)
            break
    else:
        return 'Course not found', 404

    # Redirect to the course detail page after editing
    return redirect(f'/courses/{course_id}')






if __name__ == '__main__':
    app.run(debug=True)

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