# Generated by Django 4.1 on 2022-08-27 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forums', '0002_alter_forumcategory_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forumcategory',
            name='slug',
            field=models.SlugField(editable=False, null=True, unique=True),
        ),
    ]
