from django.db import models
from comptes.models import CustomUser  # Utilisateur avec rôle


class Type(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Bien(models.Model):
    STATUT_CHOICES = [
        ('libre', 'Libre'),
        ('loue', 'Loué'),
    ]

    titre = models.CharField(max_length=200)
    description = models.TextField()
    adresse = models.CharField(max_length=255)
    surface = models.FloatField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='libre')
    image = models.ImageField(upload_to='biens/', blank=True, null=True)
    
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True)
    proprietaire = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'proprietaire'})

    def __str__(self):
        return self.titre

from .models import Bien 

class Bail(models.Model):
    bien = models.ForeignKey(Bien, on_delete=models.CASCADE)
    locataire = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'locataire'})
    date_debut = models.DateField()
    date_fin = models.DateField()
    montant_loyer = models.DecimalField(max_digits=10, decimal_places=2)
    garantie = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_creation = models.DateTimeField(auto_now_add=True)

    est_valide_proprio = models.BooleanField(default=False)
    est_valide_locataire = models.BooleanField(default=False)

    adresse_proprietaire = models.CharField(max_length=255, blank=True, null=True)
    adresse_locataire = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Bail de {self.locataire.username} pour {self.bien.titre}"

    def est_entierement_valide(self):
        return self.est_valide_proprio and self.est_valide_locataire

    def est_legalise(self):
        return self.est_valide_proprio and self.est_valide_locataire
    
    def save(self, *args, **kwargs):
        self.bien.statut = 'loue' 
        self.bien.save()
        super().save(*args, **kwargs)



class DemandeBail(models.Model):
    bien = models.ForeignKey(Bien, on_delete=models.CASCADE)
    locataire = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'locataire'})
    message = models.TextField(blank=True)
    date_demande = models.DateTimeField(auto_now_add=True)
    
    STATUT_CHOICES = [
        ('en attente', 'En attente'),
        ('accepte', 'Accepté'),
        ('refuse', 'Refusé'),
    ]
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en attente')

    def __str__(self):
        return f"{self.locataire} → {self.bien} [{self.statut}]"

import django.utils.timezone as timezone
class Paiement(models.Model):
    bail = models.ForeignKey(Bail, on_delete=models.CASCADE)
    locataire = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'locataire'})
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    mois_paye = models.CharField(max_length=20)  # ✅ ajoute ce champ
    date_paiement = models.DateTimeField(auto_now_add=True)
    valide = models.BooleanField(default=False)

    def _str_(self):
        return f"{self.locataire.get_full_name()} - {self.mois_paye} - {self.montant} DH"
    
class Intervention(models.Model):
    bail = models.ForeignKey(Bail, on_delete=models.CASCADE, related_name="interventions")
    description = models.TextField()
    date_signalement = models.DateTimeField(default=timezone.now)
    
    STATUT_CHOICES = [
        ('en attente', 'En attente'),
        ('en cours', 'En cours'),
        ('terminee', 'Terminée'),
        ('refusee', 'Refusée'),
    ]
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en attente')
    
    agent = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'agent'})
    
    def __str__(self):
        return f"{self.bail} - {self.statut}"

