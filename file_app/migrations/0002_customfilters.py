# Generated by Django 3.1.5 on 2021-03-09 14:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('file_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomFilters',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('bg_image_1', models.ImageField(blank=True, null=True, upload_to='custom/images/')),
                ('bg_image_2', models.ImageField(blank=True, null=True, upload_to='custom/images/')),
                ('bg_image_3', models.ImageField(blank=True, null=True, upload_to='custom/images/')),
                ('type', models.CharField(choices=[('FILTER', 'filter'), ('FILTER_MOTIVATION', 'filter_motivation'), ('GIF', 'gif'), ('SHINEFILTER', 'shinefilter'), ('ROTATE', 'rotate'), ('CARTOON', 'cartoon'), ('NEWS_PAPER', 'news_paper'), ('RED_BLUE', 'red_blue'), ('SHAKING', 'shaking'), ('TILES', 'tiles'), ('CLOTH_COLOR_FILTER', 'cloth_color_filter'), ('SMOKE_FILTER', 'smoke_filter'), ('CARTOON_TEAR', 'cartoon_tear')], max_length=150)),
                ('file', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='file_app.file')),
            ],
        ),
    ]
