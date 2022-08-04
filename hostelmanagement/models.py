from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

class CustomUser(AbstractUser):
    is_Owner = models.BooleanField("Owner",default=False)
    is_Student = models.BooleanField("Student",default=False)

HOSTEL_TYPES = (
    ('Mens Hostel','Mens Hostel'),
    ('Womens Hostel','Womens Hostel'),
)

FOOD_STATUS = (
    ('With Mess','With Mess'),
    ('Without Mess','Without Mess')
)

ROOM_CHOICES = (
    ('Available','Available'),
    ('Full','Full'),
    ('Not Available','Not Available')
)

STATUS_CHOICES = (
    ('Approved','Approved'),
    ('Rejected','Rejected'),
    ('On Hold','On Hold'),
    ('Suspended','Suspended')
)

class HostelDetail(models.Model):
    usr =models.ForeignKey(CustomUser,on_delete=models.CASCADE,default=None)
    notice_period = models.IntegerField()
    near_by = models.CharField(max_length=300)
    visitors_allowed = models.BooleanField(default=False)
    security_deposit = models.IntegerField()
    warden = models.BooleanField()
    restrictions = models.CharField(max_length=200)

    def __str__(self):
        return self.near_by

class Room(models.Model):
    room_number = models.IntegerField()
    hostel_name = models.CharField(max_length=100)
    usr = models.ForeignKey(CustomUser,on_delete=models.CASCADE,default=None)
    number_of_students = models.IntegerField()
    status = models.CharField(choices=ROOM_CHOICES ,max_length=100)
    room_imgs = models.ImageField(upload_to='rooms')
    room_cost = models.IntegerField()

    def __str__(self):
        return f"{ self.room_number }"

class OwnerDetail(models.Model):
    usr = models.ForeignKey(CustomUser,on_delete=models.CASCADE,default=None)
    name = models.CharField(max_length=150)
    profilePic = models.ImageField(upload_to='ownerimage')
    address = models.CharField(max_length=200)
    contact_num = PhoneNumberField(null=False, blank=False)

    def __str__(self):
        return f"{ self.usr }"

class Facilities(models.Model):
    facility = models.CharField(max_length=70)

    def __str__(self):
        return self.facility

class Hostel(models.Model):
    name = models.CharField(max_length=200)
    usr = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    location = models.CharField(max_length=200)
    zipcode = models.IntegerField()
    room = models.ManyToManyField(Room)
    type_of_hostel = models.CharField(choices=HOSTEL_TYPES, max_length=50)
    food_facility = models.CharField(choices=FOOD_STATUS,max_length=50, default="With Food",null=True)
    views = models.IntegerField(default=0)
    description = models.TextField(max_length=1000)
    details = models.ForeignKey(HostelDetail, on_delete=models.CASCADE,null=True)
    images = models.ImageField(upload_to='hostelimage')
    facilities = models.ManyToManyField(Facilities)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default='Not Approved.')

    def __str__(self):
        return f"{ self.name }"

class Reviews(models.Model):
    usr = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    text = models.TextField(max_length=400)
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE,related_name="reviews")

    def __str__(self):
        return f"{ self.text }"