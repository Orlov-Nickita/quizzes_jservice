from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Question(db.Model):
    """
    Класс модели Question, на основе которого создается таблица в БД и в последующем происходит взаимодействие с БД
    """
    question_id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    text = db.Column(db.Text)
    answer = db.Column(db.Text)
    difficulty = db.Column(db.Integer, default=0)
    created_at = db.Column(db.TIMESTAMP)
