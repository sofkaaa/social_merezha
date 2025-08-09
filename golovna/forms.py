from django import forms
from .models import Comment, UserProfile, Event

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Напиши щось...'}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['ava', 'bio']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'bescription', 'data']
        widgets = {
            'data': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }