# Generated by Django 2.2.16 on 2022-11-19 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_auto_20221116_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientinrecipe',
            name='amount',
            field=models.PositiveSmallIntegerField(verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveSmallIntegerField(verbose_name='Время приготовления'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='recipes/', verbose_name='Изображение'),
        ),
    ]