# Generated by Django 5.2 on 2025-05-09 14:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biens', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='lease',
            name='property',
        ),
        migrations.RemoveField(
            model_name='lease',
            name='tenant',
        ),
        migrations.CreateModel(
            name='Bien',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('adresse', models.CharField(max_length=255)),
                ('surface', models.FloatField()),
                ('prix', models.DecimalField(decimal_places=2, max_digits=10)),
                ('statut', models.CharField(choices=[('libre', 'Libre'), ('loue', 'Loué')], default='libre', max_length=10)),
                ('image', models.ImageField(blank=True, null=True, upload_to='biens/')),
                ('proprietaire', models.ForeignKey(limit_choices_to={'role': 'proprietaire'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='biens.type')),
            ],
        ),
        migrations.CreateModel(
            name='Bail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_debut', models.DateField()),
                ('date_fin', models.DateField()),
                ('montant_loyer', models.DecimalField(decimal_places=2, max_digits=10)),
                ('locataire', models.ForeignKey(limit_choices_to={'role': 'locataire'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('bien', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='biens.bien')),
            ],
        ),
        migrations.DeleteModel(
            name='Property',
        ),
        migrations.DeleteModel(
            name='Lease',
        ),
        migrations.DeleteModel(
            name='Tenant',
        ),
    ]
