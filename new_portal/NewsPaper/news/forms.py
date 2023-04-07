from django import forms
from .models import Post
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group, User
from django.contrib.auth.forms import UserCreationForm


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    first_name = forms.CharField(label = "Имя")
    last_name = forms.CharField(label = "Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2", )


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user


class NewsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'name_news',
            'text_news',
            'author_post',
            'post_category',
        ]
