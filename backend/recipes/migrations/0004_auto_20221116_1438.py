# Generated by Django 2.2.16 on 2022-11-16 11:38

import colorfield.fields
import django.core.validators
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0003_auto_20221116_1410"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tag",
            name="color",
            field=colorfield.fields.ColorField(
                default="#FFFFFF",
                image_field=None,
                max_length=10,
                samples=None,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Проверьте вводимый формат",
                        regex="^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$",
                    )
                ],
                verbose_name="HEX-код",
            ),
        ),
    ]