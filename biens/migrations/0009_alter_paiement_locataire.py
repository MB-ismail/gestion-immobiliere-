# Generated by Django 5.2 on 2025-05-24 20:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biens', '0008_remove_paiement_est_valide_paiement_locataire_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='paiement',
            name='locataire',
            field=models.ForeignKey(limit_choices_to={'role': 'locataire'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
