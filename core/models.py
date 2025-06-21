from django.db import models
from django.utils import timezone
from django.templatetags.static import static

from django.db import models

class Room(models.Model):
    ROOM_TYPES = [
        ('standard', 'Standard'),
        ('deluxe', 'Deluxe'),
        ('suite', 'Suite'),
        ('family', 'Family'),
        ('executive', 'Executive'),
        ('presidential', 'Presidential'),
    ]

    FIXED_PRICES = {
        'standard': 100.00,
        'deluxe': 150.00,
        'suite': 200.00,
        'family': 180.00,
        'executive': 250.00,
        'presidential': 350.00,
    }

    number = models.CharField(max_length=10, unique=True)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    status = models.CharField(max_length=20, choices=[
        ('available', 'Available'), 
        ('occupied', 'Occupied'), 
        ('maintenance', 'Maintenance')
    ])
    image = models.ImageField(upload_to='rooms/', blank=True, null=True) 

    def save(self, *args, **kwargs):
        self.price = self.FIXED_PRICES.get(self.room_type, 0.00)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.number} - {self.get_room_type_display()}"
    
    @property
    def image_url(self):
        """
        Return the static URL for the room‐type image.
        Assumes you placed e.g. /static/room_images/standard.jpg, etc.
        """
        # Compose the filename: e.g. "room_images/standard.jpg"
        filename = f"room_images/{self.room_type}.jpg"
        return static(filename)
    
class RoomType(models.Model):
    code = models.CharField(max_length=20, unique=True)  # e.g. 'standard', 'deluxe'
    name = models.CharField(max_length=50)               # e.g. 'Standard Room'
    image = models.ImageField(upload_to='room_types/')
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Guest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    def __str__(self):
        return f"{self.name} ({self.email})" 

class Reservation(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey('WebsiteUser', on_delete=models.SET_NULL, null=True, blank=True)
    check_in = models.DateField()
    check_out = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.guest.name} - Room {self.room.number} ({self.check_in} to {self.check_out})"

class Payment(models.Model):
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_at = models.DateTimeField(default=timezone.now)  # or auto_now_add=True if not editable

    def __str__(self):
        return f"Payment for {self.reservation}"


class Staff(models.Model):
    ROLE_CHOICES = [
        ('manager', 'Manager'),
        ('receptionist', 'Receptionist'),
        ('housekeeping', 'Housekeeping'),
        ('security', 'Security'),
        ('maintenance', 'Maintenance'),
    ]

    name = models.CharField(max_length=100)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)  # ✅ now a select field
    hired_date = models.DateField()

    def __str__(self):
        return self.name

class Cleaning(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"Cleaning {self.room.number} - {self.date}"

class WebsiteUser(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)  # will store hashed password
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=30, default='user')
    last_login = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.username

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('souvenir', 'Souvenir'),
        ('addon', 'Room Add-On'),
        ('wellness', 'Wellness & Spa'),
        ('food', 'Food & Beverage'),
    ]

    nama_produk = models.CharField(max_length=100)
    deskripsi = models.TextField()
    harga = models.DecimalField(max_digits=10, decimal_places=2)
    kategori = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    tersedia = models.BooleanField(default=True)
    gambar = models.ImageField(upload_to='produk/', blank=True, null=True)

    def __str__(self):
        return self.nama_produk
    
class ProductOrder(models.Model):
    user = models.ForeignKey(WebsiteUser, on_delete=models.CASCADE)
    produk = models.ForeignKey(Product, on_delete=models.CASCADE)
    jumlah = models.PositiveIntegerField()
    total_harga = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total_harga = self.jumlah * self.produk.harga
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.produk.nama_produk} x{self.jumlah} by {self.user.username}"
    
class Dashboard(models.Model):
    user = models.OneToOneField(WebsiteUser, on_delete=models.CASCADE)
    last_booking = models.DateTimeField(null=True, blank=True)
    total_bookings = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Dashboard for {self.user.username}"
    
    from django.db import models
from core.models import WebsiteUser

class Invoice(models.Model):
    user = models.ForeignKey(WebsiteUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    billing_name = models.CharField(max_length=255)
    billing_email = models.EmailField()
    billing_address = models.TextField()
    payment_method = models.CharField(max_length=50)
    card_last_digits = models.CharField(max_length=4, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Invoice #{self.id} - {self.user.username}"


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percent = models.PositiveIntegerField(default=0)  # e.g. 10 for 10%
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} - {self.discount_percent}%"


class ContactMessage(models.Model):
    SUBJECT_CHOICES = [
        ('room_inquiry', 'Room Inquiry'),
        ('booking_issue', 'Booking Issue'),
        ('payment_question', 'Payment Question'),
        ('service_request', 'Service Request'),
        ('feedback', 'Feedback / Suggestions'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(WebsiteUser, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.get_subject_display()}"
    
class Destination(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=255)
    distance_km = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='destinations/', blank=True, null=True)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
from django.db import models
from core.models import Room, Staff

class MaintenanceRequest(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    issue = models.CharField(max_length=255)
    reported_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)
    date_reported = models.DateField(auto_now_add=True)
    resolved = models.BooleanField(default=False)
    resolution_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.room.number} - {self.issue[:30]}"
    
class ConfirmedProductOrder(models.Model):
    user = models.ForeignKey(WebsiteUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    confirmed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.nama_produk} × {self.quantity} by {self.user.username}"
    
# If WebsiteUser is your public user model:
class Feedback(models.Model):
    user = models.ForeignKey(WebsiteUser, on_delete=models.CASCADE, null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Room {self.room.number} - {self.rating}★"

class OccupancyRateSnapshot(models.Model):
    date = models.DateField(unique=True)
    occupied_rooms = models.PositiveIntegerField()
    available_rooms = models.PositiveIntegerField()
    maintenance_rooms = models.PositiveIntegerField()
    occupancy_rate = models.DecimalField(max_digits=5, decimal_places=2)  # e.g., 83.33%

    def __str__(self):
        return f"Snapshot for {self.date}"

class RoomServiceRequest(models.Model):
    SERVICE_CHOICES = [
        ('food', 'Food Delivery'),
        ('cleaning', 'Extra Cleaning'),
        ('towels', 'Fresh Towels'),
        ('amenities', 'Room Amenities'),
    ]
    guest = models.ForeignKey('WebsiteUser', on_delete=models.CASCADE)
    room = models.ForeignKey('Room', on_delete=models.SET_NULL, null=True)
    service_type = models.CharField(max_length=20, choices=SERVICE_CHOICES)
    requested_at = models.DateTimeField(auto_now_add=True)
    fulfilled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.service_type} for Room {self.room} by {self.guest.username}"


