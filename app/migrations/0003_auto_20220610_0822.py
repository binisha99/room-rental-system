# Generated by Django 2.2.12 on 2022-06-10 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20220610_0448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='tenant',
            field=models.TextField(),
        ),
    ]