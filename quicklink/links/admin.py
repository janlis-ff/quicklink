from django.contrib import admin

from quicklink.links import models

admin.site.register(
    models.Link,
    admin.ModelAdmin,
)
