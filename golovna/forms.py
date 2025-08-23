from django import forms
from .models import Comment, UserProfile, Event, Group
from django.contrib.auth.models import User

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

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ["name", "bio", "ava"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Назва групи"}),
            "bio": forms.Textarea(attrs={"class": "form-control", "placeholder": "Опис групи", "rows": 4}),
            "ava": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
        labels = {
            "name": "Назва групи",
            "bio": "Опис",
            "ava": "Аватар",
        }

class OwnerForm(forms.Form):
    new_owner = forms.ModelChoiceField(queryset=User.objects.none(), label="Передати права користувачу")

    def __init__(self, group, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_owner'].queryset = group.member.exclude(pk=group.owner.pk)