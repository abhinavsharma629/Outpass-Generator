# Generated by Django 2.2.4 on 2019-08-14 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0007_registeredcolleges_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='bed_no',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='branch',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='er_no',
            field=models.CharField(blank=True, max_length=7, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='hostel',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='room_no',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='year',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
