# Generated by Django 4.1.2 on 2023-01-27 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("FoodbankApp", "0018_donor_address3")]

    operations = [
        migrations.AddField(
            model_name="wholesale",
            name="Notes",
            field=models.CharField(blank=True, max_length=1000, null=True),
        )
    ]