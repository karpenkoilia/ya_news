import pytest
from pytest_django.asserts import assertRedirects

from http import HTTPStatus

from django.urls import reverse


@pytest.mark.parametrize(
    "name, args",
    (
        ('news:detail', pytest.lazy_fixture('news_id_for_args')),
        ('news:home', None),
        ('users:login', None),
        ('users:logout', None),
        ('users:signup', None),))
def test_pages_availability(client, name, args,):
    url = reverse(name, args=args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize("user, status", [
    (pytest.lazy_fixture('reader'), HTTPStatus.NOT_FOUND),
    (pytest.lazy_fixture('author'), HTTPStatus.OK),
])
def test_availability_for_comment_edit_and_delete(
    client, comment_obj, user, status):
    client.force_login(user)
    for name in ('news:edit', 'news:delete'):
        url = reverse(name, args=(comment_obj.id,))
        response = client.get(url)
        assert response.status_code == status


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, args',
    (
    ('news:edit', pytest.lazy_fixture('comment_id_for_args')),
    ('news:delete', pytest.lazy_fixture('comment_id_for_args'))
    ))
def test_redirect_for_anonymous_client(client, name, args):
    login_url = reverse('users:login')
    url = reverse(name, args=args)
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url) 