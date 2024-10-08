# Generated by Django 5.1 on 2024-09-15 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_alter_passwordresettoken_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordresettoken',
            name='token',
            field=models.CharField(default='90544424b8434cf9a2140a128596fe20', max_length=64, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='department',
            field=models.CharField(blank=True, choices=[('Marine Engineering', 'Marine Engineering'), ('Nautical Science', 'Nautical Science'), ('Maritime Transport and Business Studies', 'Maritime Transport and Business Studies'), ('Computer Science', 'Computer Science'), ('Fisheries Technology', 'Fisheries Technology'), ('Mechanical Engineering', 'Mechanical Engineering'), ('Science Laboratory Technology', 'Science Laboratory Technology'), ('Industrial and Labour Relations', 'Industrial and Labour Relations'), ('Oceanography and Fisheries Science', 'Oceanography and Fisheries Science'), ('Hydrology and Water Resources Management', 'Hydrology and Water Resources Management'), ('MARITIME TRANSPORT AND BUSSINESS MANAGEMENT', 'MARITIME TRANSPORT AND BUSSINESS MANAGEMENT')], max_length=100, null=True),
        ),
    ]
