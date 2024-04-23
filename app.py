from flask import Flask, redirect, render_template, url_for, session, request
from werkzeug.security import check_password_hash, generate_password_hash
from dotenv import load_dotenv

from repositories import course_repo

load_dotenv()

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
            {
                'user_id': '1',
                'name': 'Landon Nalewaja',
                'rating': '3',
                'final_grade': 'B',
                'comment': 'This course was hard.'
            },
            {
                'user_id': '2',
                'name': 'Ronni Elhadidy',
                'rating': '4',
                'final_grade': 'A',
                'comment': 'It was so much work!'
            },
            {
                'user_id': '3',
                'name': 'Kendall Tart',
                'rating': '2',
                'final_grade': 'C',
                'comment': 'I thought it was not too bad.'
            }
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
            {
                'user_id': '1',
                'name': 'Landon Nalewaja',
                'rating': '3',
                'final_grade': 'B',
                'comment': 'This course was hard.'
            },
            {
                'user_id': '2',
                'name': 'Ronni Elhadidy',
                'rating': '4',
                'final_grade': 'A',
                'comment': 'It was so much work!'
            },
            {
                'user_id': '3',
                'name': 'Kendall Tart',
                'rating': '2',
                'final_grade': 'C',
                'comment': 'I thought it was not too bad.'
            }
        ]
    }
]
users = {
    'test_user': {
        'username': 'test_user',
        'password_hash': generate_password_hash('test_password'),
        'email': 'test@example.com' 
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
    course = course_repo.get_course_by_id(course_id)
    course_comments = course_repo.get_all_comments_with_course_id(course_id)
    
    return render_template('course_details.html', course=course, course_comments=course_comments)


@app.post('/courses/<string:course_id>/addComment')
def add_comment(course_id):
    user_id = 1 # need to change this value for fully functioning code when user sessions are created.
    rating = request.form.get('rating')
    final_grade = request.form.get('final_grade')
    comment = request.form.get('comment')
    result = course_repo.add_comment_to_course(course_id, user_id, rating, final_grade, comment)
    return redirect(f'/courses/{course_id}')

@app.post('/courses/<string:course_id>/editComment')
def edit_comment(course_id):
    rating = request.form.get('rating')
    final_grade = request.form.get('final_grade')
    comment = request.form.get('comment')
    review_id = request.form.get('review_id')
    result = course_repo.edit_comment_from_course(course_id, review_id, rating, final_grade, comment)
    return redirect(f'/courses/{course_id}')

@app.post('/courses/<string:course_id>/deleteComment')
def delete_comment(course_id):
    review_id = request.form.get('review_id')
    user_id = request.form.get('user_id')
    print(review_id)
    print(user_id)
    result = course_repo.delete_comment_from_course(course_id, user_id, review_id)
    return redirect(f'/courses/{course_id}')


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
    new_description = request.form.get('description')
    new_course_number = request.form.get('course_number')
    new_instructor = request.form.get('instructor')

    # Update the course data in the courses list
    for course in courses:
        if course['course_id'] == course_id:
            # Update only the fields that have been provided in the form
            if new_description:
                course['description'] = new_description
            if new_course_number:
                course['course_id'] = new_course_number
            if new_instructor:
                course['teacher'] = new_instructor
            break
    else:
        return 'Course not found', 404

    # Redirect to the course detail page after editing
    return redirect(f'/courses/{course_id}')

@app.route('/faq')
def faq():
    return render_template('faq.html')



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
    session['username'] = ''  
    return redirect(url_for('index'))

@app.get('/signup')
def show_signup_form():
    return render_template('signup.html')

@app.post('/signup')
def process_signup():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if not all([username, email, password, confirm_password]):
        return render_template('signup.html', error='Please fill out all fields.')
    if password != confirm_password:
        return render_template('signup.html', error='Passwords do not match.')

    if username in users or any(user.get('email') == email for user in users.values()):
        return render_template('signup.html', error='Username or email already exists.')

    users[username] = {
        'username': username,
        'email': email,
        'password_hash': generate_password_hash(password)
    }

    return redirect(url_for('login'))

