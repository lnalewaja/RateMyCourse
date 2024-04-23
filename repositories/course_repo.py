from repositories.db import get_pool
from psycopg.rows import dict_row

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
                    r.user_id,
                    u.username
                FROM reviews r
                JOIN courses c ON r.course_id = c.course_id
                JOIN users u ON r.user_id = u.user_id
                WHERE r.course_id = %s;
            ''', [course_id])
            return cur.fetchall()

def add_comment_to_course(course_id: str, user_id: str, rating: int, final_grade: str, comment: str):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                INSERT INTO reviews (course_id, user_id, comment, rating, final_grade)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING *;
            ''', [course_id, user_id, comment, rating, final_grade])
            return cur.fetchone()

def edit_comment_from_course(course_id: str, review_id: str, rating: int, final_grade: str, comment: str):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                UPDATE reviews
                SET comment = %s, rating = %s, final_grade = %s
                WHERE course_id = %s AND review_id = %s
                RETURNING *;
            ''', [comment, rating, final_grade, course_id, review_id])
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