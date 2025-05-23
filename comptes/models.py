from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLES = [
        ('admin', 'Administrateur'),
        ('proprietaire', 'Propriétaire'),
        ('locataire', 'Locataire'),
        ('agent', 'Agent'),
    ]
    role = models.CharField(max_length=20, choices=ROLES)
    
    def __str__(self):
        return f"{self.username} ({self.role})"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


