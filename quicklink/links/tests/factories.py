from factory import Sequence
from factory import SubFactory
from factory.django import DjangoModelFactory

from quicklink.links.models import Link
from quicklink.users.tests.factories import UserFactory


class LinkFactory(DjangoModelFactory):
    url = Sequence(lambda n: f"https://example.com/{n}")
    user = SubFactory(UserFactory)

    class Meta:
        model = Link
