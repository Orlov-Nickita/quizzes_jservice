from flask import Response, request, jsonify, Flask
from flask_sqlalchemy import SQLAlchemy
from loader import DEBUG, DB_USER, DB_PASSWORD, DB_HOST, DB_NAME
from reqs import get_request_for_questions

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Question(db.Model):
    question_id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    text = db.Column(db.Text)
    answer = db.Column(db.Text)
    difficulty = db.Column(db.Integer, default=0)
    created_at = db.Column(db.TIMESTAMP)


@app.route('/questions/', methods=['POST'])
def add_questions_in_bd_post_request() -> tuple[Response, Response.status_code]:
    a = request.get_json()
    # {'questions_num': 'int'}
    questions_num = a.get('questions_num', 'пусто')
    if questions_num == 'пусто' or not isinstance(questions_num, int):
        return jsonify(questions_num='Should be integer'), 400

    count = 0
    last_ques = ''
    while count < questions_num:
        questions = get_request_for_questions(questions_num)
        for item in questions:
            try:
                q = Question(**item)
                db.session.add(q)
                db.session.commit()
            except:
                continue
            else:
                count += 1
                last_ques = item.get('text')

    return jsonify(last_saved_question=last_ques), 200


if __name__ == '__main__':
    app.run(debug=DEBUG, host='0.0.0.0')
