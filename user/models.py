from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    is_service_provider=models.BooleanField(default=False)
    phone=models.CharField(max_length=15,blank=False,null=False)

    def __str__(self):
        return self.username
    

class Event(models.Model):
    service_provider=models.ForeignKey('service_provider.ServiceProvider',on_delete=models.CASCADE,limit_choices_to={'service_type':'event_planners'})
    name=models.CharField(max_length=200)
    description=models.TextField()
    image=models.ImageField()
    location=models.CharField(max_length=200)
    created_at=models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.name

class BookEvent(models.Model):
    ROLES=[
        ('pending','pending'),
        ('confirmed','confirmed'),
        ('cancelled','cancelled'),
    ]
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    event=models.ForeignKey(Event,on_delete=models.CASCADE)
    our_service = models.CharField(
        max_length=50,
        choices=[
            ('Venue', 'Venue'),
            ('Transportation', 'Transportation'),
            ('Catering', 'Catering'),
            ('Decorations', 'Decorations'),
            ('BridalGroom', 'BridalGroom'),
            ('Photography', 'Photography'),
        ]
    )
    status=models.CharField(max_length=20,choices=ROLES,default='pending')
    customize =models.TextField()
    reminder_sent=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking for {self.event.name} by {self.user.username}"
    
class ServiceAvailability(models.Model):
    service_type = models.CharField(
        max_length=50,
        choices=[
            ('Venue', 'Venue'),
            ('Transportation', 'Transportation'),
            ('Catering', 'Catering'),
            ('Decorations', 'Decorations'),
            ('BridalGroom', 'BridalGroom'),
            ('Photography', 'Photography')
        ]
    )
    service_id = models.PositiveIntegerField() 
    booked_date = models.DateField()

    def __str__(self):
        return f"{self.service_type} (ID: {self.service_id}) - {self.booked_date}"

    
class Venue(models.Model):
    provider = models.ForeignKey('service_provider.ServiceProvider', on_delete=models.CASCADE, related_name="venues",limit_choices_to={'service_type':'event_planners'})  # Service provider
    name = models.CharField(max_length=255)
    image=models.ImageField()
    location = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class VenueBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    event_date = models.DateField()
    venue_customize=models.CharField(max_length=20,choices=[('indoor','indoor'),('outdoor','outdoor'),('other','other')])
    status = models.CharField(
        max_length=20, 
        choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Completed', 'Completed')],
        default='Pending'
    )

    def __str__(self):
        return f"{self.user.username} - {self.venue.name} ({self.event_date})"
    
    
class TransportationService(models.Model):
    provider = models.ForeignKey('service_provider.ServiceProvider', on_delete=models.CASCADE, related_name="transport_services",limit_choices_to={'service_type':'transportation'})
    name=models.CharField(max_length=200)
    image=models.ImageField()
    desc=models.TextField()
    available = models.BooleanField(default=True)

class TransportationBooking(models.Model):
    ROLES=[
        ('A/C-Bus','A/C-Bus'),
        ('Non-A/C-Bus','Non-A/C-Bus'),
        ('Travaler','Traveler'),
        ('Permium-Cars','Permium-Cars'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(TransportationService, on_delete=models.CASCADE)
    vehicle_type = models.CharField(max_length=20,choices=ROLES)
    seats = models.CharField(max_length=20,choices=[('20','20'),('30','30'),('45','45')])
    event_date = models.DateField()
    rent_car=models.BooleanField(default=False)
    status = models.CharField(
        max_length=20, choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Completed', 'Completed')],
        default='Pending'
    )


class CateringService(models.Model):
    provider = models.ForeignKey('service_provider.ServiceProvider', on_delete=models.CASCADE, related_name="catering_services",limit_choices_to={'service_type':'catering'})
    menu_name = models.CharField(max_length=255)
    desc=models.TextField()
    images=models.ImageField()
    available = models.BooleanField(default=True)

class CateringBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(CateringService, on_delete=models.CASCADE)
    event_date = models.DateField()
    guests = models.PositiveIntegerField()
    customize_food=models.CharField(max_length=20,choices=[('non-veg','non-veg'),('veg','veg'),('north-indian','north-indian'),('desserts','desserts')])
    status = models.CharField(
        max_length=20, choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Completed', 'Completed')],
        default='Pending'
    )


class DecorationsService(models.Model):
    provider = models.ForeignKey('service_provider.ServiceProvider', on_delete=models.CASCADE, related_name="decorations_services",limit_choices_to={'service_type':'decoration'})
    name = models.CharField(max_length=255)
    theme_options = models.TextField()
    desc=models.TextField()
    image=models.ImageField()
    available = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class DecorationsBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(DecorationsService, on_delete=models.CASCADE)
    custom_service=models.TextField()
    event_date = models.DateField()
    status = models.CharField(
        max_length=20, choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Completed', 'Completed')],
        default='Pending'
    )

    def __str__(self):
        return f"{self.user.username} - {self.service.name} ({self.event_date})"



class PhotographyService(models.Model):
    provider = models.ForeignKey('service_provider.ServiceProvider', on_delete=models.CASCADE, related_name="photography_services")
    package_name = models.CharField(max_length=255)
    image=models.ImageField()
    desc=models.TextField()
    includes_video = models.BooleanField(default=False)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.package_name

class PhotographyBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(PhotographyService, on_delete=models.CASCADE)
    event_date = models.DateField()
    custom_service=models.TextField()
    status = models.CharField(
        max_length=20, choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Completed', 'Completed')],
        default='Pending'
    )

    def __str__(self):
        return f"{self.user.username} - {self.service.package_name} ({self.event_date})"



class BridalGroomService(models.Model):
    provider = models.ForeignKey('service_provider.ServiceProvider', on_delete=models.CASCADE, related_name="bridal_groom_services",limit_choices_to={'service_type':'bride_groom_service'})
    package_name = models.CharField(max_length=255)
    image=models.ImageField()
    desc=models.TextField()
    package_details = models.TextField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class BridalGroomServiceBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(BridalGroomService, on_delete=models.CASCADE)
    event_date = models.DateField()
    suggest_theme=models.TextField()
    status = models.CharField(
        max_length=20, choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Completed', 'Completed')],
        default='Pending'
    )

    def __str__(self):
        return f"{self.user.username} - {self.service.name} ({self.event_date})"
