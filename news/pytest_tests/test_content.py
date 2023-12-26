import pytest

from django.conf import settings
from django.urls import reverse



def test_news_count(author_client, home_url):
    response =author_client.get(home_url)
    object_list = response.context['object_list']
    news_count = len(object_list)
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE

def test_news_order(author, home_url):
    response = author.get(home_url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order(author_client,
                        news, detail_url,
                        comments_for_test_order):
    response = author_client.get(detail_url)
    if 'news' in response.context:
        all_comments = news.comment_set.all()
        assert all_comments[0].created < all_comments[1].created