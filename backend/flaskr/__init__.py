from flask import Flask, abort, jsonify, request
from flask_cors import CORS
from models import Category
from models import setup_db, Question

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [questions.format() for questions in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    """
    Category

    """

    @app.route("/categories", methods=["POST"])
    def create_category():
        body = request.get_json()
        name = body.get("name", None)
        if not name:
            abort(400)
        name = name.title()
        if Category.query.filter_by(name=name).one_or_none():
            abort(409)
        category = Category(name=name)
        try:
            category.insert()

            return jsonify(
                {
                    "success": True,
                    "created": category.id
                }
            )

        except:
            abort(422)

    @app.route("/categories")
    def retrieve_categories():
        categories = Category.query.order_by(Category.name).all()
        if len(categories) == 0:
            abort(404)
        categories = {cat.id: cat.name for cat in categories}
        return jsonify({
            "success": True,
            "categories": categories
        })

    @app.route("/categories/<int:category_id>/questions")
    def retrieve_category_questions(category_id):
        category = Category.query.filter_by(id=category_id).one_or_none()
        if not category:
            abort(404)
        selection = Question.query.filter_by(category_id=category_id).all()
        current_questions = paginate_questions(request, selection)
        if len(current_questions) == 0:
            abort(404)
        return jsonify({
            "success": True,
            "questions": current_questions,
            "totalQuestions": len(selection),
            "currentCategory": category.name
        })

    """
    Question

    """

    @app.route("/questions", methods=["POST"])
    def create_question():
        body = request.get_json()
        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_category = body.get("category", None)
        new_difficulty = body.get("difficulty", None)
        search_term = body.get("searchTerm", None)
        cur_cat_id = request.args.get("category", None, type=int)
        if cur_cat_id:
            current_category = Category.query.get(cur_cat_id).one_or_none()
            if current_category is None:
                abort(404)
        else:
            current_category = Category(name="All")

        if search_term:
            selection = Question.query.filter(Question.question.ilike(f"%{search_term}%")).all()
            if len(selection) == 0:
                abort(404)
            current_questions = paginate_questions(request, selection)
            return jsonify({
                "success": True,
                "questions": current_questions,
                "totalQuestions": len(selection),
                "currentCategory": current_category.name
            })
        elif new_question and new_answer and new_category and new_difficulty:
            try:
                question = Question(question=new_question, answer=new_answer, category_id=new_category,
                                    difficulty=new_difficulty)
                question.insert()
                return jsonify({"success": True})
            except:
                abort(422)
        else:
            abort(400)

    @app.route("/quizzes", methods=["POST"])
    def get_quiz():
        body = request.get_json()
        previous_questions = body["previous_questions"]
        cat_id = int(body["quiz_category"]["id"])
        quiz_category = cat_id if cat_id > 0 else None
        question = None
        try:
            if previous_questions and quiz_category:
                question = Question.query.filter(Question.category_id == quiz_category) \
                    .filter(Question.id.not_in(previous_questions)).first()
            elif quiz_category:
                question = Question.query.filter(Question.category_id == quiz_category).first()
            elif previous_questions:
                question = Question.query.filter(Question.id.not_in(previous_questions)).first()
            else:
                question = Question.query.first()
        except Exception as e:
            abort(422)

        if question is None:
            abort(404)
        return jsonify({
            "success": True,
            "question": question.format()
        })

    @app.route("/questions")
    def retrieve_questions():
        cur_cat_id = request.args.get("category", None, type=int)
        if cur_cat_id:
            current_category = Category.query.filter(Category.id == cur_cat_id).one_or_none()
            if current_category is None:
                abort(404)
        else:
            current_category = Category(name="All")
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)
        if len(current_questions) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "currentCategory": current_category.name,
                "categories": {cat.id: cat.name for cat in Category.query.all()},
                "questions": current_questions,
                "totalQuestions": len(selection)
            }
        )

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()
            if question is None:
                abort(404)

            question.delete()

            return jsonify(
                {
                    "success": True,
                    "deleted": question_id
                }
            )

        except:
            abort(422)

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({"success": False, "error": 400, "message": "bad request"}),
            400,
        )

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(405)
    def method_not_allowed(error):
        return (
            jsonify({"success": False, "error": 405, "message": "method not allowed"}),
            405
        )

    @app.errorhandler(409)
    def conflict(error):
        return (
            jsonify({"success": False, "error": 409, "message": "resource exists"}),
            409
        )

    return app
