# Generated by Django 2.2.4 on 2019-08-18 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0016_registeredcolleges_pincode'),
    ]

    operations = [
        migrations.AddField(
            model_name='registeredcolleges',
            name='country',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
