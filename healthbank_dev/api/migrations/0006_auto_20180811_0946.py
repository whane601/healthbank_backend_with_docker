# Generated by Django 2.0.3 on 2018-08-11 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20180712_0733'),
    ]

    operations = [
        migrations.RenameField(
            model_name='health_info',
            old_name='blood_pressure',
            new_name='dia_blood_pressure',
        ),
        migrations.AddField(
            model_name='health_info',
            name='sys_blood_pressure',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
