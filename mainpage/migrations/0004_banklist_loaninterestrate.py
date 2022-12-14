# Generated by Django 4.1 on 2022-09-01 18:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0003_alter_citys_options_alter_worktype_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, null=True, verbose_name='Banka İsmi')),
                ('slug', models.SlugField(editable=False, null=True, unique=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='banka/logo', verbose_name='Banka Logosu')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'verbose_name_plural': '3. Banka İsimleri',
            },
        ),
        migrations.CreateModel(
            name='LoanInterestRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.FloatField(default=0.0, verbose_name='Kredi Oranı')),
                ('state', models.CharField(choices=[('Arttı', 'Arttı'), ('Azaldı', 'Azaldı')], max_length=50, verbose_name='Durum')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('bank', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainpage.banklist', verbose_name='Banka Adı')),
            ],
            options={
                'verbose_name_plural': '4. Kredi Faiz Oranları',
            },
        ),
    ]
