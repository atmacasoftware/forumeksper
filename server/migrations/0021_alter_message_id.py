# Generated by Django 4.1 on 2022-08-24 11:30

from django.db import migrations, models
import server.models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0020_favouritemessage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='id',
            field=models.CharField(default=server.models.create_id, editable=False, max_length=255, primary_key=True, serialize=False),
        ),
    ]