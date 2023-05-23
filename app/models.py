import psycopg2
import requests
from loader import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST


def get_request_for_questions(count: int) -> list[dict]:
    url = f'https://jservice.io/api/random?count={count}'
    response: list | dict = requests.get(url).json()
    questions: list[dict] = [
        {
            "question_id": que.get('id'),
            "text": que.get('question'),
            "answer": que.get('answer'),
            "difficulty": que.get('value'),
            "created_at": que.get('created_at'),
        }
        for que in response
    ]
    return questions


def add_questions_to_db(q_num: int) -> str:
    count = 0
    while count < q_num:
        questions = get_request_for_questions(q_num)
        with psycopg2.connect(host=DB_HOST,
                              database=DB_NAME,
                              user=DB_USER,
                              password=DB_PASSWORD) as connect:
            cursor: psycopg2.cursor = connect.cursor()
            for item in questions:
                try:
                    cursor.execute("""
                    INSERT INTO questions (question_id, text, answer, difficulty, created_at)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                                   (*item.values(),))
                    connect.commit()

                except psycopg2.IntegrityError:
                    continue
                else:
                    count += 1
                    result = item.get('text')
    return result
