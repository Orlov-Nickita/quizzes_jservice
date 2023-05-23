import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()


def init_db():
    with psycopg2.connect(host=os.getenv('DB_HOST'),
                          database=os.getenv('DB_NAME'),
                          user=os.getenv('DB_USER'),
                          password=os.getenv('DB_PASSWORD')) as connect:
        cursor: psycopg2.cursor = connect.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS questions (
                question_id INTEGER PRIMARY KEY,
                text TEXT,
                answer TEXT,
                difficulty INTEGER default 0,
                created_at TIMESTAMP
            ) 
            """
        )
        connect.commit()


if __name__ == '__main__':
    init_db()
