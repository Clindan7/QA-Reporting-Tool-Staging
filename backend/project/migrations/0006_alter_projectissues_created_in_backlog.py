# Generated by Django 4.2.5 on 2023-11-09 07:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("project", "0005_projects_start_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="projectissues",
            name="created_in_backlog",
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
    ]
