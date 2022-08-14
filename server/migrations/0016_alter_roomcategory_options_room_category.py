# Generated by Django 4.0.2 on 2022-08-11 20:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0015_roomcategory_alter_message_date_added_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='roomcategory',
            options={'verbose_name_plural': '4. Kategoriler'},
        ),
        migrations.AddField(
            model_name='room',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='server.roomcategory', verbose_name='Kategori Adı'),
        ),
    ]