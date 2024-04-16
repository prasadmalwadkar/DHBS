from django.db import models

# Create your models here.
class booking(models.Model):
    booking_id = models.IntegerField(unique=True)
    guest_id = models.IntegerField()
    full_name = models.CharField(max_length=100)
    room_number = models.IntegerField()
    room_type = models.CharField(max_length=50)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Booking ID: {self.booking_id}, Guest ID: {self.guest_id}, Full Name: {self.full_name}"