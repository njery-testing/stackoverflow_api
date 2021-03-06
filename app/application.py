'''app/application.py'''
import os
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from instance.config import app_config
from app.setup_database import SetupDB

def create_app(config_name):
    '''function enclosing the Flask App'''
    os.environ["ENV"] = config_name
    from app.views import (Signup, Login, Logout,
                           Questions, QuestionsQuestionId, QuestionsAnswers, QuestionsAnswersId,
                           QuestionsAnswersUpvote, QuestionsAnswersDownvote, UserQuestions, UserAnswers,
                           AnswerComments, AnswerCommentsId, SearchQuestion)
    from app.models.revoked_token_model import RevokedTokens

    my_db = SetupDB(config_name)
    my_db.create_db()

    app = Flask(__name__)
    CORS(app)
    api = Api(app, catch_all_404s=True)

    app.url_map.strict_slashes = False
    app.config.from_object(app_config[config_name])
    app.config["TESTING"] = True
    if config_name == "testing":
        app.config['JWT_SECRET_KEY'] = 'j23j434939232i4%#$hjhj2eAJS2e2e3'
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
    jwt = JWTManager(app)

    @jwt.token_in_blacklist_loader
    def _check_if_token_blacklist(decrypted_token):
        '''check if jti(unique identifier) is in BLACKLIST'''
        json_token_identifier = decrypted_token['jti']
        revoked_tokens = RevokedTokens()
        return revoked_tokens.is_jti_blacklisted(json_token_identifier)

    #Add resources to routes
    api.add_resource(Signup, '/api/v1/auth/signup')
    api.add_resource(Login, '/api/v1/auth/login')
    api.add_resource(Logout, '/api/v1/auth/logout')
    api.add_resource(Questions, '/api/v1/questions')
    api.add_resource(QuestionsQuestionId, '/api/v1/questions/<question_id>')
    api.add_resource(QuestionsAnswers, '/api/v1/questions/<question_id>/answers')
    api.add_resource(QuestionsAnswersId, '/api/v1/questions/<question_id>/answers/<answer_id>')
    api.add_resource(QuestionsAnswersUpvote, '/api/v1/questions/<question_id>/answers/<answer_id>/upvote')
    api.add_resource(QuestionsAnswersDownvote, '/api/v1/questions/<question_id>/answers/<answer_id>/downvote')
    api.add_resource(UserQuestions, '/api/v1/users/questions')
    api.add_resource(UserAnswers, '/api/v1/users/answers')
    api.add_resource(AnswerComments, '/api/v1/questions/<question_id>/answers/<answer_id>/comments')
    api.add_resource(AnswerCommentsId, '/api/v1/questions/<question_id>/answers/<answer_id>/comments/<comments_id>')
    api.add_resource(SearchQuestion, '/api/v1/questions/search')
    return app
