from flask import Response, request, jsonify, Flask
from loader import DEBUG
from models import add_questions_to_db

app = Flask(__name__)


@app.route('/questions/', methods=['POST'])
def add_questions_in_bd_post_request() -> tuple[Response, Response.status_code]:
    a = request.get_json()
    # {'questions_num': 'int'}
    questions_num = a.get('questions_num', 'пусто')
    if questions_num == 'пусто' or not isinstance(questions_num, int):
        return jsonify(questions_num='Should be integer'), 400

    last_ques = add_questions_to_db(q_num=questions_num)
    return jsonify(last_saved_question=last_ques), 200


if __name__ == '__main__':
    app.run(debug=DEBUG, host='0.0.0.0')
