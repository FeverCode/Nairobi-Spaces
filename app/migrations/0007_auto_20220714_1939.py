# Generated by Django 3.2 on 2022-07-14 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='subscribedusers',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
