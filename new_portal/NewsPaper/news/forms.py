from django import forms
from .models import Post


class NewsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'name_news',
            'text_news',
            'author_post',
            'post_category',
        ]
