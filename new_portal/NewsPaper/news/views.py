from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category
from django.urls import reverse_lazy
from datetime import datetime
from .filters import NewsFilter
from .forms import NewsForm
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/NewsPaper/')


@login_required
def subscription_me(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)


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
        context['is_not_premium'] = not self.request.user.groups.filter(name='authors').exists()
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscription'] = self.request.user
        return context


class NewsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_create.html'
    permission_required = ('news.add_post', )

    def form_valid(self, form):
        news = form.save(commit=False)
        news.article_or_news = 'NE'
        return super().form_valid(form)


class ArticlesCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'articles_create.html'
    permission_required = ('news.add_post', )

    def form_valid(self, form):
        news = form.save(commit=False)
        news.article_or_news = Post.news
        return super().form_valid(form)


class NewsUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = NewsForm
    model = Post
    queryset = Post.objects.filter(article_or_news='NE')
    template_name = 'news_edit.html'
    permission_required = ('news.change_post', )


class ArticlesUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = NewsForm
    model = Post
    queryset = Post.objects.filter(article_or_news='AR')
    template_name = 'articles_edit.html'
    permission_required = ('news.change_post', )


class NewsDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')
    queryset = Post.objects.filter(article_or_news='NE')
    permission_required = ('news.delete_post', )


class ArticlesDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')
    queryset = Post.objects.filter(article_or_news='AR')
    permission_required = ('news.delete_post', )


