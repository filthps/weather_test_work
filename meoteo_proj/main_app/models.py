from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


validator_x = RegexValidator(r"\d{2}\.\d{3}")
validator_y = RegexValidator(r"\d{3}\.\d{3}")


class History(models.Model):
    city_name = models.CharField(max_length=50)
    x = models.FloatField(blank=False, validators=(validator_x,))
    y = models.FloatField(blank=False, validators=(validator_y,))
    search_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.city_name
