# Generated by Django 4.1.7 on 2023-03-24 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bleague_analysis', '0002_remove_team_id_remove_team_test_team_bleague_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='location',
            field=models.CharField(default='unknown', max_length=50),
        ),
    ]
