import json
import unittest

from flask_sqlalchemy import SQLAlchemy

from config import DIALECT, USER, PASSWORD, HOST, PORT
from flaskr import create_app
from models import Question, Category

DATABASE_NAME = "trivia_test"
DATABASE_PATH = f'{DIALECT}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}'

class CategoryModelTestCase(unittest.TestCase):
    """This class represents the Category model test case"""

    def setUp(self):
        """Define test variables and initialize app."""

        self.app = create_app()
        self.client = self.app.test_client
        self.app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_PATH
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        self.new_category = {"name": "Tricky"}
        self.new_category2 = {"name": "history"}
        self.new_category3 = {"body": "miSc"}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.app = self.app
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    ###################################################################################################################
    # Tests for create_category
    ###################################################################################################################

    def test_create_new_category(self):
        res = self.client().post("/categories", json=self.new_category)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])

    def test_400_create_category_failed(self):
        res = self.client().post("/categories", json=self.new_category3)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")

    def test_409_duplicate_category(self):
        res = self.client().post("/categories", json=self.new_category2)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 409)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource exists")

    ###################################################################################################################
    # Tests for retrieve_categories
    ###################################################################################################################

    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["categories"]))

    ###################################################################################################################
    # Tests for retrieve_category_questions
    ###################################################################################################################

    def test_get_cat_questions(self):
        category_id = 2
        category = Category.query.get(category_id)
        res = self.client().get(f"/categories/{category_id}/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["currentCategory"], category.name)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["totalQuestions"])

    def test_404_category_not_found(self):
        category_id = 100
        res = self.client().get(f"/categories/{category_id}/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_404_empty_category(self):
        category_id = 7
        res = self.client().get(f"/categories/{category_id}/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")


class QuestionModelTestCase(unittest.TestCase):
    """This class represents the Question model test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_PATH
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        self.new_question = {"question": "What is the name of the artist who painted ‘Mona Lisa’?",
                             "answer": "Leonardo Da Vinci", "category": 2, "difficulty": 2}
        self.new_question2 = {"question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
                              "answer": "Maya Angelou", "difficulty": 3}
        self.new_question3 = {"question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
                              "answer": "Maya Angelou", "difficulty": 3, "searchTerm": "xpres"}
        self.new_question4 = {"question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
                              "answer": "Maya Angelou", "difficulty": 3, "searchTerm": "Nirtumizac"}
        self.quiz1 = {"previous_questions": [5, 9, 23], "quiz_category": {"id": 4, "name": "History"}}
        self.quiz2 = {"quiz_category": {"id": 5, "name": "Entertainment"}}
        self.quiz3 = {"previous_questions": [12, 13, 14], "quiz_category": {"id": 5, "name": "Entertainment"}}
        self.quiz4 = {"quiz_category": {"id": 90, "name": "Unknown"}}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.app = self.app
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    ###################################################################################################################
    # Tests for create_question
    ###################################################################################################################

    def test_create_new_question(self):
        res = self.client().post(f"/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_400_create_question_failed(self):
        res = self.client().post("/questions", json=self.new_question2)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")

    ###################################################################################################################
    # Tests for search_question
    ###################################################################################################################
    def test_search_question(self):
        res = self.client().post(f"/questions", json=self.new_question3)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["totalQuestions"])
        self.assertEqual(data["currentCategory"], "All")
        self.assertTrue(len(data["questions"]))

    def test_404_search_question_failed(self):
        res = self.client().post("/questions", json=self.new_question4)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    ###################################################################################################################
    # Tests for get_quiz
    ###################################################################################################################
    def test_get_quiz_all_data(self):
        res = self.client().post("/quizzes", json=self.quiz1)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["question"]["category_id"], self.quiz1["quiz_category"]["id"])
        self.assertEqual(data["question"]["id"], 12)
        self.assertTrue(data["question"])

    def test_get_quiz_category(self):
        res = self.client().post("/quizzes", json=self.quiz2)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["question"]["category_id"], self.quiz2["quiz_category"]["id"])
        self.assertTrue(data["question"])

    def test_get_quiz_except_list(self):
        res = self.client().post("/quizzes", json=self.quiz3)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])

    def test_422_get_quiz_failed(self):
        res = self.client().post("/quizzes", json=self.quiz4)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    ###################################################################################################################
    # Tests for retrieve_questions
    ###################################################################################################################

    def test_get_paginated_questions(self):
        page = 1
        res = self.client().get(f"/questions?page={page}")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["currentCategory"], "All")
        self.assertTrue(data["totalQuestions"])
        self.assertTrue(len(data["categories"]))
        self.assertTrue(len(data["questions"]))

    def test_get_paginated_questions_with_cat(self):
        category_id = 4
        category = Category.query.get(category_id)
        res = self.client().get(f"/questions?category={category_id}")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["currentCategory"], category.name)
        self.assertTrue(data["totalQuestions"])
        self.assertTrue(len(data["categories"]))
        self.assertTrue(len(data["questions"]))

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get("/questions?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    ###################################################################################################################
    # Tests for delete_question
    ###################################################################################################################
    # Delete a different question in each attempt
    def test_delete_question(self):
        id = 21
        res = self.client().delete(f"/questions/{id}")
        data = json.loads(res.data)
        question = Question.query.filter(Question.id == id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], id)
        self.assertEqual(question, None)

    def test_422_if_question_does_not_exist(self):
        res = self.client().delete("/questions/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
