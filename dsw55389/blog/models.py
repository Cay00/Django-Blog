# blog/models.py
from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Post(models.Model):
    # Twoje pole dla postu
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def likes(self):
        return self.votes.filter(value=1).count()  # Liczba głosów na "lubię to"

    @property
    def dislikes(self):
        return self.votes.filter(value=-1).count()  # Liczba głosów na "nie lubię tego"


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"


class Vote(models.Model):
    VOTE_CHOICES = [
        (1, 'Like'),
        (-1, 'Dislike'),
    ]
    post = models.ForeignKey(Post, related_name='votes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.SmallIntegerField(choices=VOTE_CHOICES)

    class Meta:
        unique_together = ('post', 'user')  # Umożliwia tylko jeden głos na post od danego użytkownika

    def __str__(self):
        return f"{self.user.username} - {self.get_value_display()} on {self.post.title}"
