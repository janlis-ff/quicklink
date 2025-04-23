from django.db.models import F
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from quicklink.links.models import Link


class LinkProxyView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, slug):
        link = get_object_or_404(Link, slug=slug)
        Link.objects.filter(pk=link.pk).update(clicks_count=F("clicks_count") + 1)
        return redirect(link.url)
