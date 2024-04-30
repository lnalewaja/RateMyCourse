from flask import Flask, redirect, render_template, url_for, session, request, jsonify, flash
from werkzeug.security import check_password_hash, generate_password_hash
import requests
from dotenv import load_dotenv
import openai
import os
from authlib.integrations.flask_client import OAuth
from requests.structures import CaseInsensitiveDict

openai.api_key = os.environ.get('api_key')



from repositories import course_repo

load_dotenv()

app = Flask(__name__)
oauth = OAuth(app)
app.secret_key = 'super_secret_key'
google = oauth.register(
    name='google',
    client_id=os.environ.get('client_id'),
    client_secret=os.environ.get('secret_key'),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid profile email'},
    jwks_uri='https://www.googleapis.com/oauth2/v3/certs',
)


def is_valid(email: str):
    url = f"https://www.ipqualityscore.com/api/json/email/x6909hRFZmkdLzmcNP4jBNZ0C0Lq5Q1m/{email}"

    headers = CaseInsensitiveDict()
    headers["apikey"] = os.environ.get('email_validate')

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        json_resp = response.json()
        format_valid = json_resp["format_valid"]
        mx_found = json_resp["mx_found"]
        smtp_check = json_resp["smtp_check"]
        state = json_resp["state"]

        return format_valid and mx_found and smtp_check and state == "deliverable"

    return False


admin = ['ktart2@uncc.edu', 'ktart2@charlotte.edu', 'ramanna@charlotte.edu', 'ramanna@uncc.edu', 'kamanna@uncc.edu', 'kamanna@charlotte.edu', 'lnalewaj@uncc.edu', 'lnalewaj@charlotte.edu', 'relhadid@charlotte.edu', 'relhadid@uncc.edu']



@app.get('/')
def index():
    email = dict(session).get('email', None)
    name = dict(session).get('name', None)
    # Loads the Home Page.
    return render_template('index.html', no_search_bar=True, username=email)

@app.get('/course_page')
def load_courses():
    pmessage = request.args.get('pmessage', '')
    allcourse = course_repo.get_all_courses()
    search_query = request.args.get('search_query', '')  # Get the search query from the request
    if search_query:
        # Filter courses based on the search query
        searchlower = search_query.lower()
        filtered_courses = course_repo.get_courses_by_name(searchlower)
        return render_template('course_page.html', allcourse=filtered_courses, search_query=search_query)
    else:
        return render_template('course_page.html', allcourse=allcourse, pmessage=pmessage)


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
    

@app.post('/courses/new')
def add_course():
    name = request.form['course_name']
    course = ""
    description = request.form['description']
    course_id = request.form['course_num']
    namelower = name.lower()
    existing_course = course_repo.duplicate_course(name)
    if existing_course:
        flash("Class already exists!")
        existing = course_repo.get_course_by_name(name)
        print(existing)
        get_id = existing['course_id']
        return redirect(url_for('course_page', course_id=get_id))
    else:
        course_repo.add_course(course_id, name, course, description)
        return redirect(url_for('course_page', course_id=course_id))

@app.route('/create_course')
def create_course():
    pmessage="You do not have the required permissions to add a new course!"
    email = dict(session).get('email', None)
    if email != None:
        if email.endswith("@uncc.edu") or email.endswith("@charlotte.edu"):
            return render_template('create_course.html')
        else:
            return redirect(url_for('load_courses', pmessage=pmessage))
    return redirect(url_for('load_courses', pmessage=pmessage))

@app.get('/courses/<string:course_id>')
def course_page(course_id):
    user_id = session.get('user_id', None)
    email = dict(session).get('email', None)
    google_id = dict(session).get('id', None)
    name = dict(session).get('name', None)
    course = course_repo.get_course_by_id(course_id)
    course_comments = course_repo.get_all_comments_with_course_id(course_id)
    rating = 0 
    for comment in course_comments:
        rating += comment['rating']
    if (len(course_comments) == 0):
        rating = "No Ratings"
    else:
        rating = round(rating / len(course_comments), 2)
    if email in admin:
        course = course_repo.get_course_by_id(course_id)
        course_comments = course_repo.get_all_comments_with_course_id(course_id)
        return render_template('course_details.html', course=course, course_comments=course_comments, rating=rating, user_id=user_id, showactions=True)
    if email != None:
        course = course_repo.get_course_by_id(course_id)
        course_comments = course_repo.get_all_comments_with_course_id(course_id)
        return render_template('course_details.html', course=course, course_comments=course_comments, rating=rating, user_id=user_id, showactions=False)
    else:
        course = course_repo.get_course_by_id(course_id)
        course_comments = course_repo.get_all_comments_with_course_id(course_id)
        return render_template('course_details.html', course=course, course_comments=course_comments, rating=rating, user_id=user_id, showactions=False)
    return render_template('course_details.html', course=course, course_comments=course_comments, user_id=user_id, showactions=False)


@app.post('/courses/<string:course_id>/addComment')
def add_comment(course_id):
    user_id = session['user_id'] # need to change this value for fully functioning code when user sessions are created.
    rating = request.form.get('rating')
    final_grade = request.form.get('final_grade')
    comment = request.form.get('comment')
    professor_name = request.form.get('professor_name')
    result = course_repo.add_comment_to_course(course_id, user_id, rating, final_grade, comment, professor_name)
    return redirect(f'/courses/{course_id}')

@app.post('/courses/<string:course_id>/editComment')
def edit_comment(course_id):
    rating = request.form.get('rating')
    final_grade = request.form.get('final_grade')
    comment = request.form.get('comment')
    review_id = request.form.get('review_id')
    professor_name = request.form.get('professor_name')
    print(professor_name)
    result = course_repo.edit_comment_from_course(course_id, review_id, rating, final_grade, comment, professor_name)
    return redirect(f'/courses/{course_id}')

@app.post('/courses/<string:course_id>/deleteComment')
def delete_comment(course_id):
    review_id = request.form.get('review_id')
    user_id = request.form.get('user_id')
    result = course_repo.delete_comment_from_course(course_id, user_id, review_id)
    return redirect(f'/courses/{course_id}')


@app.get('/courses/<string:course_id>/edit')
def load_edit_course(course_id):
    course = course_repo.get_course_by_id(course_id)
    return render_template('course_edit_page.html', course=course)

@app.post('/courses/<string:course_id>/edit_course')
def edit_course(course_id):
    professor_name = request.form.get('instructor')
    course_name = request.form.get('course_name')
    course_description = request.form.get('description')
    
    course_repo.edit_course_page(professor_name, course_name, course_description, course_id)

    return redirect(f'/courses/{course_id}')


# edit




@app.post('/courses/<string:course_id>/delete')
def delete_course(course_id):
    try:
        # Attempt to delete the course and its reviews
        course, reviews = course_repo.delete_course_from_courses(course_id)
        if course:
            message = f"Course and all associated reviews deleted successfully. {len(reviews)} reviews removed."
        else:
            message = "No such course found."
    except Exception as e:
        message = f"Error during deletion: {str(e)}"

    return redirect(url_for('load_courses', message=message))







@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')


if __name__ == '__main__':
    app.run(debug=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = request.args.get('message', '')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        success, user_id, user_name, message = course_repo.login_user(username, password)
        if success:
            session['user_id'] = user_id
            session['name'] = user_name  # Store username in session
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login', submitted=True, message="Incorrect Password or Email"))

    return render_template('login.html', message=message)

@app.route('/Ologin', methods=['GET', 'POST'])
def Ologin():
    google = oauth.create_client('google')
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()
    email = user_info['email']
    userid = user_info['id']
    username = user_info['name']
    googlepass = "Oauth"

    session['email'] = email
    session['name'] = username
    user = course_repo.signup_user(username, email, googlepass, is_oauth=True)

    if user:
        success, user_id, user, logged_in_user = course_repo.login_user(email, googlepass, is_oauth=True)
        print(logged_in_user)
        print(user_id)
        if logged_in_user:
            session['user_id'] = user_id
            if isverified(email) == True:
                session['verified'] = True
        else:
            session['user_id'] = None
    else:
        session['user_id'] = None

    return redirect('/')
    
    return redirect('/')


def isverified(email):
    if email.endswith("@uncc.edu") or email.endswith("@charlotte.edu"):
        verified = True
    else:
        verified = False
    return verified


@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    flash('You have been logged out.')
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    message = request.args.get('message', '')
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        #validate = is_valid(email)  #added email validation on signup, it uses a free api that only has 100 requests a month

        if not all([username, email, password, confirm_password]):
            flash('Please fill out all fields.')
            return redirect(url_for('signup', submitted=True, message="Please fill out all fields"))
        if password != confirm_password:
            return redirect(url_for('signup', submitted=True, message="Password does not match!"))
        #if validate == False:
        #    return redirect(url_for('signup', submitted=True, message="Please use a valid email address!"))
        success, message = course_repo.signup_user(username, email, password)
        if not success:
            return redirect(url_for('signup', submitted=True, message="User already exists!"))
        else:
            flash(message)
            return redirect(url_for('login'))

    return render_template('signup.html')
