# Generated by Django 4.1.1 on 2022-09-09 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_name',
            field=models.CharField(max_length=128, verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=164, unique=True, verbose_name='Url'),
        ),
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(max_length=164, unique=True, verbose_name='Url'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=128, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(max_length=164, unique=True, verbose_name='Url'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='tag_name',
            field=models.CharField(max_length=128, verbose_name='Тег'),
        ),
    ]
