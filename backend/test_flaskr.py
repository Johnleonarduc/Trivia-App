import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres', '7856Julcd07', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question ={'question':'Which country has green and white flag color', 'answer': 'Nigeria', 'difficulty': 3, 'category': 5}
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])

    def test_404_requesting_particular_category(self):
        res = self.client().get("/categories/1")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
        
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        all_questions = Question.query.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'], len(all_questions))
        self.assertTrue(data['categories'])
        self.assertTrue(data['current_category'])

    def test_404_category_not_found(self):
        # res = self.client().get('/questions?page=1000')
        res = self.client().get('/questions?page=1&category=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_400_bad_page_request(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")


    # def test_delete_question(self):
    #     res = self.client().delete('/questions/22')
    #     data  = json.loads(res.data)

    #     question = Question.query.filter(Question.id == 22).one_or_none()

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['status'], 200)
    #     self.assertEqual(question, None)
    #     self.assertTrue(data['id'])

    def test_404_question_does_not_exist(self):
        res = self.client().delete('/questions/22')
        data  = json.loads(res.data)

        question = Question.query.filter(Question.id == 22).one_or_none()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(question, None)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_post_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)



    def test_search_questions(self):
        res = self.client().post('/questions', json={'searchTerm': 'cup'})
        data = json.loads(res.data)
        
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])
    
    def test_422_if_post_question_args_incomplete(self):
        res = self.client().post('/questions', json={'question':'Which country has green and white flag color', 'answer': '', 'difficulty': 3, 'category': 5})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_422_if_search_unprocessable(self):
        res = self.client().post('/questions', json={'searchTerm': 'buhari'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_400_if_both_search_and_question_args_absent(self):
        res = self.client().post('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")


    def test_get_questions_in_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])


    def test_400_if_wrong_category(self):
        res = self.client().get('/categories/22/questions')
        data  = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")

    def test_get_quiz_question_all_categories_no_previous_questions(self):
        res = self.client().post('/quizzes', json={'previous_questions': [], 'quiz_category': {'type': "click", 'id': 0}})
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_get_quiz_question_all_categories_with_previous_questions(self):
        res = self.client().post('/quizzes', json={'previous_questions': [21], 'quiz_category': {'type': "click", 'id': 0}})
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertNotEqual(data['question']['id'], 21)

    def test_get_quiz_question_single_category_no_previous_questions(self):
        res = self.client().post('/quizzes', json={'previous_questions': [], 'quiz_category': {'type': "Science", 'id': 1}})
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(data['question']['category'], 1)
        self.assertTrue(data['question'])

    def test_get_quiz_question_single_category_with_previous_questions(self):
        res = self.client().post('/quizzes', json={'previous_questions': [19], 'quiz_category': {'type': "Art", 'id': 2}})
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(data['question']['category'], 2)
        self.assertNotEqual(data['question']['id'], 19)

    def test_400_if_incomplete_or_incorrect_or_wrong_parameters_for_quiz(self):
        res = self.client().post('/quizzes', json={'previous_questions': [200], 'quiz_category': {'type': "Games", 'id': 2}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()