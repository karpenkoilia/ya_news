from http import HTTPStatus
from django.urls import reverse
import pytest

from news.models import Comment, News

from news.forms import BAD_WORDS, WARNING

from pytest_django.asserts import assertFormError, assertRedirects


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, news, form_data):
    url = reverse('news:detail', args=(news.id,))
    client.post(url, data=form_data)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_can_create_comment(author_client, author, form_data,
                                 news, comment_text):
    url = reverse('news:detail', args=(news.id,))
    author_client.post(url, data=form_data)
    comments_count = Comment.objects.count()
    assert comments_count == 1
    comment = Comment.objects.get()
    assert comment.text == comment_text
    assert comment.news == news
    assert comment.author == author


def test_user_cant_use_bad_words(author_client, news_url):
    url = news_url
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = author_client.post(url, data=bad_words_data)
    assertFormError(response, form='form', field='text', errors=WARNING)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_author_can_delete_comment(author_client, delete_url,news_url,):
    response = author_client.delete(delete_url)
    url_to_comments = news_url + '#comments'
    assertRedirects(response, url_to_comments)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_cant_delete_comment_of_another_user(reader_client, delete_url):
    response = reader_client.delete(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count = Comment.objects.count()
    assert comments_count == 1


def test_author_can_edit_comment(author_client, edit_url, form_data_update,
                                 comment_obj, news_url, new_comment_text):
    response = author_client.post(edit_url, data=form_data_update)
    url_to_comments = news_url + '#comments'
    assertRedirects(response, url_to_comments)
    comment_obj.refresh_from_db()
    assert comment_obj.text == new_comment_text


def test_user_cant_edit_comment_of_another_user(reader_client, edit_url,
                                                form_data_update, comment_obj,
                                                comment_text):
    response = reader_client.post(edit_url, data=form_data_update)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_obj.refresh_from_db()
    assert comment_obj.text, comment_text