# Generated by Django 4.1 on 2022-08-27 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forums', '0006_alter_forum_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forum',
            name='slug',
            field=models.SlugField(editable=False),
        ),
    ]
