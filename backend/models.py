from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer

db = SQLAlchemy()

"""
setup_db(app)
    
"""


def setup_db(app):
    app.config.from_object('config')
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)


"""
Category

"""


class Category(db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    questions = db.relationship('Question', backref='category', lazy=True)

    def __init__(self, name):
        self.name = name

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        for question in self.questions:
            db.session.delete(question)
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name
        }


"""
Question

"""


class Question(db.Model):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    difficulty = Column(Integer, nullable=False)
    category_id = Column(Integer, db.ForeignKey('categories.id'), nullable=False)
    ratings = db.relationship('Rating', backref='question', lazy=True)

    def __init__(self, question, answer, category_id, difficulty):
        self.question = question
        self.answer = answer
        self.category_id = category_id
        self.difficulty = difficulty

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        for rating in self.ratings:
            rating.delete()
        db.session.delete(self)
        db.session.commit()

    def format(self):
        rating_values = [rating.value for rating in self.ratings]
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category_id': self.category_id,
            'difficulty': self.difficulty,
            'rating': sum(rating_values) / len(rating_values)
        }


"""
Rating

"""


class Rating(db.Model):
    __tablename__ = 'ratings'

    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, db.ForeignKey('questions.id'), nullable=False)
    user_id = Column(Integer, db.ForeignKey('users.id'), nullable=False)
    value = Column(Integer, nullable=False)

    def __init__(self, question_id, user_id, value):
        self.question_id = question_id
        self.user_id = user_id
        self.value = value

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'question_id': self.question_id,
            'user_id': self.user_id,
            'value': self.value
        }


"""
User

"""


class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    score = Column(Integer, nullable=False)

    def __init__(self, username, email, password):
        self.score = 0
        self.username = username
        self.email = email
        self.password = password

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'score': self.score
        }
