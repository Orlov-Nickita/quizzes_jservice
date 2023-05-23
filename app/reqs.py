import requests


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
