from django.db import models
from django.conf import settings

from django.utils import timezone


class UserVisit(models.Model):
    """
    We'll track each time a user visited the site
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    last_seen = models.DateTimeField(auto_now=True)
    visits = models.PositiveIntegerField(default=0)

    @classmethod
    def all_visitors_count(cls) -> int:
        return cls.objects.all().count()

    @classmethod
    def all_visits_in_last_hour_count(cls) -> int:
        """could pass in a timedelta or parameter to make it more flexible, but this should be enough for the spec"""
        return cls.objects.filter(
            last_seen__gte=(timezone.now() - timezone.timedelta(hours=1))
        ).count()

    @classmethod
    def all_visits_count(cls) -> int:
        return cls.objects.aggregate(models.Sum("visits"))["visits__sum"]
