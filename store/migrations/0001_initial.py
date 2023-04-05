import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=200)),
                ('author', models.CharField(blank=True, max_length=200)),
                ('isbn', models.CharField(default='NULL', max_length=30)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('price', models.IntegerField(default=0)),
                ('image', models.FileField(default='NULL', max_length=1000, upload_to='')),
                ('rating', models.FloatField(default=0)),
                ('volume', models.IntegerField(default=0)),
                ('description', models.TextField(default='Без описания', max_length=4000)),
                ('publisher', models.CharField(default='NULL', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('section', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(db_index=True, max_length=100, unique=True)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=20, validators=[django.core.validators.MinLengthValidator(5)])),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, max_length=500)),
                ('rating_review', models.FloatField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.user')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('number', models.AutoField(primary_key=True, serialize=False, validators=[django.core.validators.MinValueValidator(100)])),
                ('book', models.ManyToManyField(to='store.Book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.user')),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=16)),
                ('date_month', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)])),
                ('date_year', models.IntegerField(validators=[django.core.validators.MinValueValidator(2023), django.core.validators.MaxValueValidator(2028)])),
                ('last_name', models.CharField(max_length=20)),
                ('cvv', models.IntegerField(validators=[django.core.validators.MinValueValidator(3), django.core.validators.MaxValueValidator(3)])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='store.user')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.category'),
        ),
    ]