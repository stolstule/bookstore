# Generated by Django 3.2.12 on 2023-05-22 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_auto_20230521_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='/static/store/img/user.png', upload_to='profile_pics'),
        ),
    ]