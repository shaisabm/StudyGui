# Generated by Django 5.0.3 on 2024-06-05 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_alter_profile_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, default='static/images/profile_pic/default.jpg', null=True, upload_to='static/images/profile_pic'),
        ),
    ]
