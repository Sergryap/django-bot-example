# Generated by Django 3.1.2 on 2020-11-21 18:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_bot', '0026_auto_20201121_2100'),
    ]

    operations = [
        migrations.RenameField(
            model_name='player',
            old_name='success_attemps_curent_session',
            new_name='success_attempts_current_session',
        ),
    ]