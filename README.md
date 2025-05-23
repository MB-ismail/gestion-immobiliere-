# 🏠 Gestion Immobilière - Projet Django

Ce projet est une plateforme de gestion immobilière développée en Django.  
Il permet aux propriétaires de publier leurs biens, aux locataires de faire des demandes, et aux deux parties de signer un contrat de bail en ligne.

## 👨‍💻 Fonctions principales

- Authentification par rôle (propriétaire, locataire)
- Ajout, modification et suppression de biens
- Gestion des demandes de location
- Signature numérique du contrat de bail
- Génération PDF du contrat
- Tableau de bord personnalisé

## ⚙️ Technologies

- Django 5.x
- Bootstrap 5
- MySQL
- HTML / CSS / JS
- xhtml2pdf
- num2words

## 📦 Installation locale

```bash
git clone https://github.com/ton-utilisateur/gestion-immobiliere.git
cd gestion-immobiliere
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
