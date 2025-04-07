from django.db import models

# Create your models here.
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import Company, Customer


class Service(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    description = models.TextField()
    price_hour = models.DecimalField(decimal_places=2, max_digits=100)
    rating = models.IntegerField(validators=[MinValueValidator(
        0), MaxValueValidator(5)], default=0)
    choices = (
        ('Air Conditioner', 'Air Conditioner'),
        ('Carpentry', 'Carpentry'),
        ('Electricity', 'Electricity'),
        ('Gardening', 'Gardening'),
        ('Home Machines', 'Home Machines'),
        ('House Keeping', 'House Keeping'),
        ('Interior Design', 'Interior Design'),
        ('Locks', 'Locks'),
        ('Painting', 'Painting'),
        ('Plumbing', 'Plumbing'),
        ('Water Heaters', 'Water Heaters'),
    )
    field = models.CharField(max_length=30, blank=False,
                             null=False, choices=choices)
    date = models.DateTimeField(auto_now=True, null=False)

    def __str__(self):
        return self.name


class ServiceHistory(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    service_time = models.DecimalField(decimal_places=1, max_digits=4)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    request_date = models.DateTimeField(auto_now_add=True)

    def calculate_price(self):
        """Calculate the total price based on service time and service price per hour"""
        return self.service_time * self.service.price_hour

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.calculate_price()
        super(ServiceHistory, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer.user.username} - {self.service.name} - {self.request_date.strftime('%Y-%m-%d')}"

    class Meta:
        ordering = ['-request_date']
        verbose_name_plural = "Service Histories"