# Generated by Django 2.2.4 on 2019-08-14 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0006_auto_20190815_0016'),
    ]

    operations = [
        migrations.AddField(
            model_name='registeredcolleges',
            name='logo',
            field=models.FileField(blank=True, null=True, upload_to='College Logos'),
        ),
    ]
