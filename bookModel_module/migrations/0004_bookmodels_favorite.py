# Generated by Django 4.0.5 on 2022-10-28 21:13

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bookModel_module', '0003_bookmodels_offer'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookmodels',
            name='favorite',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
