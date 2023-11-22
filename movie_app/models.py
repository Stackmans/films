from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class Actor(models.Model):
    MALE = 'M'
    FEMALE = 'F'

    SEX = [
        (MALE, 'Чоловік'),
        (FEMALE, 'Жінка'),
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    sex = models.CharField(max_length=1, choices=SEX, default=MALE)

    def __str__(self):
        if self.sex == self.MALE:
            return f'Актор: {self.first_name} {self.last_name}'
        else:
            return f'Акторка: {self.first_name} {self.last_name}'


class Director(models.Model):
    director_email = models.EmailField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Movie(models.Model):
    EUR = 'EUR'
    USD = 'USD'
    UAH = 'UAH'

    currency_choices = [
        (EUR, 'EUR'),
        (USD, 'USD'),
        (UAH, 'UAH'),
    ]

    name = models.CharField(max_length=40)  # len str not more 40
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])  # int

    year = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1888), MaxValueValidator(2023)])
    budget = models.IntegerField(default=1000, validators=[MinValueValidator(1)])  # int

    currency = models.CharField(max_length=3, choices=currency_choices, default='USD')
    slug = models.SlugField(default='', null=False, max_length=255, unique=True)

    director = models.ForeignKey(Director, on_delete=models.CASCADE, null=True)
    actors = models.ManyToManyField(Actor)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Movie, self).save(*args, **kwargs)

    def get_url(self):
        return reverse('movie-detail', args=[self.slug])

    def __str__(self):
        return f'{self.name} - {self.rating}%'
