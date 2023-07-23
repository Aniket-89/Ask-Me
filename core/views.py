from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from django.views.generic import UpdateView
from django.urls import reverse
from django.views import View
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm


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
        return render(request, 'core/signup.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        return render(request, 'core/signup.html', {'form': form})


class QuestionDetailView(View):
    def get(self, request, question_id):
        # Fetch the question and its answers from the database and render the detail page
        question = get_object_or_404(Question, id=question_id)
        answers = Answer.objects.filter(question=question)
        return render(request, 'core/question_detail.html', {'question': question, 'answers': answers})


class PostQuestionView(LoginRequiredMixin, View):
    def get(self, request):
        form = QuestionForm()
        return render(request, 'core/post_question.html', {'form': form})

    def post(self, request):
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            return redirect('question_detail', question_id=question.id)
        return render(request, 'core/post_question.html', {'form': form})


class PostAnswerView(LoginRequiredMixin, View):
    def get(self, request, question_id):
        question = get_object_or_404(Question, id=question_id)
        form = AnswerForm()
        return render(request, 'core/post_answer.html', {'question': question, 'form': form})

    def post(self, request, question_id):
        question = get_object_or_404(Question, id=question_id)
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user
            answer.question = question
            answer.save()
            return redirect('question_detail', question_id=question.id)
        return render(request, 'core/post_answer.html', {'question': question, 'form': form})


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


class QuestionEditView(LoginRequiredMixin, UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = 'core/edit_question.html'
    context_object_name = 'question'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_success_url(self):
        return reverse('question_detail', kwargs={'question_id': self.object.id})


class AnswerEditView(LoginRequiredMixin, UpdateView):
    model = Answer
    form_class = AnswerForm
    template_name = 'core/edit_answer.html'
    context_object_name = 'answer'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_success_url(self):
        return reverse('question_detail', kwargs={'question_id': self.object.question.id})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('index')