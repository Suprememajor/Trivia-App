## Udacity's Limit Breaking Trivia APp

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created the trivia app to play the game.
This project is a trivia app for Udacity employees and students. Players are able to pick a category, answer questions, add new questions as well as delete questions. 

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/). 

## Getting Started

### Pre-requisites and Local Development 
Developers using this project should already have Python3, pip and node installed on their local machines.

#### Backend

From the backend folder run `pip install -r requirements.txt`. All required packages are included in the requirements file. 

To run the application run the following commands: 
```
export FLASK_APP=flaskr
export FLASK_DEBUG=true
flask db upgrade
flask run
```

These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration. 

#### Frontend

From the frontend folder, run the following commands to start the client: 
```
npm install // only once to install dependencies
npm start 
```

By default, the frontend will run on localhost:3000. 

### Tests
In order to run tests navigate to the backend folder and run the following commands: 

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

The first time you run the tests, omit the dropdb command. 

All tests are kept in that file and should be maintained as updates are made to app functionality. 

## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return five error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 405: Method Not Allowed
- 409: Resource Exists
- 422: Not Processable 

### Endpoints 
#### GET /questions
- General:
    - Returns a list of question objects, all categories, success value, total number of questions, and current category.
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 
- Sample: `curl http://127.0.0.1:5000/questions`

``` {
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports",
    "7": "Misc"
  },
  "currentCategory": "All",
  "questions": [
    {
      "answer": "Tom Cruise",
      "category_id": 5,
      "difficulty": 4,
      "id": 1,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Apollo 13",
      "category_id": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Muhammad Ali",
      "category_id": 4,
      "difficulty": 1,
      "id": 3,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Maya Angelou",
      "category_id": 4,
      "difficulty": 2,
      "id": 4,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Scarab",
      "category_id": 4,
      "difficulty": 4,
      "id": 5,
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    },
    {
      "answer": "Blood",
      "category_id": 1,
      "difficulty": 4,
      "id": 6,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "Alexander Fleming",
      "category_id": 1,
      "difficulty": 3,
      "id": 7,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Liver",
      "category_id": 1,
      "difficulty": 4,
      "id": 8,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Jackson Pollock",
      "category_id": 2,
      "difficulty": 2,
      "id": 9,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    },
    {
      "answer": "One",
      "category_id": 2,
      "difficulty": 4,
      "id": 10,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }
  ],
  "success": true,
  "totalQuestions": 19
}

```
#### POST /questions
- General:
    - Creates a new question using the submitted question value, answer, category id and difficulty. Returns the success value.
    - `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"When", "answer":"Now", "category":"2", "difficulty":"3"}'`
```
{
  "success": true
}
```
  - Also used to search for questions using the submitted search term.
  - `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm":"nounce"}'`
```
{
  "currentCategory": "All",
  "questions": [
    {
      "answer": "Tom Cruise",
      "category_id": 5,
      "difficulty": 4,
      "id": 1,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }
  ],
  "success": true,
  "totalQuestions": 1
}

```
#### POST /quizzes
- General:
    - Returns a success value and a question based on the list of past questions and the question category.
    - `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions":[4, 8, 2], "quiz_category":{"id": 6, "name": "Sports"}}'`
```
{
  "question": {
    "answer": "Brazil",
    "category_id": 6,
    "difficulty": 3,
    "id": 10,
    "question": "Which is the only team to play in every soccer World Cup tournament?"
  },
  "success": true
}
```
#### DELETE /questions/{question_id}
- General:
    - Deletes the question of the given ID if it exists. Returns the id of the deleted book and success value.
- `curl -X DELETE http://127.0.0.1:5000/questions/5`
```
{
  "deleted": 5,
  "success": true
}

```
#### GET /categories
- General:
    - Returns a list of category objects and success value.
- Sample: `curl http://127.0.0.1:5000/categories`

``` 
  {
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports",
    "7": "Misc"
  },
  "success": true
}
```
#### POST /categories
- General:
    - Creates a new category using the submitted category name which must be unique.
- `curl http://127.0.0.1:5000/categories -X POST -H "Content-Type: application/json" -d '{"name":"Funny"}'`
```
{
  "created": 8,
  "success": true
}
```
#### GET /categories/{category_id}/questions
- General:
    - Returns a list of question objects under the category having the provided id, success value and number of questions in this category.
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
- Sample: `curl http://127.0.0.1:5000/categories/4/questions`

``` 
  {
  "currentCategory": "History",
  "questions": [
    {
      "answer": "Muhammad Ali",
      "category_id": 4,
      "difficulty": 1,
      "id": 3,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Maya Angelou",
      "category_id": 4,
      "difficulty": 2,
      "id": 4,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "George Washington Carver",
      "category_id": 4,
      "difficulty": 2,
      "id": 16,
      "question": "Who invented Peanut Butter?"
    }
  ],
  "success": true,
  "totalQuestions": 3
}
```
## Deployment N/A

## Authors
Yours truly, Nobert Etta

## Acknowledgements 
Coach Caryn
The awesome team at Udacity and all the amazing teachers. 
