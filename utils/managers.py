from django.db import models


class ApprovedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(approved_time__isnull=False, approved_user__isnull=False)