# Generated by Django 4.2.4 on 2024-02-11 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('borrowed_book', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrowed_history',
            name='book_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
