from string import ascii_letters

from django.db.utils import IntegrityError
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from quicklink.links.models import Link


class LinkSerializer(serializers.ModelSerializer):
    MIN_LENGTH = 8
    MAX_LENGTH = 16

    url = serializers.CharField(
        max_length=4096,
        required=True,
    )
    slug = serializers.SlugField(
        min_length=MIN_LENGTH,
        max_length=MAX_LENGTH,
        required=False,
        allow_blank=False,
        allow_null=True,
    )
    clicks_count = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    def validate_slug(self, value):
        if value is None:
            return value
        if not all(char in ascii_letters for char in value):
            raise ValidationError(_("Slug can only contain letters."))
        return value

    def validate_url(self, value):
        if not value.startswith("http://") and not value.startswith("https://"):
            raise ValidationError(_("Please provide a valid URL."))
        return value

    def create(self, validated_data):
        try:
            return Link.create(
                url=validated_data["url"],
                slug=validated_data.get("slug", None),
                user=self.context.get("user", None),
            )
        except IntegrityError as e:
            raise ValidationError(
                {"slug": [_("This slug is already taken. Please choose another one.")]},
            ) from e

    class Meta:
        model = Link
        fields = (
            "id",
            "slug",
            "url",
            "clicks_count",
            "created_at",
        )
