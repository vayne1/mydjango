# Generated by Django 2.0.4 on 2018-04-18 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0004_host_cloud'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='soft',
            field=models.CharField(max_length=512, null=True),
        ),
        migrations.AddField(
            model_name='host',
            name='user',
            field=models.CharField(max_length=128, null=True),
        ),
    ]