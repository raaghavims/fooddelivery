# Generated by Django 4.2.7 on 2023-12-20 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_userprofile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
