# Generated by Django 4.2.2 on 2023-11-09 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0005_testcasedateandcount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testcasedateandcount',
            name='passed_test_case_count',
            field=models.IntegerField(null=True),
        ),
    ]
