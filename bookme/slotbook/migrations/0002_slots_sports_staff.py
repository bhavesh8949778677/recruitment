# Generated by Django 4.0.4 on 2022-08-22 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slotbook', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='slots',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('days', models.CharField(max_length=64)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='sports',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sport', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=64)),
                ('password', models.CharField(max_length=64)),
                ('email', models.CharField(max_length=64)),
                ('role', models.CharField(max_length=64)),
            ],
        ),
    ]