# Generated by Django 2.2.4 on 2019-08-20 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warden', '0006_warden_id_card'),
    ]

    operations = [
        migrations.AddField(
            model_name='warden',
            name='signature',
            field=models.TextField(blank=True, null=True),
        ),
    ]