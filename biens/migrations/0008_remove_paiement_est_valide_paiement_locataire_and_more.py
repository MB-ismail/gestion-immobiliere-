# Generated by Django 5.2 on 2025-05-24 20:07

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biens', '0007_paiement'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paiement',
            name='est_valide',
        ),
        migrations.AddField(
            model_name='paiement',
            name='locataire',
            field=models.ForeignKey(limit_choices_to={'role': 'locataire'}, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='paiement',
            name='bail',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='biens.bail'),
        ),
        migrations.AlterField(
            model_name='paiement',
            name='date_paiement',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
