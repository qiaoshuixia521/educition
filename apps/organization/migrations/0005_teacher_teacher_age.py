# Generated by Django 2.0.2 on 2019-01-26 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0004_teacher_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='teacher_age',
            field=models.IntegerField(default=25, verbose_name='年龄'),
        ),
    ]
