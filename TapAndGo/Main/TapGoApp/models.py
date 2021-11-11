from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from .utils import get_random_code, get_random_code_card
from django.template.defaultfilters import slugify
from PIL import Image
from django.shortcuts import reverse

# Create your models here.
class NationalId(models.Model):
    firstname = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    famName = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    dateofbirth = models.DateField()
    phone = models.CharField(max_length=15)
    fathername = models.CharField(max_length=100)
    mothername = models.CharField(max_length=100)
    id_num = models.SlugField(default=str(get_random_code()))

    def __str__(self):
        return f'{self.firstname} {self.famName}'

    __initial_first_name = None
    __initial_last_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initial_first_name = self.firstname
        self.__initial_last_name = self.name
    def save(self, *args, **kwargs):
        ex = False
        to_slug = self.id_num
        if self.firstname != self.__initial_first_name or self.name!= self.__initial_last_name or self.id_num=="":
            if self.firstname  and self.name:
                to_slug = slugify(str(get_random_code()))
                ex = NationalId.objects.filter(id_num=to_slug).exists()
                while ex:
                    to_slug = slugify(to_slug + " " + str(get_random_code()))
                    ex = NationalId.objects.filter(id_num=to_slug).exists()
            else:
                to_slug = str(self.user)
        self.slug = to_slug

        return super().save(*args, **kwargs)



HEALTH_CHOICE = {
    ('Vaccinated', 'Vaccinated'),
    ('Unvaccinated', 'Unvaccinated'),
    ('Positive', 'Positive')
}
 

class HealthReport(models.Model):
    citizen = models.ForeignKey(NationalId, on_delete=models.CASCADE, related_name='cit_health')
    report = models.CharField(choices=HEALTH_CHOICE, default='Not reported', max_length=12)

    def __str__(self):
        return f'{self.citizen}'


class PersonnalizedAccount(AbstractUser):
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

CARD_TYPE = {
    ('online', 'online'),
    ('blocked', 'blocked'),
    ('pending', 'pending')
 
}  
class Card(models.Model):
    cardnum = models.CharField(max_length=20)
    status = models.CharField(choices=CARD_TYPE, max_length=7, default='pending')
    balance = models.FloatField(default=0.0)
    position = models.BooleanField(default=False)
    transaction = models.FloatField(default=0.0)

    def __str__(self):
        return f'{self.cardnum}'

    @property
    def get_total(self):
        total = self.transaction
        return total

    @property
    def get_transaction_total(self):
        total = Card.objects.filter().all()
        totals = sum([item.get_total for item in total])
        return totals


PROFILE_TYPE = {
    ('Admin', 'Admin'),
    ('Agent', 'Agent'),
    ('Driver', 'Driver'),
    ('Passenger', 'Passenger')
}
class Profile(models.Model):
    account = models.OneToOneField(PersonnalizedAccount, on_delete=models.CASCADE, related_name='perso_account')
    health = models.ForeignKey(HealthReport, on_delete=models.CASCADE, related_name='health_account')
    typeUser = models.CharField(choices=PROFILE_TYPE, max_length=9, default='Passenger')
    cardNum = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='card_account')
    picture = models.ImageField(upload_to="images/", default='images/defaultUser.png', verbose_name='Profile picture')

    def __str__(self):
        return f'{self.health.citizen}'

    def get_absolute_url(self):
            return reverse("user_info", kwargs={"cardNum": self.cardNum.cardnum})
            
    def save(self, *args, **kwargs):
        img = Image.open(self.picture.path)

        if img.height > 900 or img.width > 900:
            output_size = (850,850)
            img.thumbnail(output_size)
            img.save(self.picture.path)

        super().save(*args, **kwargs)

class Cash(models.Model):
    account = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='cash_account')
    balance = models.FloatField(default=0.0)
    transaction = models.SlugField(default=str(get_random_code_card()))

    def __str__(self):
        return self.balance


ROAD_NUM = {
    ('301', '301'),
    ('303', '303'),
    ('311', '311'),
    ('313', '313')
}
class Road(models.Model):
    roadNum = models.CharField(choices=ROAD_NUM, max_length=5, default='301')
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.description

class BusStation(models.Model):
    num = models.CharField(max_length=5)
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.description

class Bus(models.Model):
    platenum = models.CharField(max_length=20)
    mark = models.CharField(max_length=20)
    sitNum = models.IntegerField(default=40)
    sitAvailable = models.IntegerField(default=0)
    affectRoad = models.ForeignKey(Road, on_delete=models.CASCADE, related_name='bus_road')
    affectStation = models.ForeignKey(BusStation, on_delete=models.CASCADE, related_name='bus_station')
    affectDriver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='driver_bus')

    def __str__(self):
        return f'{self.mark} {self.platenum}'

