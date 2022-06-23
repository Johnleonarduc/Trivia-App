import os
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

#function to paginate questions based on questions_per_page
def paginate_questions(request, questions):
    #get the page query value from the request arguement, default to 1 if not available
    page = request.args.get("page", 1, type=int)
   #define where to start pagination
    start = (page - 1) * QUESTIONS_PER_PAGE
    #define where pagination stops
    end = start + QUESTIONS_PER_PAGE

    #properly format questions passed as arguement
    format_questions = [question.format() for question in questions]
    #slice out the questions for the paginated page
    current_questions = format_questions[start:end]

    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    #COR(Cross-Origin Request Setup)
    CORS(app)

    #set CORS response headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    #Endpoint to handle GET requests for all available categories.
    @app.route('/categories')
    def get_categories():
        #query categories database for all categories and properly format them for the frontend
        try:
            categories = [Category.format(item) for item in Category.query.all()]
            f_category = {}
            for category in categories:
                f_category[category['id']] = category['type']

            return jsonify({
                'success': True,
                'categories': f_category
            })
        except:
            abort(404)

    #Endpoint to handle GET requests for /questions, including pagination (every 10 questions)
    #Endpoint was modified to accept optional query parameters from the frontend eg. /questions?page=1&category=1
    @app.route('/questions', methods=['GET'])
    def get_paginated_questions():
        #get the optional category query parameter; default to 1 if absent
        request_category = request.args.get("category", 1, type=int)
        #check if request category exists
        category_check = Category.query.filter(Category.id == request_category).one_or_none()
        if not category_check:
            abort(404)
        try:
            #query DB for questions under the request category ordered by their ids
            questions = Question.query.filter(Question.category == request_category).order_by(Question.id).all()
            #derive current questions under requested category well paginated
            current_questions = paginate_questions(request, questions)
            
            if not current_questions:
                abort(400)

            #get categories
            categories = [Category.format(item) for item in Category.query.all()]
            f_category = {}
            for category in categories:
                f_category[category['id']] = category['type']
            
            
            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(questions),
                'categories': f_category,
                'current_category': Category.query.filter(Category.id == request_category).one().format()['type']
                
            })
        except:
            abort(400)

   #endpoint to DELETE question using a question ID.
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        #get the particular question from DB
        question = Question.query.filter(Question.id == question_id).one_or_none()
        
        if question is None:
            abort(404)

        try:
            question.delete()

            return jsonify({
                'status': 200,
                'id': question_id
            })
        except:
            abort(422)


    #Endpoint to POST a new question,which will require the question and answer text,category, and difficulty score.
    @app.route('/questions', methods=['POST'])
    def post_question():
        body = request.get_json()
        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_difficulty = body.get('difficulty', None)
        new_category = body.get('category', None)
        searchterm = body.get('searchTerm', None)

        #implement search feature
        try:
            if searchterm:
                search_result = Question.query.filter(Question.question.ilike('%{}%'.format(searchterm))).all()

                return jsonify({
                    'success':True,
                    'questions': [question.format() for question in search_result],
                    'total_questions': len(search_result),
                    'current_category': Category.query.filter(Category.id == [question.format() for question in search_result][0]['category']).one().format()['type']
                })
            #implement POST for new question
            elif new_question:
                if (bool(new_question) == True and bool(new_answer) == True and bool(new_category) == True and bool(new_difficulty) == True):
                    question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
                    question.insert()

                    # return get_paginated_questions()
                    return jsonify({"success":True})
                else:
                    abort(422)
            else:
                 abort(400)
        except:
            abort(422)

    #endpoint to get questions based on category.
    @app.route('/categories/<int:category_id>/questions')
    def get_category_questions(category_id):
        try:   
            category_questions = [question.format() for question in Question.query.filter(Question.category == category_id).all()]

            return jsonify({
                'success': True,
                'questions': category_questions,
                'total_questions': len(category_questions),
                'current_category': Category.query.filter(Category.id == category_id).one().format()['type']
            })
        except:
            abort(400)

    #endpoint to get questions to play the quiz.
    #it takes category and previous question parameters
    #and return a random questions within the given category,
    #if provided, and that is not one of the previous questions.
    @app.route('/quizzes', methods=['POST'])
    def get_quiz_question():
        body = request.get_json()
        previous_questions = body.get('previous_questions',None)
        quiz_category = body.get('quiz_category', None)

        try:
            #handle all categories case, with type of click and id of 0
            if(quiz_category['type'] == 'click' and quiz_category['id'] == 0):
                #fetch all questions
                all_questions = [question.format() for question in Question.query.all()]
                #get ids of all questions
                all_question_ids = [question['id'] for question in all_questions]

                #handle cases where previous questions are suplied in the request
                if previous_questions:
                    #separate previous question ids from category questions
                    [all_question_ids.remove(q_id) for q_id in previous_questions]
                    #get a random question id
                    rand_question_id = all_question_ids[random.randint(0, (len(all_question_ids)-1))]

                    return jsonify({
                        'success': True,
                        #use random question id to return that particular question
                        'question': list(filter(lambda quest: quest['id']==rand_question_id, all_questions))[0]
                        })

                #handle cases where no previous questions was provided
                else:
                    #get a random question id from all_questions_id 
                    rand_question_id = all_question_ids[random.randint(0, (len(all_question_ids)-1))]
                    return jsonify({
                        'success': True,
                        ##use random question id to return that particular question
                        'question':list(filter(lambda quest: quest['id']==rand_question_id, all_questions))[0]
                        })

            #handle cases that are with category specified that are not the "All" option case
            else:
                #get the id of the category specified in the request from the database
                category = Category.query.filter(Category.type == quiz_category['type']).one_or_none()
                #handle any case where category id is not found in the DB
                if category is None:
                    abort(404)

                category_id = category.format()['id']
                #use the category id derived to fetch all questions in that category
                category_questions = [question.format() for question in Question.query.filter(Question.category == category_id).all()]
                #get the ids of all questions in that category
                all_question_ids = [question['id'] for question in category_questions]
            
                #handle cases where previous questions are suplied in the request
                if previous_questions:
                    #remove all previous_questions ids from all_question_ids 
                    [all_question_ids.remove(q_id) for q_id in previous_questions]
                    #get random question id
                    rand_question_id = all_question_ids[random.randint(0, (len(all_question_ids)-1))]

                    return jsonify({
                        'success': True,
                        #use random question id to return that particular question
                        'question': list(filter(lambda quest: quest['id']==rand_question_id, category_questions))[0]
                        })

                #handle cases where no previous questions was provided
                else:
                    #get a random question id from all_questions_id 
                    rand_question_id = all_question_ids[random.randint(0, (len(all_question_ids)-1))]
                    return jsonify({
                        'success': True,
                        ##use random question id to return that particular question
                        'question':list(filter(lambda quest: quest['id']==rand_question_id, category_questions))[0]
                        })
        except:
            abort(400)

    #error handlers for all expected errors 404 and 422.
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

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    return app