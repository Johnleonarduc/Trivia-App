# The Trivia App Project

## Introduction
This is the final project of the API Develoment and Documentation Module in Udacity's Full Stack Web Development Course.
I forked the starter folder which already includes a working frontend that is fully reliant on the backend APIs i was meant to implement. It also included some basic setup code and project instructions.

The Trivia game is an investment by Udacity to create bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where I came in and helped to finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. 

The application does the following:

1. Display questions - both all questions and by category. Questions show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that users include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

## About the Stack

This application is built with Python, Flask, SqlAlchemy, and Postgress for Backend and React, JavaScript, CSS, and HTML for Frontend.

This app can be run locally for now. To run the app locally, you must first setup the backend requirements and start the server, then install the frontend requirements and start its server likewise.

### Backend Setup Steps - Trivia API

1. **Python 3.7** - Follow instructions to install the latest version of python for the app in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - Instructions for setting up a virtual environment for the app can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```
#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `__init__.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension used to handle cross-origin requests from our frontend server.

### Seting up the Database

Make sure Postgres service is running on your pc, then create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql 

or

psql -U postgres -d trivia -f trivia.psql (for Windows if the above did not work for you)

```

#### Set Up your environment variables:
1. Install python-dotenv:
```bash
pip install python-dotenv
```

2. Import dotenv: (This has already been done for you in models.py)
    see line: from dotenv import dotenv_values
3. Create a .env file in the same directory as your models.py. Inside it, 
    set your database USERNAME and PASSWORD credentials same as those used to create your database in psql. eg.
    USERNAME=john
    PASSWORD=12345

Now, you have installed all requirements for the app, and you have data in your local trivia database, time to run your server.

### Run your Server

From within the `./flaskr ` directory, first ensure you are working using your created virtual environment by running:
```bash
where python
```
To run the server, execute the command below from same directory:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

# Setting Up The Frontend

## Intall Dependences:
1. **Installing Node and NPM**
   This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

2. **Installing project dependencies**
   This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. A
   
   Navigate to you /frontend directory in your terminal and run: 

```bash
npm install
```
3. Run the Frontend Server:
In order to run the app in development mode use:
```bash
npm start
```
4. Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.


# API Endpoints and Documentation

## All GET Endpoint

`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Parameters: None
- Response Body: An object with a single key, categories, that contains an object of id: category_string key:value pairs.

```json
{
  "success": "true",
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```

---

`GET '/questions?page=${integer}&category=${id}'`

- Fetches a paginated set of questions, a total number of questions, all categories and current category string. Due to the need for a current category in the project requirements, a category field is included as part of the query parameters - if not explicitly stated, the first category is implied.
- Request Parameters: `page` - integer, `category` - integer
- Response body: An object with 10 paginated questions, total questions, object including all categories, and current category string

```json
{
  "success": "true",
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 2
    }
  ],
  "total_questions": 100,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": "History"
}
```

---

`GET '/categories/${id}/questions'`

- Fetches questions for a cateogry specified by id request argument
- Request Parameters: `id` - integer
- Response body: An object with questions for the specified category, total questions, and current category string

```json
{
  "success": "true",
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 4
    }
  ],
  "total_questions": 100,
  "current_category": "History"
}
```

---
## ALL POST Endpoints

`POST '/quizzes'`

- Sends a post request in order to get the next question
- Request Body:

```json
{
    "previous_questions": [1, 4, 20, 15],
    "quiz_category": "current category"
 }
```

- Response body: it returns a single new question object

```json
{
  "success":"true",
  "question": {
    "id": 1,
    "question": "This is a question",
    "answer": "This is an answer",
    "difficulty": 5,
    "category": 4
  }
}
```

---

`POST '/questions'`

- Sends a post request in order to add a new question
- Request Body:

```json
{
  "question": "Heres a new question string",
  "answer": "Heres a new answer string",
  "difficulty": 1,
  "category": 3
}
```

- Response body: It returns success message of true

```json
{
  "success": "true"
}
```

---

`POST '/questions'`

- Sends a post request in order to search for a specific question by search term
- Request Body:

```json
{
  "searchTerm": "this is the term the user is looking for"
}
```

- Response body: returns any array of questions, a number of totalQuestions that met the search term and the current category string

```json
{
  "success": "true",
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 5
    }
  ],
  "total_questions": 100,
  "current_category": "Entertainment"
}
```

## All Delete Endpoint(s)

`DELETE '/questions/${id}'`

- Deletes a specified question using the id of the question
- Request Parameter: `id` - integer
- Response body: It returns the appropriate HTTP status code and question id. 

```json
{
  "status": 200,
  "id": 5,
}
```

Thank you for viewing my project. Enjoy!

---
