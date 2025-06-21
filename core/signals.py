from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Reservation

@receiver(post_delete, sender=Reservation)
def release_room_on_delete(sender, instance, **kwargs):
    room = instance.room
    room.status = 'available'
    room.save()
