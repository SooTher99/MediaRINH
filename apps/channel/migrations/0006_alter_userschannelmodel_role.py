# Generated by Django 4.1.5 on 2023-01-14 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0005_alter_channelsmodel_link_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userschannelmodel',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('moderator', 'Moderator'), ('user', 'User')], default='user', max_length=64, verbose_name='Роль'),
        ),
    ]
