from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from django.urls import reverse
from django.views import View
from .models import Question, Answer

# Create your views here.
class IndexView(View):
    def get(self, request):
        # Get all the questions from the database and render them on the index page
        questions = Question.objects.all()
        context = {'questions' : questions}
        return render(request, 'core/index.html', context)

def login_view(request):
    pass

class SignupView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'registration/signup.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        return render(request, 'registration/signup.html', {'form': form})

class QuestionDetailView(View):
    def get(self, request, question_id):
        # Fetch the question and its answers from the database and render the detail page
        question = get_object_or_404(Question, id=question_id)
        answers = Answer.objects.filter(question=question)
        return render(request, 'core/question_detail.html', {'question': question, 'answers': answers})

class PostQuestionView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'core/post_question.html')

    def post(self, request):
        # Process the form data when the user submits the question
        title = request.POST['title']
        content = request.POST['content']
        user = request.user
        question = Question.objects.create(title=title, content=content, user=user)
        return redirect('question_detail', question_id=question.id)

class PostAnswerView(LoginRequiredMixin, View):
    def get(self, request, question_id):
        question = get_object_or_404(Question, id=question_id)
        return render(request, 'core/post_answer.html', {'question': question})

    def post(self, request, question_id):
        question = get_object_or_404(Question, id=question_id)
        # Process the form data when the user submits the answer
        content = request.POST['content']
        user = request.user
        answer = Answer.objects.create(question=question, content=content, user=user)
        return redirect('question_detail', question_id=question.id)

class LikeAnswerView(LoginRequiredMixin, View):
    def get(self, request, answer_id):
        answer = get_object_or_404(Answer, id=answer_id)
        user = request.user

        # Check if the user has already liked the answer
        if user in answer.likes.all():
            # Unlike the answer
            answer.likes.remove(user)
        else:
            # Like the answer
            answer.likes.add(user)

        return redirect('question_detail', question_id=answer.question.id)

@login_required
def edit_question_view(request, pk):
    pass

@login_required
def delete_question_view(request, pk):
    pass

class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('index')