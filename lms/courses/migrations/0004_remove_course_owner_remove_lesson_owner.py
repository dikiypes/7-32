# Generated by Django 5.0.2 on 2024-02-25 05:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_course_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='owner',
        ),
    ]
