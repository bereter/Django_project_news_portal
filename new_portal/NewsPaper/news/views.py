from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from django.urls import reverse_lazy
from datetime import datetime
from .filters import NewsFilter
from .forms import NewsForm
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

class NewsList(ListView):
    model = Post
    ordering = '-data_time'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context


class NewsSearch(ListView):
    model = Post
    ordering = '-data_time'
    template_name = 'news_search.html'
    context_object_name = 'news_search'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs


class NewsBlockDetail(DetailView):
    model = Post
    template_name = 'news_block.html'
    context_object_name = 'news_block'


class NewsCreate(CreateView, LoginRequiredMixin):
    form_class = NewsForm
    model = Post
    template_name = 'news_create.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.article_or_news = 'NE'
        return super().form_valid(form)


class ArticlesCreate(CreateView, LoginRequiredMixin):
    form_class = NewsForm
    model = Post
    template_name = 'articles_create.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.article_or_news = Post.news
        return super().form_valid(form)


class NewsUpdate(UpdateView, LoginRequiredMixin):
    form_class = NewsForm
    model = Post
    queryset = Post.objects.filter(article_or_news='NE')
    template_name = 'news_edit.html'


class ArticlesUpdate(UpdateView, LoginRequiredMixin):
    form_class = NewsForm
    model = Post
    queryset = Post.objects.filter(article_or_news='AR')
    template_name = 'articles_edit.html'


class NewsDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')
    queryset = Post.objects.filter(article_or_news='NE')


class ArticlesDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')
    queryset = Post.objects.filter(article_or_news='AR')


