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
        database_path = "postgresql://suprememajor:12345678@localhost:5432/trivia_2"
        self.app = create_app()
        self.client = self.app.test_client
        self.app.config["SQLALCHEMY_DATABASE_URI"] = database_path
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        self.new_question = {"question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
                             "answer": "Maya Angelou", "category": 2, "difficulty": 3}

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

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_paginated_books(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["current_category"], "All")
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))
        self.assertTrue(len(data["categories"]))

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get("/questions?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    # def test_update_book_rating(self):
    #     res = self.client().patch("/books/5", json={"rating": 1})
    #     data = json.loads(res.data)
    #     book = Book.query.filter(Book.id == 5).one_or_none()
    #
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertEqual(book.format()["rating"], 1)
    #
    # def test_400_for_failed_update(self):
    #     res = self.client().patch("/books/5")
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 400)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "bad request")
    #
    # def test_create_new_book(self):
    #     res = self.client().post("/books", json=self.new_book)
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["created"])
    #     self.assertTrue(len(data["books"]))
    #
    # def test_405_if_book_creation_not_allowed(self):
    #     res = self.client().post("/books/45", json=self.new_book)
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 405)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "method not allowed")
    #
    # # Delete a different book in each attempt
    # def test_delete_book(self):
    #     id = 13
    #     res = self.client().delete(f"/books/{id}")
    #     data = json.loads(res.data)
    #
    #     book = Book.query.filter(Book.id == id).one_or_none()
    #
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertEqual(data["deleted"], id)
    #     self.assertTrue(data["total_books"])
    #     self.assertTrue(len(data["books"]))
    #     self.assertEqual(book, None)
    #
    # def test_422_if_book_does_not_exist(self):
    #     res = self.client().delete("/books/1000")
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "unprocessable")
    #
    # def test_get_book_search_with_results(self):
    #     res = self.client().post("/books", json={"search": "Novel"})
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["total_books"])
    #     self.assertEqual(len(data["books"]), 2)
    #
    # def test_get_book_search_without_results(self):
    #     res = self.client().post("/books", json={"search": "applejacks"})
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertEqual(data["total_books"], 0)
    #     self.assertEqual(len(data["books"]), 0)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()