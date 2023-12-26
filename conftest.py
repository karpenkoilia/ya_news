from django.urls import reverse
from django.utils import timezone
from django.conf import settings

from datetime import datetime, timedelta

import pytest

from news.models import News, Comment



# Фикстура создающая лбьект модели User.
@pytest.fixture
def author(django_user_model):  
    return django_user_model.objects.create(username='Автор')

# Фикстура создающая залогиненного юзера.
@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client

@pytest.fixture
def news():
    news = News.objects.create(
        title='Заголовок',
        text='Текст',
    )
    return news

@pytest.fixture
def comment_obj(author, news):
    comment = Comment.objects.create(
            news=news,
            author=author,
            text='Текст комментария'
        )
    return comment

@pytest.fixture
# Фикстура запрашивает другую фикстуру создания заметки.
def news_id_for_args(news):  
    # И возвращает кортеж, который содержит id заметки.
    # На то, что это кортеж, указывает запятая в конце выражения.
    return news.id,

@pytest.fixture
def comment_id_for_args(comment):
    return comment.id,

@pytest.fixture
def all_news():
    today = datetime.today()
    all_news = [
            News(
                title=f'Новость {index}',
                text='Просто текст.',
                date=today - timedelta(days=index))
            for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
        ]
    News.objects.bulk_create(all_news)

@pytest.fixture
def detail_url():
    detail_url = reverse('news:detail', args=(news_id_for_args,))
    return detail_url

@pytest.fixture
def home_url():
    return reverse('news:home')

@pytest.fixture
def comments_for_test_order():
    now = timezone.now()
    for index in range(2):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Tекст {index}',
            )
        comment.created = now + timedelta(days=index)
            # И сохраняем эти изменения.
        comment.save()

@pytest.fixture
def db():
    return db