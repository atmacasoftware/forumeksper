# Generated by Django 4.1 on 2022-08-10 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0011_alter_room_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='name',
            field=models.CharField(max_length=255, null=True, verbose_name='Kanal Adı'),
        ),
    ]
