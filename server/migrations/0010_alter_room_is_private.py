# Generated by Django 4.1 on 2022-08-10 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0009_alter_room_modified_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='is_private',
            field=models.BooleanField(default=False, null=True, verbose_name='Gizli Mi?'),
        ),
    ]