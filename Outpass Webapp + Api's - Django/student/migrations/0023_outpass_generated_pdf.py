# Generated by Django 2.2.4 on 2019-08-24 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0022_auto_20190821_0455'),
    ]

    operations = [
        migrations.AddField(
            model_name='outpass',
            name='generated_pdf',
            field=models.FileField(blank=True, null=True, upload_to="Generated Pdf's"),
        ),
    ]