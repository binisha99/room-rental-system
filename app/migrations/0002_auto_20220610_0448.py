# Generated by Django 2.2.12 on 2022-06-10 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SampleFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_url', models.CharField(default='/static//app/uploads/', max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='room',
            name='status',
            field=models.TextField(default='Empty'),
        ),
    ]
