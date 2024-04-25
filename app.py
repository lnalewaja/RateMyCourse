from flask import Flask, redirect, render_template, url_for, session, request, jsonify, flash
from werkzeug.security import check_password_hash, generate_password_hash
from dotenv import load_dotenv
import openai
import os

openai.api_key = os.environ.get('api_key')



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
        allcourse = course_repo.get_all_courses()
        print(allcourse)
        return render_template('course_page.html', allcourse=allcourse)


@app.route('/get_courses', methods=['POST'])
def get_courses():
    course_name = request.form['course_name']
    page = int(request.form.get('page', 1))
    per_page = 8

    courses = []
    with open('listing.txt', 'r', encoding='utf-8') as file:
        for line in file:
            if course_name.lower() in line.lower():
                courses.append(line.strip())

    total_courses = len(courses)
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    paginated_courses = courses[start_index:end_index]

    return jsonify({
        'courses': paginated_courses,
        'total_courses': total_courses,
        'current_page': page,
        'total_pages': (total_courses + per_page - 1) // per_page
    })
    
@app.route('/instructor', methods=['POST'])
def get_instructors():
    instructor_name = request.form['instructor']
    page = int(request.form.get('page', 1))
    per_page = 8

    instructors = []
    with open('teachersunique.txt', 'r', encoding='utf-8') as file:
        for line in file:
            if instructor_name.lower() in line.lower():
                instructors.append(line.strip())

    total_instructors = len(instructors)
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    paginated_instructors = instructors[start_index:end_index]

    return jsonify({
        'instructors': paginated_instructors,
        'total_instructors': total_instructors,
        'current_page': page,
        'total_pages': (total_instructors + per_page - 1) // per_page
    })
    
def chat_with_gpt(prompt):
    courses = course_repo.get_all_courses()

    # Format each course dictionary as a string
    course_strings = []
    for course in courses:
        course_str = f"Course ID: {course['course_id']}\nTitle: {course['course_name']}\nDescription: {course['course_description']}\n"
        course_strings.append(course_str)

    # Join the course strings into a single string
    courses_str = "\n".join(course_strings)

    # Check if the user is asking about a specific course
    if prompt.lower().startswith("reviews:"):
        course_id = prompt.split(":")[1].strip()
        comments = course_repo.get_all_comments_with_course_id(course_id)

        # Format each comment as a string
        comment_strings = []
        for comment in comments:
            comment_str = f"Comment ID: {comment['review_id']}\nUser: {comment['user_id']}\nComment: {comment['comment']}\n"
            comment_strings.append(comment_str)

        # Join the comment strings into a single string
        comments_str = "\n".join(comment_strings)

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI assistant that provides helpful responses based on the given course information and comments when asked."},
                {"role": "system", "content": "Here are the comments for the requested course:\n" + comments_str},
                {"role": "user", "content": prompt}
            ]
        )
    else:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI assistant that provides helpful responses based on the given course information when asked."},
                {"role": "system", "content": "Here are all the available courses:\n" + courses_str},
                {"role": "user", "content": prompt}
            ]
        )
    return response.choices[0].message.content.strip()

@app.route("/gpt")
def home():
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json  # Access the JSON data sent by the client
    user_input = data.get("message", "")  # Get the message from the JSON data
    print(f"Received user input: {user_input}")
    response = chat_with_gpt(user_input)
    return jsonify({"response": response})
    
def replace_spaces_with_hyphens(course_id, course):
    concat = course_id + "-" + course
    return concat.replace(" ", "-")

@app.post('/courses/new')
def add_course():
    name = request.form['course_name']
    course = request.form['instructor']
    description = request.form['description']
    id = replace_spaces_with_hyphens(name, course)
    if course_repo.get_course_by_id(id):
        flash("Class already exists!")
        return redirect(url_for('course_page', course_id=id))
    else:
        course_repo.add_course(id ,name, course, description)
        return redirect(url_for('course_page', course_id=id))
    # Makes post request to create new course.
    # add code here to add course to the database
    return render_template('course_page.html')

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
    message = request.args.get('message', '')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        success, user_id, message = course_repo.login_user(username, password)
        if success:
            session['user_id'] = user_id
            session['username'] = username  # Store username in session
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login', submitted=True, message="Incorrect Password or Email"))

    return render_template('login.html', message=message)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)  # Clear the username from session
    flash('You have been logged out.')
    return redirect(url_for('index'))

@app.get('/signup')
def show_signup_form():
    return render_template('signup.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if not all([username, email, password, confirm_password]):
            flash('Please fill out all fields.')
            return redirect(url_for('signup'))
        if password != confirm_password:
            flash('Passwords do not match.')
            return redirect(url_for('signup'))

        # Call to the signup_user function in course_repo
        success, message = course_repo.signup_user(username, email, password)
        flash(message)
        if success:
            return redirect(url_for('login'))
        else:
            return redirect(url_for('signup'))

    return render_template('signup.html')
