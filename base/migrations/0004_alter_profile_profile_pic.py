# Generated by Django 5.0.3 on 2024-06-05 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_profile_profile_pic_alter_profile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to='static/images/profile_pic'),
        ),
    ]
