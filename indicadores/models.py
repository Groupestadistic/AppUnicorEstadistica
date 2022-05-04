from django.db import models

# Create your models here.
class Register(models.Model):
    name = models.CharField("nombre", max_length=100, blank=False, null=True)