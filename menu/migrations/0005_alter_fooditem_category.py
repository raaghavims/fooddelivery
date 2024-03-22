# Generated by Django 4.2.7 on 2024-02-13 10:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("menu", "0004_alter_fooditem_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fooditem",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="fooditems",
                to="menu.category",
            ),
        ),
    ]