# Generated by Django 2.2.4 on 2019-08-20 20:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0019_auto_20190819_2237'),
    ]

    operations = [
        migrations.AddField(
            model_name='requests',
            name='college',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student.RegisteredColleges'),
        ),
    ]
