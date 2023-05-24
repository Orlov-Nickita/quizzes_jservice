import json
import datetime
import requests


def get_request_for_questions(count: int) -> list[dict]:
    """
    Отправляет GET запрос на API по генерации случайных вопросов с ответами для викторины
    :param count: количество вопросов, которые нужно запросить
    :return: список с вопросами
    """
    url = f'https://jservice.io/api/random?count={count}'
    response: list = json.loads(requests.get(url).content.decode())
    questions: list[dict] = [
        {
            "question_id": que.get('id'),
            "text": que.get('question'),
            "answer": que.get('answer'),
            "difficulty": que.get('value'),
            "created_at": datetime.datetime.fromisoformat(que.get('created_at')[:-1]),
        }
        for que in response
    ]
    return questions
