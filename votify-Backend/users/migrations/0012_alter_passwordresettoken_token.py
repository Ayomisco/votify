# Generated by Django 5.1 on 2024-09-14 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_passwordresettoken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordresettoken',
            name='token',
            field=models.CharField(default='bbfe578100c34937a1ed376b21d677d5', max_length=64, unique=True),
        ),
    ]
