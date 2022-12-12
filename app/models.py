from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class appUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    image = models.FileField(upload_to='static/site-data/profile-pictures', blank=True)
    date_of_birth = models.DateField(default=timezone.now)
    joined_date = models.DateField(default=timezone.now)
    phone_number = models.CharField(max_length=15, blank=True)
    verification_code = models.CharField(max_length=5, default="no")
    blocked_status = models.BooleanField(default=False)
    tenant_status = models.BooleanField(default=False)
    landlord_status = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username
Statuses = (
    ('1','Pending'),
    ('2','Confirmed'),
    ('3', 'Cancelled')
)
class Room(models.Model):
    name = models.CharField(max_length=20, blank=True)
    location = models.TextField()
    facilities = models.TextField()
    price = models.IntegerField(null=False, default=0)
    photos = models.TextField()
    landlord = models.ForeignKey(appUser, on_delete=models.PROTECT)
    tenant = models.TextField(blank=True)
    status = models.TextField(default="Empty")
    def __str__(self):
        return str(self.landlord.user.username)

class Room_request(models.Model):
    from_user = models.ForeignKey(appUser, on_delete=models.PROTECT)
    requested_date = models.DateField(default=timezone.now)
    room_id = models.IntegerField(default=None)
    status = models.CharField(max_length=18, choices = Statuses, default=1, blank=False, null=False)
    
    def get_req_status(self):
        return str(Statuses[int(self.status)-1][1])

class SampleFile(models.Model):
    # files = models.FileField(upload_to='static/coffee_club/uploads/products')
    file_url = models.CharField(
        max_length=200, default="/static//app/uploads/")

    def __str__(self):
        return self.file_url