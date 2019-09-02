# Generated by Django 2.2.4 on 2019-08-14 19:23

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('student', '0008_auto_20190815_0023'),
        ('commonPanel', '0004_auto_20190815_0019'),
    ]

    operations = [
        migrations.CreateModel(
            name='Warden',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(blank=True, max_length=50, null=True)),
                ('hostels', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, null=True, size=None)),
                ('contact_no', phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='Contact phone number', max_length=128, null=True, region=None)),
                ('isVerified', models.BooleanField(default=False)),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.RegisteredColleges')),
                ('warden', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='warden_name', to='commonPanel.UserDetails')),
            ],
        ),
    ]