# Generated by Django 4.2.5 on 2023-11-12 17:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("report", "0009_bugsummary"),
    ]

    operations = [
        migrations.AddField(
            model_name="bugsummary",
            name="test_case_choice",
            field=models.CharField(max_length=50, null=True),
        ),
    ]
