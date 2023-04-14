from math import remainder
from django.db import models
from django.forms import BooleanField
from django.contrib.auth.models import User
import datetime

# Create your models here.

class Donor(models.Model):
    DonorID = models.AutoField(primary_key=True)
    FullName = models.CharField(max_length=100)
    FirstName = models.CharField(max_length=100)
    LastName = models.CharField(max_length=100)
    Email = models.CharField(max_length=254)
    Address1 = models.CharField(max_length=500, blank=True, null=True)
    Address2 = models.CharField(max_length=500, blank=True, null=True)
    Address3 = models.CharField(max_length=500, blank=True, null=True)
    PostCode = models.CharField(max_length=12, blank=True, null=True)
    DonorType = models.CharField(max_length=100, blank=True, null=True)
    Notes = models.CharField(max_length=1000, blank=True, null=True)
    Phone = models.CharField(max_length=500, blank=True, null=True)
    InvolveNo = models.PositiveSmallIntegerField(default=0)
    Volunteer = models.BooleanField(default=False)


class Collection(models.Model):
    CollectionID = models.AutoField(primary_key=True)
    CollectionDate = models.DateField()
    Type = models.CharField(max_length=100)
    TotalWeight = models.DecimalField(max_digits=6, decimal_places=2)
    TotalCost = models.DecimalField(max_digits=8, decimal_places=2)
    CollectionPhoto = models.CharField(max_length=100)
    CollectionSpreadsheet = models.CharField(max_length=100)
    CollectionStatus = models.CharField(default="PLANNED", max_length=100)

class Wholesale(models.Model):
    WholesaleID = models.AutoField(primary_key=True)
    TotalDonated = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    TotalSpent = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    Remainder = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    WholesaleReceipt = models.CharField(default="N/A", max_length=100)
    Notes = models.CharField(max_length=1000, blank=True, null=True)
    CollectionID = models.ForeignKey(Collection, on_delete=models.CASCADE)

class Participation(models.Model):
    ParticipationID = models.AutoField(primary_key=True)
    PaymentRecieved = models.BooleanField(default=False)
    DateRecieved = models.DateField(blank=True, null=True) 
    DonationType = models.CharField(default="0", max_length=100)
    TotalDonated = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    DropOffTime = models.CharField(default="N/A", max_length=100)
    Notes = models.CharField(max_length=1000, blank=True, null=True)
    DonorID = models.ForeignKey(Donor, on_delete=models.CASCADE)
    CollectionID = models.ForeignKey(Collection, on_delete=models.CASCADE)
    WholesaleID = models.ForeignKey(Wholesale, on_delete=models.CASCADE)
