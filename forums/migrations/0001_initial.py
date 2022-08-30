# Generated by Django 4.1 on 2022-08-27 17:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, null=True, verbose_name='Forum Başlığı')),
                ('content', models.TextField(null=True, verbose_name='Forum İçeriği')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(editable=False, unique=True)),
                ('status', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Oluşturan Kullanıcı')),
            ],
            options={
                'verbose_name_plural': '1. Forumlar',
            },
        ),
        migrations.CreateModel(
            name='ForumCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Forum Kategorisi')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('icon', models.CharField(max_length=100, verbose_name='İkon')),
                ('slug', models.SlugField(editable=False, unique=True)),
                ('status', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': '2. Forum Kategorileri',
            },
        ),
        migrations.CreateModel(
            name='ForumComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='Yorum')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('ip', models.CharField(blank=True, max_length=20)),
                ('status', models.BooleanField(default=True)),
                ('forum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forum_comment', to='forums.forum', verbose_name='İlgili Forum')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='forums.forumcomment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Yorum Yapan Kullanıcı')),
            ],
            options={
                'verbose_name_plural': '3. Forum Yorumları',
            },
        ),
    ]