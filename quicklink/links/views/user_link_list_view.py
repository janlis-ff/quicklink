from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema_view
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from quicklink.links.models import Link
from quicklink.links.serializers import LinkSerializer


@extend_schema_view(
    get=extend_schema(
        summary=_("List current user's links"),
        description=_("Retrieve a list of links created by the current user."),
    ),
)
class UserLinkListView(ListAPIView):
    serializer_class = LinkSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Link.objects.filter(
            user=self.request.user,
        ).order_by("-created_at")
