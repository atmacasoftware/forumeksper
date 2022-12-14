# Generated by Django 4.1 on 2022-08-27 18:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('survey', '0005_vote_is_answered'),
    ]

    operations = [
        migrations.AlterField(
            model_name='options',
            name='survey',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='option_survey', to='survey.survey', verbose_name='İlgili Anket'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Oluşturulma Tarihi'),
        ),
        migrations.AlterField(
            model_name='vote',
            name='answered_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answer_user', to=settings.AUTH_USER_MODEL, verbose_name='Cevap Veren Kullanıcı'),
        ),
        migrations.AlterField(
            model_name='vote',
            name='options',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vote_option', to='survey.options', verbose_name='Ankete Ait Seçenekler'),
        ),
        migrations.AlterField(
            model_name='vote',
            name='survey',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vote_survey', to='survey.survey', verbose_name='İlgili Anket'),
        ),
    ]
