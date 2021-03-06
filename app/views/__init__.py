'''view/__init__.py'''
from app.views.user_registration import Signup, Login, Logout
from app.views.questions import (Questions, QuestionsQuestionId, QuestionsAnswers,
                                 QuestionsAnswersId, QuestionsAnswersUpvote,
                                 QuestionsAnswersDownvote, UserQuestions, UserAnswers, SearchQuestion)
from app.views.comments import (AnswerComments, AnswerCommentsId)
