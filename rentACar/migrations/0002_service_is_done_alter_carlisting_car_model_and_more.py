# Generated by Django 4.2.5 on 2023-09-26 14:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rentACar', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='is_done',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='carlisting',
            name='car_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='car', to='rentACar.carmodel'),
        ),
        migrations.AlterField(
            model_name='review',
            name='reviewer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client_review', to=settings.AUTH_USER_MODEL),
        ),
    ]
