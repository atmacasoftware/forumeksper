# Generated by Django 4.1 on 2022-08-27 18:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forums', '0003_alter_forumcategory_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='forum',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='forums.forumcategory', verbose_name='Forum Kategorisi'),
        ),
        migrations.AlterField(
            model_name='forumcomment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='forum_comment', to='forums.forumcomment', verbose_name='Yoruma Yanıt'),
        ),
    ]
