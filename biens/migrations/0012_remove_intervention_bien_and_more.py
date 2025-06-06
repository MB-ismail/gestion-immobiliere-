# Generated by Django 5.2 on 2025-05-25 16:34

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biens', '0011_intervention'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='intervention',
            name='bien',
        ),
        migrations.RemoveField(
            model_name='intervention',
            name='locataire',
        ),
        migrations.AddField(
            model_name='intervention',
            name='bail',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='interventions', to='biens.bail'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='intervention',
            name='agent',
            field=models.ForeignKey(blank=True, limit_choices_to={'role': 'agent'}, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='intervention',
            name='date_signalement',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='intervention',
            name='statut',
            field=models.CharField(choices=[('en attente', 'En attente'), ('en cours', 'En cours'), ('terminee', 'Terminée'), ('refusee', 'Refusée')], default='en attente', max_length=20),
        ),
    ]
