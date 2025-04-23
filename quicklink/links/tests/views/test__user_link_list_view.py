import pytest
from django.urls import resolve
from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status

from quicklink.links.tests.factories import LinkFactory
from quicklink.links.views import UserLinkListView
from quicklink.users.tests.factories import UserFactory


@pytest.mark.django_db
class TestLinkListView:
    viewname = "links:user-link-list"
    url = reverse(viewname)

    def test__url(self):
        # WHEN / THEN
        assert self.url == "/api/links/user-links/"

    def test__view_class(self):
        # WHEN
        resolved = resolve(self.url).func.view_class

        # THEN
        assert resolved == UserLinkListView

    def test__unauthenticated(self, anonymous_client):
        # WHEN
        response = anonymous_client.get(self.url)

        # THEN
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test__empty_response(self, user_client):
        # WHEN
        response = user_client.get(self.url)

        # THEN
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    @freeze_time("2020-01-01")
    def test__response(self, user_client):
        # GIVEN
        current_user = user_client.handler._force_user  # noqa: SLF001
        other_user = UserFactory()
        link = LinkFactory(
            user=current_user,
            slug="aaa",
            url="https://example.com/link",
        )
        LinkFactory(slug="bbb", user=other_user)
        LinkFactory(slug="ccc", user=None)

        # WHEN
        response = user_client.get(self.url)

        # THEN
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == [
            {
                "id": link.id,
                "url": "https://example.com/link",
                "short_url": "http://testserver/aaa",
                "clicks_count": 0,
                "created_at": "2020-01-01T01:00:00+01:00",
            },
        ]
