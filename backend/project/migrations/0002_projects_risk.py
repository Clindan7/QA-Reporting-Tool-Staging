# Generated by Django 4.2.2 on 2023-10-19 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='projects',
            name='risk',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
