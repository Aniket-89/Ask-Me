from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout, login
from django.views.generic import DetailView, CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import View
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm


class IndexView(View):
    def get(self, request):
        # Get all the questions from the database and render them on the index page
        questions = Question.objects.all()
        context = {'questions' : questions}
        return render(request, 'core/index.html', context)

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        if self.request.user.is_authenticated:
            return reverse_lazy('core:index')  # Redirect to 'core:index' (change it to your index URL name)
        return reverse_lazy('core:login')
    

class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('core:index')

class SignupView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'registration/signup.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('core:index')
        return render(request, 'registration/signup.html', {'form': form})



class QuestionDetailView(DetailView):
    model = Question
    template_name = 'core/question_detail.html'
    context_object_name = 'question'



class PostQuestionView(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'core/post_question.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PostAnswerView(LoginRequiredMixin, CreateView):
    model = Answer
    form_class = AnswerForm
    template_name = 'core/post_answer.html'
    context_object_name = 'question'

    def form_valid(self, form):
        question = get_object_or_404(Question, id=self.kwargs['question_id'])
        form.instance.user = self.request.user
        form.instance.question = question
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = get_object_or_404(Question, id=self.kwargs['question_id'])
        return context

    def get_success_url(self):
        return reverse_lazy('question_detail', kwargs={'pk': self.kwargs['question_id']})


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
        return reverse_lazy('question_detail', kwargs={'question_id': self.object.id})


class AnswerEditView(LoginRequiredMixin, UpdateView):
    model = Answer
    form_class = AnswerForm
    template_name = 'core/edit_answer.html'
    context_object_name = 'answer'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('question_detail', kwargs={'question_id': self.object.question.id})

