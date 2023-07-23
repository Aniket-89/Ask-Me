from django.urls import path, include
from .views import (
    IndexView,
    QuestionDetailView,
    QuestionEditView,
    PostQuestionView,
    AnswerEditView,
    LikeAnswerView,
    PostAnswerView,
    LogoutView,
    SignupView,
    CustomLoginView,
)

app_name = "core"

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),

    path('question/<int:pk>/', QuestionDetailView.as_view(), name='question_detail'),
    path('post_question/', PostQuestionView.as_view(), name='post_question'),
    path('post_answer/<int:question_id>/', PostAnswerView.as_view(), name='post_answer'),
    path('like_answer/<int:answer_id>/', LikeAnswerView.as_view(), name='like_answer'),
    
    path('edit_question/<int:pk>/', QuestionEditView.as_view(), name='edit_question'),
    path('edit_answer/<int:pk>/', AnswerEditView.as_view(), name='edit_answer'),

]