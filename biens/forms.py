from django import forms
from .models import Bien
from .models import Bail

class BienForm(forms.ModelForm):
    class Meta:
        model = Bien
        fields = ['titre', 'description', 'adresse', 'surface', 'prix', 'statut', 'image', 'type']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class BailForm(forms.ModelForm):
    class Meta:
        model = Bail
        fields = [
            'bien',
            'locataire',
            'date_debut',
            'date_fin',
            'montant_loyer',
            'garantie',
            'adresse_locataire',
            'adresse_proprietaire'
        ]
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(BailForm, self).__init__(*args, **kwargs)
        # Afficher uniquement les biens libres
        self.fields['bien'].queryset = Bien.objects.filter(statut='libre')

