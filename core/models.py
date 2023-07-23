from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse_lazy

class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse_lazy('core:question_detail', args=[str(self.id)])
    

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_answers', blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Answer to '{self.question.title}' by {self.user.username}"

    def total_likes(self):
        return self.likes.count()
    

    def get_absolute_url(self):
        return reverse_lazy('core:question_detail', args=[str(self.question.id)])


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
    def get_absolute_url(self):
        return reverse_lazy('user_detail', args=[str(self.id)])

