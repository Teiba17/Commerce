# Generated by Django 4.1.7 on 2023-03-28 19:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_auctions_listing_current'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctions_listing',
            name='winner',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]