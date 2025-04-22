from __future__ import annotations

import random
import string

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Link(models.Model):
    slug = models.SlugField(
        max_length=16,
        unique=True,
        db_index=True,
    )
    url = models.TextField(
        max_length=4096,
        blank=False,
        null=False,
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="links",
        null=True,
        blank=True,
    )
    clicks_count = models.PositiveBigIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        url = self.url if len(self.url) < 20 else self.url[:20] + "..."
        return f"{self.slug} ({url})"

    @classmethod
    def create(
        cls,
        url: str,
        slug: str | None = None,
        user: User | None = None,
    ) -> Link:
        if slug is None:
            slug = cls.get_random_slug()
        return cls.objects.create(url=url, slug=slug, user=user)

    @classmethod
    def get_random_slug(cls) -> str:
        while True:
            slug = "".join(random.choices(string.ascii_letters, k=8))  # noqa: S311
            try:
                cls.objects.get(slug=slug)
            except cls.DoesNotExist:
                return slug
