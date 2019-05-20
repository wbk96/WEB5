from django.db import models

# Create your models here.

class biaoti(models.Model):
    string=models.CharField(max_length=30,verbose_name='string')

    def __str__(self):
        return  self.string
class User(models.Model):
    name=models.CharField(max_length=20,verbose_name='name')
    pool=models.IntegerField(verbose_name='pool')
    string=models.ForeignKey(biaoti,on_delete=models.CASCADE)
    def __str__(self):
        return self.name

