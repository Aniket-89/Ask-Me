from django.contrib.auth.models import User
from django.db import models

class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_answers', blank=True)

    def __str__(self):
        return f"Answer to '{self.question.title}' by {self.user.username}"

    def total_likes(self):
        return self.likes.count()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add any additional user profile fields you need (e.g., profile picture, bio, etc.)

    def __str__(self):
        return self.user.username
