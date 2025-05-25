from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_biens, name='list_biens'),
    path('bien/<int:pk>/', views.bien_detail, name='bien_detail'),
    path('bien/ajouter/', views.ajouter_bien, name='ajouter_bien'),
    path('bien/<int:pk>/modifier/', views.modifier_bien, name='modifier_bien'),
    path('bien/<int:pk>/supprimer/', views.supprimer_bien, name='supprimer_bien'),
    path('bien/<int:bien_id>/demander-bail/', views.demander_bail, name='demander_bail'),
    


    path('bails/', views.list_bails, name='list_bails'),
    path('bails/ajouter/', views.ajouter_bail, name='ajouter_bail'),
    path('bails/<int:pk>/supprimer/', views.supprimer_bail, name='supprimer_bail'),
    path('bail/<int:bail_id>/', views.detail_bail, name='detail_bail'),


    path('demandes/', views.demandes_recuees, name='demandes_recuees'),
    path('demande/<int:demande_id>/accepter/', views.accepter_demande, name='accepter_demande'),
    path('demande/<int:demande_id>/refuser/', views.refuser_demande, name='refuser_demande'),

    path('disponibles/', views.biens_disponibles, name='biens_disponibles'),

    path('mes-demandes/', views.mes_demandes_bail, name='mes_demandes_bail'),

    path('mes-baux/', views.mes_baux, name='mes_baux'),

    path('bail/<int:pk>/contrat/', views.contrat_pdf_xhtml, name='contrat_pdf'),

    path('bails/ajouter/<int:bien_id>/<int:locataire_id>/', views.ajouter_bail, name='ajouter_bail'),
    path('bails/<int:pk>/valider_proprio/', views.valider_bail_proprio, name='valider_bail_proprio'),

    path('bail/<int:bail_id>/payer/', views.payer_loyer, name='payer_loyer'),
    path('paiements/recus/', views.paiements_recus, name='paiements_recus'),
    path('paiement/<int:paiement_id>/valider/', views.valider_paiement, name='valider_paiement'),
    path('mes_paiements/', views.list_paiements, name='mes_paiements'),

    path('intervention/signalement/', views.signaler_intervention, name='signaler_intervention'),
    path('agent/dashboard/', views.dashboard_agent, name='dashboard_agent'),
    path('interventions/traiter/<int:intervention_id>/', views.traiter_intervention, name='traiter_intervention'),
    path('interventions-a-traiter/', views.interventions_a_traiter, name='interventions_a_traiter'),
    path('intervention/<int:pk>/valider/', views.valider_intervention, name='valider_intervention'),
    path('agent/intervention/<int:intervention_id>/refuser/', views.refuser_intervention, name='refuser_intervention'),
    path('interventions/mes/', views.mes_interventions, name='mes_interventions'),
]
