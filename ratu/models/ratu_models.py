from django.db import models

class Region(models.Model):
    name = models.CharField(max_length=30, unique=True)
    koatuu = models.CharField(max_length=10, unique=True, null=True)

class District(models.Model):
    EMPTY_FIELD = 'empty field'
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    koatuu = models.CharField(max_length=10, unique=True, null=True)

class City(models.Model):
    EMPTY_FIELD = 'empty field'
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    koatuu = models.CharField(max_length=10, unique=True, null=True)

class Citydistrict(models.Model):
    EMPTY_FIELD = 'empty field'
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    koatuu = models.CharField(max_length=10, unique=True, null=True)

class Street(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    citydistrict = models.ForeignKey(Citydistrict, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)