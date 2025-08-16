from django.db import models
from django.contrib.auth.models import User
# myapp/models.py
from django.db import models
# Create your models here.
class Child(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to="children/")
    health = models.TextField()
    background = models.TextField()

    def __str__(self):
        return self.name
    



# Model for storing registration requests
class Registration(models.Model):
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    
    father_email = models.EmailField()
    mother_email = models.EmailField()
    
    father_phone = models.CharField(max_length=10)
    mother_phone = models.CharField(max_length=10)
    
    father_age = models.PositiveIntegerField(null=True, blank=True)
    mother_age = models.PositiveIntegerField()
    
    father_aadhar = models.CharField(max_length=12)
    mother_aadhar = models.CharField(max_length=12)
    
    address = models.TextField()
    reason = models.TextField()
    document = models.FileField(upload_to='documents/')
    
    is_approved = models.BooleanField(default=False)
    user_id = models.CharField(max_length=50, blank=True)
    password = models.CharField(max_length=100, blank=True)

    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.father_name} & {self.mother_name} - {self.father_email}"




class AdoptionApplication(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    child = models.ForeignKey(
        Child,
        on_delete=models.CASCADE,
        related_name="applications",
        null=True,  # allow nullable for migration
        blank=True
    )
    system_message = models.TextField(default="Adoption request submitted.")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    user_message = models.TextField(blank=True, null=True)  # Message written by user
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.child.name} ({self.status})"






















# class AdoptionRequest(models.Model):
#     father_name = models.CharField(max_length=100, null=True, blank=True)
#     father_email = models.EmailField(null=True, blank=True)
#     father_phone = models.CharField(max_length=15, null=True, blank=True)
#     father_aadhar = models.CharField(max_length=12, null=True, blank=True)
#     father_age = models.IntegerField(null=True, blank=True)

#     mother_name = models.CharField(max_length=100, null=True, blank=True)
#     mother_email = models.EmailField(null=True, blank=True)
#     mother_phone = models.CharField(max_length=15, null=True, blank=True)
#     mother_aadhar = models.CharField(max_length=12, null=True, blank=True)
#     mother_age = models.IntegerField(null=True, blank=True)

#     address = models.TextField(null=True, blank=True)
#     reason = models.TextField(null=True, blank=True)
#     document = models.FileField(upload_to='documents/', null=True, blank=True)
    
#     is_approved = models.BooleanField(default=False )
#     username = models.CharField(max_length=50, blank=True, null=True)
#     password = models.CharField(max_length=100, blank=True, null=True)

#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.father_name} & {self.mother_name}"



# # Model for donation entries
# class Donation(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField()
#     phone = models.CharField(max_length=15)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     payment_done = models.BooleanField(default=False)

# # Model for children available for adoption
# class Child(models.Model):
#     name = models.CharField(max_length=100)
#     age = models.IntegerField()
#     sex = models.CharField(max_length=10)
#     description = models.TextField()
#     photo = models.ImageField(upload_to='children/')

# # Model for adoption application made by user
# class AdoptionApplication(models.Model):
#     user_email = models.EmailField()
#     child = models.ForeignKey(Child, on_delete=models.CASCADE)
#     status = models.CharField(max_length=20, default='Pending')  # Pending, Approved, Denied
#     paid = models.BooleanField(default=False)
