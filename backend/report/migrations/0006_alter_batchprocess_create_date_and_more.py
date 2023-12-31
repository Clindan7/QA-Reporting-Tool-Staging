# Generated by Django 4.2.5 on 2023-11-09 18:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("report", "0005_remove_batchprocess_batch_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="batchprocess",
            name="create_date",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name="batchprocess",
            name="update_date",
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name="subbatchprocess",
            name="create_date",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name="subbatchprocess",
            name="end_time",
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name="subbatchprocess",
            name="update_date",
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
