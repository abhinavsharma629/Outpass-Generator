# Generated by Django 2.2.4 on 2019-08-14 18:46

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0005_auto_20190814_2302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registeredcolleges',
            name='contact_no',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='Contact phone number', max_length=128, region=None),
        ),
    ]