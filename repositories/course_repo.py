from repositories.db import get_pool
from psycopg.rows import dict_row
from werkzeug.security import generate_password_hash, check_password_hash

def get_all_courses():
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                SELECT
                    *
                FROM courses;
            ''')
            return cur.fetchall()
        
def get_courses_by_name(name):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(''' SELECT * FROM courses WHERE LOWER(course_name) LIKE LOWER(%s); ''', [f"%{name}%"])
            return cur.fetchall()
        
def duplicate_course(name):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                SELECT course_name
                FROM courses 
                WHERE LOWER(course_name) LIKE LOWER(%s);
            ''', [f"%{name}%"])
            return cur.fetchall()

def get_course_by_id(course_id: str):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                SELECT
                    course_id,
                    course_name,
                    course_description,
                    professor_name
                FROM courses
                WHERE course_id = %s;
            ''', [course_id])
            return cur.fetchone()
        
def get_course_by_name(name: str):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                SELECT
                    course_id,
                    course_name,
                    course_description,
                    professor_name
                FROM courses
                WHERE LOWER(course_name) LIKE LOWER(%s);
            ''', [f"%{name}%"])
            return cur.fetchone()

def get_all_comments_with_course_id(course_id: str):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                SELECT
                    r.review_id,
                    r.comment,
                    r.rating,
                    r.final_grade,
                    r.professor_name,
                    r.user_id,
                    u.username
                FROM reviews r
                JOIN users u ON r.user_id = u.user_id
                WHERE r.course_id = %s;
            ''', [course_id])
            return cur.fetchall()

def add_comment_to_course(course_id: str, user_id: str, rating: int, final_grade: str, comment: str, professor_name: str):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                INSERT INTO reviews (course_id, user_id, comment, rating, final_grade, professor_name)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING *;
            ''', [course_id, user_id, comment, rating, final_grade, professor_name])
            return cur.fetchone()

def edit_comment_from_course(course_id: str, review_id: str, rating: int, final_grade: str, comment: str, professor_name: str):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                UPDATE reviews
                SET comment = %s, rating = %s, final_grade = %s, professor_name = %s
                WHERE course_id = %s AND review_id = %s
                RETURNING *;
            ''', [comment, rating, final_grade, professor_name, course_id, review_id])
            return cur.fetchone()

def delete_comment_from_course(course_id: str, user_id: str, review_id: str):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                DELETE FROM reviews
                WHERE course_id = %s AND user_id = %s AND review_id = %s
                RETURNING *;
            ''', [course_id, user_id, review_id])
            return cur.fetchone()
        


def signup_user(username: str, email: str, password: str, is_oauth: bool = False):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            # Check if the user already exists
            cur.execute('SELECT user_id FROM Users WHERE email = %s', (email,))
            if cur.fetchone():
                return False, 'Username or email already exists.'

            # Insert the new user into the database
            if is_oauth:
                # For OAuth users, store a placeholder password
                password_hash = generate_password_hash("oauth_user")
            else:
                password_hash = generate_password_hash(password)

            cur.execute('INSERT INTO Users (username, email, password, is_oauth) VALUES (%s, %s, %s, %s)',
                        (username, email, password_hash, is_oauth))
            conn.commit()
            return True, 'Registration successful, please login.'
        

def login_user(email: str, password: str, is_oauth: bool = False):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            # Check if the user exists and fetch credentials
            cur.execute('SELECT user_id, username, password, is_oauth FROM Users WHERE email = %s', (email,))
            user_record = cur.fetchone()
            if user_record:
                user_id, username, password_hash, user_is_oauth = user_record
                # Verify the password
                if is_oauth and user_is_oauth:
                    # For OAuth users, skip password verification
                    return True, user_id, username
                elif not is_oauth and check_password_hash(password_hash, password):
                    return True, user_id, username
            return False, None, 'Invalid username or password'
        
def add_course(id: str, course_name: str, instructor: str, description: str):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                INSERT INTO Courses (course_id, course_name, course_description, professor_name)
                VALUES (%s, %s, %s, %s)
                RETURNING *;
            ''', [id, course_name, description, instructor])
            return cur.fetchone()
        

def edit_course_page(professor_name: str, course_name: str, course_description: str, course_id: str):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                UPDATE courses
                SET professor_name = %s, course_name = %s, course_description = %s
                WHERE course_id = %s
                RETURNING *;
            ''', [professor_name, course_name, course_description, course_id])
            return cur.fetchone()


def delete_course_from_courses(course_id: str):
    pool = get_pool()
    with pool.connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute('''
                    DELETE FROM Reviews
                    WHERE course_id = %s
                    RETURNING *;
                ''', (course_id,))
                reviews = cur.fetchall()

                cur.execute('''
                    DELETE FROM Courses
                    WHERE course_id = %s
                    RETURNING *;
                ''', (course_id,))
                course = cur.fetchone()

            conn.commit()
            return course, reviews
        except Exception as e:
            conn.rollback()
            raise e




