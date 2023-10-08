from django.db import models
import pypjlink

# Create your models here.


class Projector(models.Model):
    name = models.CharField(max_length=40)
    address = models.CharField(max_length=15)

    def power_on(self):
        proj = pypjlink.Projector.from_address(self.address)
        proj.authenticate()
        proj.set_power('on')

    def power_off(self):
        proj = pypjlink.Projector.from_address(self.address)
        proj.authenticate()
        proj.set_power('off')
