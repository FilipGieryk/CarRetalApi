# Generated by Django 4.2.5 on 2023-10-09 15:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rentACar', '0004_alter_review_rental'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rental',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='rentACar.rental'),
        ),
    ]