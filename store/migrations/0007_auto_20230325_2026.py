from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_author_publisher'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Author',
        ),
        migrations.DeleteModel(
            name='Publisher',
        ),
    ]