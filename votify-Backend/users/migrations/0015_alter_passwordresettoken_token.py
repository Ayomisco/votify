# Generated by Django 5.0.6 on 2024-09-28 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_alter_passwordresettoken_token_alter_user_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordresettoken',
            name='token',
            field=models.CharField(default='a21fd6b960dc4d5590b6fa06ace8dcd6', max_length=64, unique=True),
        ),
    ]
