import json
import unittest

from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app


class CategoryModelTestCase(unittest.TestCase):
    """This class represents the Category model test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        database_path = "postgresql://suprememajor:12345678@localhost:5432/trivia_4"
        self.app = create_app()
        self.client = self.app.test_client
        self.app.config["SQLALCHEMY_DATABASE_URI"] = database_path
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        self.new_category = {"name": "new category"}
        self.new_category2 = {"name": "miSc"}
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
#
#     def test_create_new_category(self):
#
#         res = self.client().post("/categories", json=self.new_category)
#         data = json.loads(res.data)
#
#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(data["success"], True)
#         self.assertTrue(data["created"])
#         self.assertTrue(len(data["categories"]))
#
#     def test_400_create_category_failed(self):
#
#         res = self.client().post("/categories", json=self.new_category3)
#         data = json.loads(res.data)
#
#         self.assertEqual(res.status_code, 400)
#         self.assertEqual(data["success"], False)
#         self.assertEqual(data["message"], "bad request")
#
#     def test_409_create_category_failed(self):
#
#         res = self.client().post("/categories", json=self.new_category2)
#         data = json.loads(res.data)
#
#         self.assertEqual(res.status_code, 409)
#         self.assertEqual(data["success"], False)
#         self.assertEqual(data["message"], "resource exists")

    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["categories"]))
#     #
#     # def test_delete_category(self):
#     #     category_id = 6
#     #     res = self.client().delete(f"/categories/{category_id}")
#     #     data = json.loads(res.data)
#     #     category = Category.query.filter(Category.id == category_id).one_or_none()
#     #     questions = Question.query.filter(Question.category_id == category_id).all()
#     #
#     #     self.assertEqual(res.status_code, 200)
#     #     self.assertEqual(data["success"], True)
#     #     self.assertEqual(data["deleted"], category_id)
#     #     self.assertTrue(len(data["categories"]))
#     #     self.assertEqual(category, None)
#     #     self.assertEqual(len(questions), 0)
#     #
#     # def test_422_if_category_does_not_exist(self):
#     #
#     #     res = self.client().delete("/categories/1000")
#     #     data = json.loads(res.data)
#     #
#     #     self.assertEqual(res.status_code, 422)
#     #     self.assertEqual(data["success"], False)
#     #     self.assertEqual(data["message"], "unprocessable"


class QuestionModelTestCase(unittest.TestCase):
    """This class represents the Question model test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        database_path = "postgresql://suprememajor:12345678@localhost:5432/trivia_4"
        self.app = create_app()
        self.client = self.app.test_client
        self.app.config["SQLALCHEMY_DATABASE_URI"] = database_path
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        self.new_question = {"question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
                             "answer": "Maya Angelou", "category": 4, "difficulty": 3}
        self.new_question2 = {"question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
                             "answer": "Maya Angelou", "difficulty": 3}

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

    # def test_create_new_question(self):
    #     res = self.client().post(f"/questions?category={self.new_question['category']}", json=self.new_question)
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertEqual(data["current_category"]["id"], self.new_question["category"])
    #     self.assertTrue(data["created"])
    #     self.assertTrue(data["total_questions"])
    #     self.assertTrue(len(data["categories"]))
    #     self.assertTrue(len(data["questions"]))
    #
    # def test_400_create_question_failed(self):
    #
    #     res = self.client().post("/questions", json=self.new_question2)
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 400)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "bad request")

    # def test_get_paginated_questions(self):
    #     res = self.client().get(f"/questions")
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["total_questions"])
    #     self.assertTrue(len(data["categories"]))
    #     self.assertTrue(len(data["questions"]))
    #
    # def test_get_paginated_questions_with_cat(self):
    #     category = 4
    #     res = self.client().get(f"/questions?category={category}")
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertEqual(data["current_category"]["id"], category)
    #     self.assertTrue(data["total_questions"])
    #     self.assertTrue(len(data["categories"]))
    #     self.assertTrue(len(data["questions"]))
    #
    # def test_404_sent_requesting_beyond_valid_page(self):
    #     res = self.client().get("/questions?page=1000")
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "resource not found")

    # Delete a different question in each attempt
    # def test_delete_question(self):
    #     id = 9
    #     res = self.client().delete(f"/questions/{id}")
    #     data = json.loads(res.data)
    #     question = Question.query.filter(Question.id == id).one_or_none()
    #
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertEqual(data["deleted"], id)
    #     self.assertTrue(data["total_questions"])
    #     self.assertTrue(len(data["questions"]))
    #     self.assertEqual(question, None)
    #
    # def test_422_if_question_does_not_exist(self):
    #     res = self.client().delete("/questions/1000")
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "unprocessable")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
