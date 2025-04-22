from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema_view
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from quicklink.links.models import Link
from quicklink.links.serializers import LinkSerializer


@extend_schema_view(
    post=extend_schema(
        summary=_("Create a short link"),
        description=_(
            "Allows to create a new short link. If the slug is not "
            "provided, a random slug will be assigned.",
        ),
    ),
)
class LinkCreateView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LinkSerializer
    queryset = Link.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.request.user.is_authenticated:
            context["user"] = self.request.user
        return context
