# Generated by Django 2.0.4 on 2018-04-16 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='date',
            field=models.DateField(auto_now=True),
        ),
    ]
