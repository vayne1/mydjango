from django.db import models

# Create your models here.
class host(models.Model):
    instance_name = models.CharField(max_length=64)
    area = models.CharField(max_length=32)
    outside_ip = models.CharField(max_length=32)
    inside_ip = models.CharField(max_length=32)
    system = models.CharField(max_length=32)
    cpu_num = models.CharField(max_length=32)
    ram = models.CharField(max_length=32)
    bandwidth = models.CharField(max_length=32)
    risk = models.CharField(max_length=64)
    date = models.DateField(auto_now=True)
    cloud = models.ForeignKey(to='project',to_field='id',on_delete=models.DO_NOTHING)
    user = models.CharField(max_length=128,null=True)
    soft = models.CharField(max_length=512,null=True)

class project(models.Model):
    type = models.CharField(max_length=32)

    def __str__(self):
        return self.type


class account(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    status = models.BooleanField()

class all_account(models.Model):
    species = models.CharField(max_length=64)
    acc_mum = models.CharField(max_length=64)
    pwd = models.CharField(max_length=64)
