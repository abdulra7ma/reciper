# Generated by Django 5.0.4 on 2024-05-05 02:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_useraccount_bio_useraccount_followers_count_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="useraccount",
            old_name="id",
            new_name="uuid",
        ),
    ]
