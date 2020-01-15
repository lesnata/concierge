from django.db import models

# Create your models here.
from django.db.models import DO_NOTHING


def datetime_update(timespec='seconds'):
    return datetime.utcnow().isoformat(timespec=timespec)


class Tenant(models.Model):
    """
    Room's owner/tenant
    """
    first_name = models.CharField(
        'First name',
        max_length=250,
    )
    last_name = models.CharField(
        'Last name',
        max_length=250,
    )
    date_of_birth = models.DateField(
        blank=True,
        null=True,
        db_index=True,
    )
    phone = models.CharField(
        'Phone num',
        max_length=20,
        blank=True,
        null=True,
    )
    # photo = models.ImageField(
    #     'Photo',
    #     upload_to='tenant',
    #     help_text='Photo of the tenant',
    #     null=True,
    #     blank=True
    # )
    notes = models.TextField(
        blank=True,
        null=True,
    )

    @property
    def fullname(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.fullname

    class Meta:
        ordering = ['first_name', 'last_name']
        indexes = [
            models.Index(fields=['first_name', 'last_name']),
        ]


class Room(models.Model):
    number = models.IntegerField(blank=True, null=True)
    max_guests = models.IntegerField(blank=True, null=True)
    owner = models.ForeignKey(Tenant, on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(max_length=10, default='Free')


class Journal(models.Model):
    room_number = models.ForeignKey(Room, on_delete=DO_NOTHING, blank=True, null=True)
    tenant_id = models.ForeignKey(Tenant, on_delete=models.DO_NOTHING)
    guests = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    key_out_date = models.DateTimeField(blank=True, null=True)
    key_in_date = models.DateTimeField(db_index=True)
    is_kept = models.BooleanField()

    def __str__(self):
        return f'{self.room_number}, {self.key_in_date}, {self.key_out_date}, {self.guests}'

    def save(self, *args, **kwargs):
        room_number = self.room_number
        max_guests = room_number.max_guests
        if max_guests and self.guests > max_guests:
            raise ValueError(f'Maximal number of guests for this room is'
                             f'{max_guests}')
        elif self.is_kept and self.tenant_id:
            self.is_kept = False
            self.key_in_date = datetime_update()
            room_number.status = 'Busy'
            room_number.tenant = self.tenant_id
            room_number.save()
        else:
            self.key_is_kept = True
            self.key_is_back = datetime_update()
            self.key_on_hands = None
            room_number.status = 'free'
            room_number.tenant = self.tenant_id
            room_number.save()

        super().save(*args, **kwargs)








