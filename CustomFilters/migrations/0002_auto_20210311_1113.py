# Generated by Django 3.1.5 on 2021-03-11 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CustomFilters', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customfilters',
            name='input_file',
            field=models.FileField(blank=True, null=True, upload_to='custom/input/images/'),
        ),
        migrations.AddField(
            model_name='customfilters',
            name='output_file',
            field=models.FileField(blank=True, null=True, upload_to='custom/output/images/'),
        ),
    ]
