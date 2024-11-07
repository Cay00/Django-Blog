# blog/forms.py
from django import forms
from .models import Comment, Vote


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  # Tylko treść komentarza


class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ['value']  # Zawiera tylko pole 'value', bo to jest głosowanie
