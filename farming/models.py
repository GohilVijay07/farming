from django.db import models
from django.contrib.auth.models import User

# All 33 Districts of Gujarat, India
GUJARAT_DISTRICTS = [
    ('Ahmedabad', 'Ahmedabad'),
    ('Amreli', 'Amreli'),
    ('Anand', 'Anand'),
    ('Aravalli', 'Aravalli'),
    ('Banaskantha', 'Banaskantha'),
    ('Bharuch', 'Bharuch'),
    ('Bhavnagar', 'Bhavnagar'),
    ('Botad', 'Botad'),
    ('Chhota Udepur', 'Chhota Udepur'),
    ('Dahod', 'Dahod'),
    ('Dang', 'Dang'),
    ('Devbhumi Dwarka', 'Devbhumi Dwarka'),
    ('Gandhinagar', 'Gandhinagar'),
    ('Gir Somnath', 'Gir Somnath'),
    ('Jamnagar', 'Jamnagar'),
    ('Junagadh', 'Junagadh'),
    ('Kheda', 'Kheda'),
    ('Kutch', 'Kutch'),
    ('Mahisagar', 'Mahisagar'),
    ('Mehsana', 'Mehsana'),
    ('Morbi', 'Morbi'),
    ('Narmada', 'Narmada'),
    ('Navsari', 'Navsari'),
    ('Panchmahal', 'Panchmahal'),
    ('Patan', 'Patan'),
    ('Porbandar', 'Porbandar'),
    ('Rajkot', 'Rajkot'),
    ('Sabarkantha', 'Sabarkantha'),
    ('Surat', 'Surat'),
    ('Surendranagar', 'Surendranagar'),
    ('Tapi', 'Tapi'),
    ('Vadodara', 'Vadodara'),
    ('Valsad', 'Valsad'),
]

# 5 Agro-Climatic Regions of Gujarat
GUJARAT_REGIONS = [
    ('Saurashtra', 'Saurashtra (Rajkot, Junagadh, Amreli, Jamnagar, Bhavnagar, etc.)'),
    ('North Gujarat', 'North Gujarat (Banaskantha, Patan, Mehsana, Sabarkantha, Aravalli)'),
    ('Central Gujarat', 'Central Gujarat (Ahmedabad, Anand, Kheda, Vadodara, Panchmahal)'),
    ('South Gujarat', 'South Gujarat (Surat, Navsari, Valsad, Bharuch, Narmada, Tapi, Dang)'),
    ('Kutch', 'Kutch (Bhuj, Mandvi, Anjar, Rapar, Nakhatrana)'),
]


class FarmerProfile(models.Model):
    """
    Model representing extended profile details for a registered Gujarat farmer.
    Connected One-to-One with Django's built-in User model.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='farmer_profile')
    full_name = models.CharField(max_length=150, verbose_name="Full Name")
    phone = models.CharField(max_length=20, verbose_name="Phone Number")
    state = models.CharField(max_length=50, default='Gujarat', verbose_name="State")
    district = models.CharField(max_length=100, choices=GUJARAT_DISTRICTS, default='Ahmedabad', verbose_name="Gujarat District")
    taluka = models.CharField(max_length=100, blank=True, default='', verbose_name="Taluka / Block")
    farm_location = models.CharField(max_length=255, blank=True, default='', verbose_name="Village / Farm Location")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Farmer Profile"
        verbose_name_plural = "Farmer Profiles"
        ordering = ['-created_at']

    def get_location_display(self):
        """Returns clean formatted Gujarat location string."""
        parts = []
        if self.farm_location:
            parts.append(self.farm_location)
        if self.taluka:
            parts.append(self.taluka)
        if self.district:
            parts.append(self.district)
        parts.append(self.state or 'Gujarat')
        return ", ".join(parts)

    def __str__(self):
        loc = f"{self.taluka + ', ' if self.taluka else ''}{self.district}, Gujarat"
        return f"{self.full_name or self.user.username} ({loc})"


class Crop(models.Model):
    """
    Model representing crops managed by a Gujarat farmer.
    Connected Many-to-One with Django's built-in User model.
    """
    SEASON_CHOICES = [
        ('Kharif (Monsoon)', 'Kharif (Monsoon)'),
        ('Rabi (Winter)', 'Rabi (Winter)'),
        ('Zaid (Summer)', 'Zaid (Summer)'),
        ('Year-Round', 'Year-Round'),
    ]

    STATUS_CHOICES = [
        ('Planted', 'Planted'),
        ('Growing', 'Growing'),
        ('Ready to Harvest', 'Ready to Harvest'),
        ('Harvested', 'Harvested'),
    ]

    CROP_TYPE_CHOICES = [
        ('Cereal / Grain', 'Cereal / Grain (Wheat, Bajra, Maize, Rice)'),
        ('Cash Crop', 'Cash Crop (Cotton, Sugarcane, Tobacco)'),
        ('Oilseed', 'Oilseed (Groundnut, Castor, Sesame, Mustard)'),
        ('Spice', 'Spice / Seed (Cumin / Jeera, Fennel, Coriander)'),
        ('Pulse / Legume', 'Pulse / Legume (Chickpea, Tuver, Green Gram)'),
        ('Vegetable', 'Vegetable (Onion, Tomato, Potato, Chili)'),
        ('Fruit', 'Fruit (Mango, Pomegranate, Banana, Papaya)'),
        ('Fodder', 'Fodder'),
    ]

    farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='crops')
    crop_name = models.CharField(max_length=100, verbose_name="Crop Name")
    crop_type = models.CharField(max_length=50, choices=CROP_TYPE_CHOICES, default='Cash Crop', verbose_name="Crop Type")
    region = models.CharField(max_length=100, choices=GUJARAT_REGIONS, default='Saurashtra', verbose_name="Gujarat Agricultural Region")
    season = models.CharField(max_length=50, choices=SEASON_CHOICES, default='Kharif (Monsoon)', verbose_name="Season")
    farm_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Farm Area (Acres)", help_text="Total land area in acres")
    planting_date = models.DateField(verbose_name="Planting Date")
    expected_harvest_date = models.DateField(verbose_name="Expected Harvest Date")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Planted', verbose_name="Status")
    notes = models.TextField(blank=True, null=True, verbose_name="Notes & Instructions")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Crop"
        verbose_name_plural = "Crops"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.crop_name} - {self.status} ({self.farmer.username})"



class ContactMessage(models.Model):
    """
    Model representing messages submitted through the website Contact Us page.
    """
    name = models.CharField(max_length=150, verbose_name="Your Name")
    email = models.EmailField(verbose_name="Email Address")
    subject = models.CharField(max_length=200, verbose_name="Subject")
    message = models.TextField(verbose_name="Message Content")
    is_read = models.BooleanField(default=False, verbose_name="Is Read")
    read_at = models.DateTimeField(blank=True, null=True, verbose_name="Read At")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
        ordering = ['-created_at']

    def __str__(self):
        status = "Read" if self.is_read else "Unread"
        return f"{self.name} - {self.subject} [{status}] ({self.created_at.strftime('%Y-%m-%d %H:%M')})"


class FarmingTip(models.Model):
    """
    Model representing Gujarat farming tips and best practices manageable by Administrators.
    """
    CATEGORY_CHOICES = [
        ('Soil Preparation', 'Soil Preparation'),
        ('Irrigation', 'Irrigation & Drip Technology'),
        ('Water Management', 'Water Conservation & Management'),
        ('Fertilizer', 'Fertilizer & Soil Nutrition'),
        ('Pest Control', 'Pest & Disease Control'),
        ('Crop Rotation', 'Crop Rotation'),
        ('Organic Farming', 'Organic Farming (Prakrutik Kheti)'),
        ('Monsoon Farming', 'Monsoon Farming (Kharif Season)'),
        ('Rabi Farming', 'Winter Farming (Rabi Season)'),
        ('Kharif Farming', 'Kharif Crops Management'),
    ]

    title = models.CharField(max_length=200, verbose_name="Tip Title")
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='Soil Preparation', verbose_name="Category")
    description = models.TextField(verbose_name="Tip Description")
    level = models.CharField(max_length=50, default='Essential', verbose_name="Importance / Badge Level")
    icon = models.CharField(max_length=50, default='fa-seedling', verbose_name="FontAwesome Icon Class")
    image = models.ImageField(upload_to='tips/', blank=True, null=True, verbose_name="Tip Image (Optional)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Farming Tip"
        verbose_name_plural = "Farming Tips"
        ordering = ['category', '-created_at']

    def __str__(self):
        return f"[{self.category}] {self.title}"


class ActivityLog(models.Model):
    """
    Model recording important system and user events for Admin oversight.
    """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='activities', verbose_name="User")
    action = models.CharField(max_length=100, verbose_name="Action Type")
    details = models.TextField(blank=True, verbose_name="Event Details")
    icon = models.CharField(max_length=50, default='fa-circle-info', verbose_name="Icon Class")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Timestamp")

    class Meta:
        verbose_name = "Activity Log"
        verbose_name_plural = "Activity Logs"
        ordering = ['-created_at']

    def __str__(self):
        username = self.user.username if self.user else "System / Visitor"
        return f"{self.action} by {username} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class EmailVerificationOTP(models.Model):
    """
    Model storing cryptographically secure, hashed 6-digit OTPs for farmer email verification.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otp_records', verbose_name="User")
    otp_hash = models.CharField(max_length=255, verbose_name="Hashed OTP")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    expires_at = models.DateTimeField(verbose_name="Expires At")
    is_verified = models.BooleanField(default=False, verbose_name="Is Verified")
    attempts = models.PositiveIntegerField(default=0, verbose_name="Failed Attempts")

    class Meta:
        verbose_name = "Email Verification OTP"
        verbose_name_plural = "Email Verification OTPs"
        ordering = ['-created_at']

    def __str__(self):
        status = "Verified" if self.is_verified else ("Expired" if self.is_expired() else "Pending")
        return f"OTP for {self.user.username} [{status}] (Attempts: {self.attempts})"

    @staticmethod
    def generate_otp_code():
        """
        Generates a cryptographically secure 6-digit numeric OTP.
        """
        import secrets
        return f"{secrets.randbelow(1000000):06d}"

    def set_otp(self, raw_otp):
        """
        Hashes and stores the OTP securely using Django's password hasher.
        """
        from django.contrib.auth.hashers import make_password
        self.otp_hash = make_password(str(raw_otp).strip())

    def check_otp(self, raw_otp):
        """
        Validates raw 6-digit OTP against the stored hash.
        """
        from django.contrib.auth.hashers import check_password
        if not self.otp_hash or not raw_otp:
            return False
        return check_password(str(raw_otp).strip(), self.otp_hash)

    def is_expired(self):
        """
        Checks if the OTP has exceeded its 10-minute validity period.
        """
        from django.utils import timezone
        return timezone.now() > self.expires_at


class PasswordResetOTP(models.Model):
    """
    Model storing cryptographically secure, hashed 6-digit OTPs for user password reset requests.
    Completely separated from Registration EmailVerificationOTP.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_otps', verbose_name="User")
    otp_hash = models.CharField(max_length=255, verbose_name="Hashed OTP")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    expires_at = models.DateTimeField(verbose_name="Expires At")
    is_verified = models.BooleanField(default=False, verbose_name="Is Verified")
    attempts = models.PositiveIntegerField(default=0, verbose_name="Failed Attempts")

    class Meta:
        verbose_name = "Password Reset OTP"
        verbose_name_plural = "Password Reset OTPs"
        ordering = ['-created_at']

    def __str__(self):
        status = "Verified" if self.is_verified else ("Expired" if self.is_expired() else "Pending")
        return f"Password Reset OTP for {self.user.username} [{status}] (Attempts: {self.attempts})"

    @staticmethod
    def generate_otp_code():
        """
        Generates a cryptographically secure 6-digit numeric OTP.
        """
        import secrets
        return f"{secrets.randbelow(1000000):06d}"

    def set_otp(self, raw_otp):
        """
        Hashes and stores the OTP securely using Django's password hasher.
        """
        from django.contrib.auth.hashers import make_password
        self.otp_hash = make_password(str(raw_otp).strip())

    def check_otp(self, raw_otp):
        """
        Validates raw 6-digit OTP against the stored hash.
        """
        from django.contrib.auth.hashers import check_password
        if not self.otp_hash or not raw_otp:
            return False
        return check_password(str(raw_otp).strip(), self.otp_hash)

    def is_expired(self):
        """
        Checks if the OTP has exceeded its 10-minute validity period.
        """
        from django.utils import timezone
        return timezone.now() > self.expires_at


def log_activity(action, details="", user=None, icon=None):
    """
    Safely creates an activity audit record.
    """
    icon_map = {
        'User Registered': 'fa-user-plus',
        'Email Verified': 'fa-circle-check',
        'Password Reset Requested': 'fa-key',
        'Password Reset OTP Verified': 'fa-shield-check',
        'Password Reset Successful': 'fa-lock',
        'Crop Added': 'fa-seedling',
        'Crop Updated': 'fa-pen-to-square',
        'Crop Deleted': 'fa-trash-can',
        'Message Received': 'fa-envelope',
        'Message Read': 'fa-envelope-open-text',
        'Admin Login': 'fa-shield-halved',
        'User Status Changed': 'fa-user-gear',
        'User Deleted': 'fa-user-xmark',
        'Tip Added': 'fa-lightbulb',
        'Tip Updated': 'fa-pen',
        'Tip Deleted': 'fa-trash',
    }
    if not icon:
        icon = icon_map.get(action, 'fa-circle-info')
    try:
        return ActivityLog.objects.create(
            user=user,
            action=action,
            details=details,
            icon=icon
        )
    except Exception:
        return None


