# Generated by Django 4.1 on 2022-08-10 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0004_room_banner_room_created_at_room_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='created_at',
            field=models.DateTimeField(editable=False, null=True, verbose_name='Oluşturulduğu Tarih'),
        ),
        migrations.AlterField(
            model_name='room',
            name='modified_at',
            field=models.DateTimeField(null=True, verbose_name='Güncellendiği Tarih'),
        ),
    ]
