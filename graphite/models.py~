from django.db import models

# Create your models here.
class users(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    api=models.CharField(max_length=30)
    vip=models.CharField(max_length=15)
    pip=models.CharField(max_length=15)
    def __unicode__(self):
	return self.name
