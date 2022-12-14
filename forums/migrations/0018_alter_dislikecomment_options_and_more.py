# Generated by Django 4.1 on 2022-08-29 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forums', '0017_likecomment_dislikecomment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dislikecomment',
            options={'verbose_name_plural': '5.4 Forum Beğenmemeleri'},
        ),
        migrations.AlterModelOptions(
            name='likecomment',
            options={'verbose_name_plural': '5.3 Yorum Beğenmeleri'},
        ),
        migrations.AddField(
            model_name='dislikecomment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='dislikeforum',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='likecomment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='likeforum',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='dislikecomment',
            name='ip',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='dislikecomment',
            name='is_liked',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='likecomment',
            name='ip',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='likecomment',
            name='is_liked',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
