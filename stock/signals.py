from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Company, Threshold

@receiver(post_save, sender=Company)
def create_thresholds(sender, instance, created, **kwargs):
    if created:
        Threshold.objects.create(name='low_stock', value=10, company=instance)
        Threshold.objects.create(name='low_demand', value=5, company=instance)
        Threshold.objects.create(name='low_profit_margin', value=.01, company=instance)
        Threshold.objects.create(name='low_quantity', value=5, company=instance)
        Threshold.objects.create(name='low_rotation', value=2, company=instance)
        Threshold.objects.create(name='high_demand', value=8, company=instance)
        Threshold.objects.create(name='high_profit_margin', value=0.2, company=instance)
        Threshold.objects.create(name='high_rotation', value=10, company=instance)

@receiver(pre_delete, sender=Company)
def delete_thresholds(sender, instance, **kwargs):
    # récupérer les objets Threshold associés à l'objet Company qui va être supprimé
    thresholds = Threshold.objects.filter(company=instance)

    # supprimer les objets Threshold un par un
    for threshold in thresholds:
        threshold.delete()