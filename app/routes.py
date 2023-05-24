from flask import Response, request, jsonify, Blueprint
from sqlalchemy.exc import IntegrityError
from reqs import get_request_for_questions
from models import db, Question

questions = Blueprint('questions', 'questions_route')


@questions.route('/questions/', methods=['POST'])
def add_questions_in_bd_post_request() -> tuple[Response, Response.status_code]:
    """
    Получает объект JSON путем POST запроса с количеством вопросов для добавления в базу данных и добавляет их один
    за другим. Если указанное число не является целым числом, оно возвращает сообщение об ошибке.
    :return: Кортеж из последнего добавленного вопроса и код состояния
    """
    a: dict = request.get_json()
    # {'questions_num': 'int'}
    questions_num: int = a.get('questions_num', 'пусто')
    if questions_num == 'пусто' or not isinstance(questions_num, int):
        return jsonify(questions_num='Should be integer'), 400

    count = 0
    last_ques = ''
    while count < questions_num:
        questions: list = get_request_for_questions(questions_num)
        for item in questions:
            try:
                q = Question(**item)
                db.session.add(q)
                db.session.commit()
            except IntegrityError:
                continue
            else:
                count += 1
                last_ques = item.get('text')
    return jsonify(last_saved_question=last_ques), 200
