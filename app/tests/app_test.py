import json
import os
from unittest import TestCase
from app import create_app
from models import Question, db


class TestFlaskApp(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.app = create_app('config.TestConfig')

    def setUp(self):
        self.client = self.app.test_client()
        print('test', self.app.config.get('TESTING'))
        self.base_url = '/questions/'
        with self.app.app_context():
            db.create_all()

    def test_can_post_request_with_correct_data(self):
        response = self.client.post(self.base_url, data=json.dumps({'questions_num': 4}),
                                    headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('last_saved_question' in response.data.decode())

    def test_data_added_to_test_database(self):
        count = 4
        self.client.post(self.base_url, data=json.dumps({'questions_num': count}),
                         headers={'Content-Type': 'application/json'})
        with self.app.app_context():
            self.assertEqual(count, len(db.session.query(Question).all()))

    def test_cannot_post_request_with_incorrect_data(self):
        response = self.client.post(self.base_url, data=json.dumps({'questions_num': '4'}),
                                    headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual({"questions_num": "Should be integer"}, json.loads(response.data.decode()))

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    @classmethod
    def tearDownClass(cls) -> None:
        path_test_db: str = cls.app.config.get('SQLALCHEMY_DATABASE_URI').replace('sqlite:////', '')
        os.remove(path_test_db)
