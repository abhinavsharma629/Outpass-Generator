# Generated by Django 2.2.4 on 2019-08-14 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_registeredcolleges_student'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='isVerfified',
            new_name='isVerified',
        ),
    ]