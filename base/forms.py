from django.forms import ModelForm
from .models import Question
from django.contrib.auth.models import User

class QuestionForm(ModelForm):
    class Meta:
        model=Question
        fields="__all__"
        exclude=['host', 'participants']

class UserForm(ModelForm):
    class Meta:
        model=User
        fields=['username']

        