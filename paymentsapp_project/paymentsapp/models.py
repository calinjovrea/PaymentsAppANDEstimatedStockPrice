from django.db import models

# Create your models here.
class Payment(models.Model):
	credit_card_number = models.CharField(max_length=16)
	card_holder = models.CharField(max_length=100)
	expiration_date = models.DateField()
	security_code = models.CharField(max_length=3)
	amount = models.DecimalField(max_digits = 10, decimal_places = 2)
