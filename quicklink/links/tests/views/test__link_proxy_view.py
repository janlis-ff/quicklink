import pytest
from django.urls import resolve
from django.urls import reverse
from pytest_lazy_fixtures import lf as lazy_fixture
from rest_framework import status

from quicklink.links.tests.factories import LinkFactory
from quicklink.links.views import LinkProxyView


@pytest.mark.django_db
class TestLinkProxyView:
    viewname = "link-proxy"

    def test__url(self):
        # WHEN
        url = reverse(self.viewname, kwargs={"slug": "testslug"})

        # THEN
        assert url == "/testslug"

    def test__resolved_view(self):
        # WHEN
        url = reverse(self.viewname, kwargs={"slug": "testslug"})
        view = resolve(url)

        # THEN
        assert view.func.view_class == LinkProxyView

    def test__link_not_found(self, anonymous_client):
        # GIVEN
        url = reverse(self.viewname, kwargs={"slug": "nonexistent"})

        # WHEN
        response = anonymous_client.get(url)

        # THEN
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.parametrize(
        "client",
        [
            lazy_fixture("anonymous_client"),
            lazy_fixture("user_client"),
        ],
    )
    def test__success(self, client):
        # GIVEN
        link = LinkFactory(slug="testslug")
        url = reverse(self.viewname, kwargs={"slug": link.slug})

        # WHEN
        response = client.get(url)
        link.refresh_from_db()

        # THEN
        assert response.status_code == status.HTTP_302_FOUND
        assert response.url == link.url
        assert link.clicks_count == 1
