# Generated by Django 4.2 on 2024-09-09 14:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0004_alter_article_date_pub'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='date_pub',
            field=models.DateField(blank=True, default=django.utils.timezone.now),
        ),
    ]
