# Generated by Django 2.1 on 2018-09-10 08:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SysMGR', '0003_loginfo_messgeinfo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messgeinfo',
            name='note',
        ),
        migrations.RemoveField(
            model_name='messgeinfo',
            name='url',
        ),
    ]