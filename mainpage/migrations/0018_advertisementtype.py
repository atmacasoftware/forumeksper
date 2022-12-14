# Generated by Django 4.0.2 on 2022-09-26 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0017_adscategory_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdvertisementType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Kategori Adı')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(editable=False, null=True, unique=True)),
            ],
            options={
                'verbose_name_plural': '7.1. Reklam Kategorileri',
                'ordering': ['name'],
            },
        ),
    ]
