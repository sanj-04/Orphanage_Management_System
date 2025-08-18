from django.db import models
from django.contrib.auth.models import User

class Child(models.Model):
    STATUS_CHOICES = [
        ("Available", "Available"),
        ("Pending", "Pending"),
        ("Adopted", "Adopted"),
    ]
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to="children/")
    health = models.TextField()
    background = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Available")

    def __str__(self):
        return self.name


class Registration(models.Model):
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)

    father_email = models.EmailField()
    mother_email = models.EmailField()

    father_phone = models.CharField(max_length=10)
    mother_phone = models.CharField(max_length=10)

    father_age = models.PositiveIntegerField(null=True, blank=True)
    mother_age = models.PositiveIntegerField(null=True, blank=True)

    father_aadhar = models.CharField(max_length=12)
    mother_aadhar = models.CharField(max_length=12)

    address = models.TextField()
    reason = models.TextField()
    document = models.FileField(upload_to='documents/')

    is_approved = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name="registration")
    password = models.CharField(max_length=100, blank=True)  # plain password only for email

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
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name="applications", null=True, blank=True)
    system_message = models.TextField(default="Adoption request submitted.")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")

    full_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    user_message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name or self.user.username} - {self.child.name} ({self.status})"


class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_id = models.CharField(max_length=100, blank=True, null=True)  # Transaction ID
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - ₹{self.amount}"