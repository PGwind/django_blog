# Generated by Django 4.2.7 on 2023-11-14 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepost',
            name='body',
            field=models.TextField(default=''),
        ),
    ]
