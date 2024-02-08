# Generated by Django 5.0.1 on 2024-02-08 16:24
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0005_dish_price"),
    ]

    operations = [
        migrations.AddField(
            model_name="driver",
            name="nationality",
            field=models.CharField(default="Poland", max_length=50),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name="DriverReview",
        ),
    ]
