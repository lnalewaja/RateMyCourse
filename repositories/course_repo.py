from repositories.db import get_pool
from psycopg.rows import dict_row

def get_all_courses():
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute('''
                SELECT
            ''')
            return cur.fetchall()
