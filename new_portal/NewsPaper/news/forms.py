from django import forms
from .models import Post
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


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
