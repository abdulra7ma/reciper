# Generated by Django 5.0.4 on 2024-05-05 04:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0002_alter_file_name"),
        ("tips", "0002_favoritetip"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tip",
            name="image",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="tips", to="common.file"
            ),
        ),
    ]
