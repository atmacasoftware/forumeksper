# Generated by Django 4.1 on 2022-08-10 16:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0012_alter_room_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='membership',
            options={'verbose_name_plural': '2. Kanal Üyeleri'},
        ),
        migrations.AlterModelOptions(
            name='room',
            options={'verbose_name_plural': '1. Kanallar'},
        ),
    ]
