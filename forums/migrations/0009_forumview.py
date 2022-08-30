# Generated by Django 4.1 on 2022-08-28 08:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forums', '0008_alter_forum_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForumView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.CharField(max_length=100)),
                ('session', models.CharField(max_length=100)),
                ('forum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forum_views', to='forums.forum')),
            ],
        ),
    ]