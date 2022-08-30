# Generated by Django 4.1 on 2022-08-29 14:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forums', '0015_likeforum'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='likeforum',
            options={'verbose_name_plural': '5.1 Forum Beğenmeleri'},
        ),
        migrations.AlterField(
            model_name='likeforum',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='like_forum', to=settings.AUTH_USER_MODEL, verbose_name='Beğenen Kullanıcı'),
        ),
        migrations.CreateModel(
            name='DisLikeForum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(blank=True, max_length=20)),
                ('is_liked', models.BooleanField(default=False)),
                ('forum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dislike_forum', to='forums.forum', verbose_name='İlgili Forum')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dislike_forum', to=settings.AUTH_USER_MODEL, verbose_name='Beğenmeyen Kullanıcı')),
            ],
            options={
                'verbose_name_plural': '5.2 Forum Beğenmemeleri',
            },
        ),
    ]
