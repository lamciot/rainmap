from django.db import models

# Create your models here
class MuongXen(models.Model):
    date_time = models.DateTimeField()
    data = models.TextField()