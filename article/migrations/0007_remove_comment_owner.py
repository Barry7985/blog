# Generated by Django 4.2 on 2024-09-09 21:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0006_alter_article_date_pub'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='owner',
        ),
    ]
