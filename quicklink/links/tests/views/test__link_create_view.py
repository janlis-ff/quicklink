from unittest.mock import patch

import pytest
from django.urls import resolve
from django.urls import reverse_lazy
from freezegun import freeze_time
from pytest_lazy_fixtures import lf as lazy_fixture
from rest_framework import status

from quicklink.links.models import Link
from quicklink.links.tests.factories import LinkFactory
from quicklink.links.views import LinkCreateView


@pytest.mark.django_db
class TestLinkCreateView:
    viewname = "links:link-create"
    url = reverse_lazy(viewname)

    def test__url(self):
        # WHEN / THEN
        assert self.url == "/api/links/"

    def test__view_class(self):
        # WHEN
        resolved = resolve(self.url).func.view_class

        # THEN
        assert resolved == LinkCreateView

    def test__url_missing(self, anonymous_client):
        # WHEN
        response = anonymous_client.post(self.url, data={})

        # THEN
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"url": ["This field is required."]}

    def test__url_invalid(self, anonymous_client):
        # WHEN
        response = anonymous_client.post(
            self.url,
            data={"url": "invalid_url"},
        )

        # THEN
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"url": ["Please provide a valid URL."]}

    def test__url_too_long(self, anonymous_client):
        # GIVEN
        too_long_url = "https://example.com/" + "a" * 4077

        # WHEN
        response = anonymous_client.post(
            self.url,
            data={"url": too_long_url},
        )

        # THEN
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {
            "url": ["Ensure this field has no more than 4096 characters."],
        }

    @pytest.mark.parametrize(
        argnames=("slug", "expected_error"),
        argvalues=[
            pytest.param(
                "abcdef",
                "Ensure this field has at least 8 characters.",
                id="too_short",
            ),
            pytest.param(
                "abcdefghijklmnopq",
                "Ensure this field has no more than 16 characters.",
                id="too_long",
            ),
            pytest.param(
                "abcd1234",
                "Slug can only contain letters.",
                id="contains_numbers",
            ),
        ],
    )
    def test__slug_invalid(self, anonymous_client, slug, expected_error):
        # WHEN
        response = anonymous_client.post(
            self.url,
            data={"url": "https://example.com/", "slug": slug},
        )

        # THEN
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"slug": [expected_error]}

    def test__slug_already_taken(self, anonymous_client):
        # GIVEN
        LinkFactory(slug="alreadytaken")

        # WHEN
        response = anonymous_client.post(
            self.url,
            data={"url": "https://example.com/", "slug": "alreadytaken"},
        )

        # THEN
        expected_error = "This slug is already taken. Please choose another one."
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"slug": [expected_error]}

    @pytest.mark.parametrize(
        argnames=("url", "slug", "expected_slug"),
        argvalues=[
            pytest.param(
                "https://example.com/abc/",
                None,
                "randomslug",
            ),
            pytest.param(
                "https://example.com/1234/",
                "customslug",
                "customslug",
            ),
        ],
    )
    @pytest.mark.parametrize(
        "client",
        [
            lazy_fixture("anonymous_client"),
            lazy_fixture("user_client"),
        ],
    )
    @patch(
        "quicklink.links.models.Link.get_random_slug",
        new=lambda: "randomslug",
    )
    @freeze_time("2020-01-01")
    def test__success(self, client, url, slug, expected_slug):
        # WHEN
        response = client.post(
            self.url,
            data={"url": url, "slug": slug},
            format="json",
        )
        created_obj = Link.objects.get()

        # THEN
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == {
            "id": created_obj.id,
            "url": url,
            "short_url": f"http://testserver/{expected_slug}",
            "clicks_count": 0,
            "created_at": "2020-01-01T01:00:00+01:00",
        }

    def test__success__assigned_to_user(self, user_client):
        # GIVEN
        current_user = user_client.handler._force_user  # noqa: SLF001

        # WHEN
        response = user_client.post(
            self.url,
            data={"url": "https://example.com/"},
        )
        created_obj = Link.objects.get()

        # THEN
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["id"] == created_obj.id
        assert created_obj.user == current_user
