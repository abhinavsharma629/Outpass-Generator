# Generated by Django 2.2.4 on 2019-08-14 17:32

from django.db import migrations
import phone_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('commonPanel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='phone',
            field=phone_field.models.PhoneField(blank=True, help_text='Contact phone number', max_length=31, null=True),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='phone1',
            field=phone_field.models.PhoneField(blank=True, help_text='Contact phone number', max_length=31, null=True),
        ),
    ]
