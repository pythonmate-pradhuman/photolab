# Generated by Django 3.1.5 on 2021-03-12 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CustomFilters', '0004_auto_20210312_1003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customfilters',
            name='processed_image',
            field=models.FileField(blank=True, null=True, upload_to='custom/output/images/'),
        ),
    ]