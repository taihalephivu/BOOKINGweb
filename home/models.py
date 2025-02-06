from django.contrib.auth.models import User
from django.db import models
import uuid




class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4   , editable=False , primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering=['uid']

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.user.username
    
class Amenities(BaseModel):
    amenity_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.amenity_name

class Hotel(BaseModel):
    hotel_name = models.CharField(max_length=100)
    hotel_price = models.IntegerField()
    description = models.TextField()
    amenities = models.ManyToManyField(Amenities)
    room_count = models.IntegerField(default=10)
    
    def __str__(self) -> str:
        return self.hotel_name

class HotelImages(BaseModel):
    hotel = models.ForeignKey(Hotel, related_name="hotel_images", on_delete=models.CASCADE)
    images = models.ImageField(upload_to="hotels/", blank=True, null=True, default='hotels/')

class HotelBooking(BaseModel):
    hotel = models.ForeignKey(Hotel, related_name="hotel_bookings", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="user_bookings", on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    booking_type = models.CharField(max_length=100, choices=(
        ('Pre Paid', 'Pre Paid'),
        ('Post Paid', 'Post Paid')
    ))
    status = models.CharField(max_length=20, choices=(
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed')
    ), default='active')
    
    def __str__(self) -> str:
        return f'{self.hotel.hotel_name} - {self.user.username}'
    
    