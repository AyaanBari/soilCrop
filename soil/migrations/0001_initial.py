# Generated by Django 5.1.7 on 2025-03-26 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Crop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('image', models.ImageField(upload_to='crop_images/')),
                ('description', models.TextField()),
                ('crop_type', models.CharField(max_length=100)),
                ('diseases', models.TextField()),
                ('companion', models.TextField(blank=True, null=True)),
                ('pests', models.TextField(blank=True, null=True)),
                ('fertilizer', models.TextField()),
                ('tips', models.TextField(blank=True, null=True)),
                ('spacing', models.TextField(blank=True, null=True)),
                ('watering', models.TextField(blank=True, null=True)),
                ('storage', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
