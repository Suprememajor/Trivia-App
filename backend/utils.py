from models import Category, db, Question

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [questions.format() for questions in selection]
    current_questions = questions[start:end]

    return current_questions


def populate_database():
    """
    Populates database on first run
    """
    categories = [
        Category("Science"),
        Category("Art"),
        Category("Geography"),
        Category("History"),
        Category("Entertainment"),
        Category("Sports"),
        Category("Misc")
    ]
    questions = [
        Question(category_id=5, difficulty=4, answer="Tom Cruise",
                 question="What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"),
        Question(category_id=5, difficulty=4, answer="Apollo 13",
                 question="What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"),
        Question(category_id=4, difficulty=1, answer="Muhammad Ali",
                 question="What boxer's original name is Cassius Clay?"),
        Question(category_id=4, difficulty=2, answer="Maya Angelou",
                 question="Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"),
        Question(category_id=4, difficulty=4, answer="Scarab",
                 question="Which dung beetle was worshipped by the ancient Egyptians?"),
        Question(category_id=1, difficulty=4, answer="Blood",
                 question="Hematology is a branch of medicine involving the study of what?"),
        Question(category_id=1, difficulty=3, answer="Alexander Fleming", question="Who discovered penicillin?"),
        Question(category_id=1, difficulty=4, answer="Liver", question="What is the heaviest organ in the human body?"),
        Question(category_id=2, difficulty=2, answer="Jackson Pollock",
                 question="Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"),
        Question(category_id=2, difficulty=4, answer="One",
                 question="How many paintings did Van Gogh sell in his lifetime?"),
        Question(category_id=2, difficulty=3, answer="Mona Lisa", question="La Giaconda is better known as what?"),
        Question(category_id=2, difficulty=1, answer="Escher",
                 question="Which Dutch graphic artist–initials M C was a creator of optical illusions?"),
        Question(category_id=3, difficulty=2, answer="Agra", question="The Taj Mahal is located in which Indian city?"),
        Question(category_id=3, difficulty=3, answer="The Palace of Versailles",
                 question="In which royal palace would you find the Hall of Mirrors?"),
        Question(category_id=3, difficulty=2, answer="Lake Victoria", question="What is the largest lake in Africa?"),
        Question(category_id=4, difficulty=2, answer="George Washington Carver",
                 question="Who invented Peanut Butter?"),
        Question(category_id=6, difficulty=4, answer="Uruguay",
                 question="Which country won the first ever soccer World Cup in 1930?"),
        Question(category_id=6, difficulty=3, answer="Brazil",
                 question="Which is the only team to play in every soccer World Cup tournament?"),
        Question(category_id=5, difficulty=3, answer="Edward Scissorhands",
                 question="What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?")
    ]
    try:
        db.session.bulk_save_objects(categories)
        db.session.bulk_save_objects(questions)
        db.session.commit()
    except Exception as exception:
        print(exception)
        db.session.rollback()
    finally:
        db.close()
