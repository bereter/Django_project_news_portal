from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
    user_author = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user_author)

    def update_rating(self):
        rating_posts_author = Post.objects.filter(author_post_id=self.pk).aggregate(rating_news=Sum('rating_news'))[
            'rating_news']
        rating_comments_author = \
            Comment.objects.filter(user_comment_id=self.pk).aggregate(rating_comment=Sum('rating_comment'))[
                'rating_comment']
        rating_comments_posts = \
            Comment.objects.filter(post_comment__author_post=self.pk).aggregate(rating_comment=Sum('rating_comment'))[
                'rating_comment']
        self.user_rating = rating_posts_author * 3 + rating_comments_author + rating_comments_posts
        self.save()


class Category(models.Model):
    world_events = 'WE'
    politics = 'PO'
    culture = 'CU'
    economics = 'EC'
    technology = 'TE'
    science = 'SC'

    CATEGORY_NEWS = [
        (world_events, 'События в мире'),
        (politics, 'Политика'),
        (culture, 'Культура'),
        (economics, 'Экономика'),
        (technology, 'Технологии'),
        (science, 'Наука')
    ]

    category_new = models.CharField(max_length=2, choices=CATEGORY_NEWS, unique=True)
    subscribers = models.ManyToManyField(User, through='AuthorCategory')

    def __str__(self):
        return self.category_new


class Post(models.Model):
    news = 'NE'
    article = 'AR'
    FIELD = [
        (news, 'Новость'),
        (article, 'Статья')
    ]

    article_or_news = models.CharField(max_length=2, choices=FIELD)
    data_time = models.DateTimeField(auto_now_add=True)
    name_news = models.CharField(max_length=255)
    text_news = models.TextField()
    rating_news = models.IntegerField(default=0)
    author_post = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_category = models.ManyToManyField(Category, through='PostCategory')

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])

    def like_post(self):
        self.rating_news += 1
        self.save()

    def dislike_post(self):
        self.rating_news -= 1
        self.save()

    def preview(self):
        return self.text_news[0:124] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class AuthorCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    text_comment = models.TextField()
    data_time_comment = models.DateTimeField(auto_now_add=True)
    rating_comment = models.IntegerField(default=0)
    post_comment = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE)

    def like_comment(self):
        self.rating_comment += 1
        self.save()

    def dislike_comment(self):
        self.rating_comment -= 1
        self.save()
