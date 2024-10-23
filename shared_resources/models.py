from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    iso_code = models.CharField(max_length=25, unique=True)
    currecny = models.CharField(max_length=25)
    phone_code = models.CharField(max_length=25, unique=True)
    capital = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.ForeignKey(
        Country, related_name="states", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class CasteCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class University(models.Model):
    name = models.CharField(max_length=200, unique=True)
    state = models.ForeignKey(
        State, related_name="universities", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Specialization(models.Model):
    name = models.CharField(max_length=200, unique=True)
    course = models.ForeignKey(
        Course, related_name="specializations", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
