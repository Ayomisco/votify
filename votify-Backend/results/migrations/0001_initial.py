# Generated by Django 5.1 on 2024-09-12 15:38

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('elections', '0007_candidate_votes_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_votes', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('election', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='result', to='elections.election')),
            ],
            options={
                'verbose_name': 'Result',
                'verbose_name_plural': 'Results',
            },
        ),
        migrations.CreateModel(
            name='Winner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('announced_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elections.candidate')),
                ('result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='winners', to='results.result')),
            ],
            options={
                'verbose_name': 'Winner',
                'verbose_name_plural': 'Winners',
            },
        ),
    ]
