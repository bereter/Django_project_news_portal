from django.urls import path
# Импортируем созданное нами представление
from .views import NewsList, NewsBlockDetail, NewsSearch, NewsCreate, ArticlesCreate, NewsUpdate, ArticlesUpdate, \
    NewsDelete, ArticlesDelete, upgrade_me, subscription_me

urlpatterns = [
    path('', NewsList.as_view(), name='news_list'),
    path('<int:pk>', NewsBlockDetail.as_view(), name='news_detail'),
    path('search/', NewsSearch.as_view(), name='news_search'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('articles/create/', ArticlesCreate.as_view(), name='articles_create'),
    path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),
    path('articles/<int:pk>/edit/', ArticlesUpdate.as_view(), name='articles_edit'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('articles/<int:pk>/delete/', ArticlesDelete.as_view(), name='articles_delete'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('upgrade_subscription/', subscription_me, name='upgrade_subscription')
]
