# Generated by Django 4.1 on 2022-08-14 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0016_alter_roomcategory_options_room_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='file_type',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
