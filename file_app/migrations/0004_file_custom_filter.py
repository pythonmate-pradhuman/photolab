# Generated by Django 3.1.5 on 2021-03-10 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('file_app', '0003_auto_20210310_0740'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='custom_filter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='file_app.customfilters'),
        ),
    ]
