# Generated by Django 3.2.12 on 2023-04-16 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='store/static/store/img/user.png', upload_to='profile_pics'),
        ),
    ]
