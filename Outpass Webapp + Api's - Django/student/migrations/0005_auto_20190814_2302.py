# Generated by Django 2.2.4 on 2019-08-14 17:32

from django.db import migrations
import phone_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0004_auto_20190814_2040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registeredcolleges',
            name='contact_no',
            field=phone_field.models.PhoneField(blank=True, help_text='Contact phone number', max_length=31),
        ),
    ]
