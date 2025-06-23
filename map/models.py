from django.db import models

# Create your models here
class MuongXen(models.Model):
    id = models.AutoField(primary_key=True)
    date_time = models.DateTimeField()
    data = models.TextField()
    st_quy_chau = models.IntegerField(null=True)
    st_muong_lat = models.IntegerField(null=True)
    st_xa_la = models.IntegerField(null=True)
    st_cua_dat = models.IntegerField(null=True)
    st_muong_xen = models.IntegerField(null=True)

class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField()
    password = models.CharField()
    
