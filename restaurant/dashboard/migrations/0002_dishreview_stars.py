# Generated by Django 5.0.1 on 2024-02-06 22:39
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="dishreview",
            name="stars",
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]