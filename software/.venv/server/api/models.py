from django.db import models

# Create your models here.
class Bet(models.Model):
  type = models.CharField(max_length=30)
  accuracy = models.DecimalField(decimal_places=2, max_digits=4)