# Generated by Django 2.2.4 on 2019-08-14 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='outpass',
            name='matter',
        ),
        migrations.RemoveField(
            model_name='outpass',
            name='outPassDate',
        ),
        migrations.AddField(
            model_name='outpass',
            name='addressWhileLeave',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='outpass',
            name='fromDate',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='outpass',
            name='no_of_days',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='outpass',
            name='purposeOfLeave',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='outpass',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='outpass',
            name='toDate',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
