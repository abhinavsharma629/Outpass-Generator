# Generated by Django 2.2.4 on 2019-08-14 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0009_auto_20190815_0057'),
        ('warden', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='warden',
            name='student',
            field=models.ManyToManyField(blank=True, to='student.Student'),
        ),
    ]
