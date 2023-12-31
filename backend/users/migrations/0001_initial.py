# Generated by Django 4.2.5 on 2023-10-13 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Members',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('email', models.EmailField(max_length=100, null=True)),
                ('user_id', models.IntegerField(null=True)),
                ('backlog_user_id', models.CharField(max_length=50, null=True)),
                ('role_type', models.PositiveSmallIntegerField(choices=[(1, 'admin'), (2, 'project member')])),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'inactive'), (1, 'Active')])),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'members',
            },
        ),
    ]
