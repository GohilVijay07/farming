from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import FarmerProfile, Crop, ContactMessage, FarmingTip, GUJARAT_DISTRICTS, GUJARAT_REGIONS


class FarmerRegistrationForm(forms.Form):
    """
    Form for registering a new Gujarat farmer account and associated profile.
    """
    full_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your full name (e.g., Rajeshbhai Patel)',
            'id': 'reg_full_name'
        })
    )
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Choose a unique username',
            'id': 'reg_username'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'name@example.com',
            'id': 'reg_email'
        })
    )
    phone = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+91 98765 43210',
            'id': 'reg_phone'
        })
    )
    district = forms.ChoiceField(
        choices=GUJARAT_DISTRICTS,
        initial='Ahmedabad',
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'reg_district'
        })
    )
    taluka = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Taluka / Tehsil (e.g., Gondal, Sanand, Jetpur)',
            'id': 'reg_taluka'
        })
    )
    farm_location = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Village / Farm Name (e.g., Moti Marad Farm)',
            'id': 'reg_farm_location'
        })
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Create a secure password',
            'id': 'reg_password'
        })
    )
    confirm_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password',
            'id': 'reg_confirm_password'
        })
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError("This username is already taken. Please choose another one.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("An account with this email address already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match. Please verify and retype.")

        if password and len(password) < 6:
            self.add_error('password', "Password must be at least 6 characters long.")

        return cleaned_data

    def save(self):
        """Creates both User and FarmerProfile objects in database."""
        data = self.cleaned_data
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            first_name=data['full_name'].split()[0] if data['full_name'] else '',
            last_name=' '.join(data['full_name'].split()[1:]) if len(data['full_name'].split()) > 1 else ''
        )
        FarmerProfile.objects.create(
            user=user,
            full_name=data['full_name'],
            phone=data['phone'],
            state='Gujarat',
            district=data['district'],
            taluka=data.get('taluka', ''),
            farm_location=data['farm_location']
        )
        return user


class FarmerLoginForm(forms.Form):
    """
    Custom login form for farmer authentication.
    """
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username or email',
            'id': 'login_username',
            'autocomplete': 'username'
        })
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
            'id': 'login_password',
            'autocomplete': 'current-password'
        })
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'id': 'remember_me'
        })
    )


class FarmerProfileUpdateForm(forms.Form):
    """
    Form for updating Gujarat farmer profile details.
    """
    full_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'profile_full_name'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'profile_email'})
    )
    phone = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'profile_phone'})
    )
    district = forms.ChoiceField(
        choices=GUJARAT_DISTRICTS,
        required=True,
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'profile_district'})
    )
    taluka = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'profile_taluka', 'placeholder': 'Taluka / Tehsil'})
    )
    farm_location = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'profile_farm_location', 'placeholder': 'Village / Farm Name'})
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        profile = getattr(user, 'farmer_profile', None)
        if profile:
            self.fields['full_name'].initial = profile.full_name or user.get_full_name() or user.username
            self.fields['phone'].initial = profile.phone
            self.fields['district'].initial = profile.district or 'Ahmedabad'
            self.fields['taluka'].initial = profile.taluka
            self.fields['farm_location'].initial = profile.farm_location
        else:
            self.fields['full_name'].initial = user.get_full_name() or user.username
            self.fields['phone'].initial = ''
            self.fields['district'].initial = 'Ahmedabad'
            self.fields['taluka'].initial = ''
            self.fields['farm_location'].initial = ''
        self.fields['email'].initial = user.email

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exclude(pk=self.user.pk).exists():
            raise ValidationError("This email is already in use by another account.")
        return email

    def save(self):
        """Updates User and FarmerProfile objects."""
        data = self.cleaned_data
        self.user.email = data['email']
        parts = data['full_name'].split()
        self.user.first_name = parts[0] if parts else ''
        self.user.last_name = ' '.join(parts[1:]) if len(parts) > 1 else ''
        self.user.save()

        profile, created = FarmerProfile.objects.get_or_create(user=self.user)
        profile.full_name = data['full_name']
        profile.phone = data['phone']
        profile.state = 'Gujarat'
        profile.district = data['district']
        profile.taluka = data.get('taluka', '')
        profile.farm_location = data['farm_location']
        profile.save()
        return profile


class CropForm(forms.ModelForm):
    """
    ModelForm for Adding and Editing Gujarat Crop information.
    """
    class Meta:
        model = Crop
        fields = [
            'crop_name',
            'crop_type',
            'region',
            'season',
            'farm_area',
            'planting_date',
            'expected_harvest_date',
            'status',
            'notes',
        ]
        widgets = {
            'crop_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Cotton (કપાસ), Groundnut (મગફળી), Wheat (ઘઉં), Cumin (જીરું)',
                'id': 'crop_name'
            }),
            'crop_type': forms.Select(attrs={
                'class': 'form-select',
                'id': 'crop_type'
            }),
            'region': forms.Select(attrs={
                'class': 'form-select',
                'id': 'crop_region'
            }),
            'season': forms.Select(attrs={
                'class': 'form-select',
                'id': 'season'
            }),
            'farm_area': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 5.0 (in Acres)',
                'step': '0.01',
                'min': '0.01',
                'id': 'farm_area'
            }),
            'planting_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'id': 'planting_date'
            }),
            'expected_harvest_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'id': 'expected_harvest_date'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select',
                'id': 'status'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Add soil preparation notes, fertilizer schedule (DAP/Urea), micro-irrigation details, seed variety (e.g., BT Cotton, GG-20 Groundnut)...',
                'id': 'notes'
            }),
        }

    def clean_farm_area(self):
        farm_area = self.cleaned_data.get('farm_area')
        if farm_area is not None and farm_area <= 0:
            raise ValidationError("Farm area must be greater than zero.")
        return farm_area

    def clean(self):
        cleaned_data = super().clean()
        planting_date = cleaned_data.get('planting_date')
        expected_harvest_date = cleaned_data.get('expected_harvest_date')

        if planting_date and expected_harvest_date:
            if expected_harvest_date < planting_date:
                self.add_error('expected_harvest_date', "Expected harvest date cannot be earlier than planting date.")

        return cleaned_data


class ContactForm(forms.ModelForm):
    """
    Form for Contact Us inquiries.
    """
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name',
                'id': 'contact_name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address',
                'id': 'contact_email'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'What is this regarding?',
                'id': 'contact_subject'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Write your message or inquiry here...',
                'id': 'contact_message'
            }),
        }


class AdminLoginForm(forms.Form):
    """
    Dedicated Login Form for AgriConnect Administrators (Staff & Superusers).
    """
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'admin-form-input',
            'placeholder': 'Admin Username or Email',
            'id': 'admin_username',
            'autocomplete': 'username',
            'autofocus': True
        })
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'admin-form-input',
            'placeholder': 'Admin Password',
            'id': 'admin_password',
            'autocomplete': 'current-password'
        })
    )


class AdminUserEditForm(forms.Form):
    """
    Form allowing Administrators to update user details, Gujarat profile information, and account status.
    """
    full_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'admin-form-control', 'id': 'user_full_name'})
    )
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'admin-form-control', 'id': 'user_username'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'admin-form-control', 'id': 'user_email'})
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'admin-form-control', 'id': 'user_phone'})
    )
    district = forms.ChoiceField(
        choices=GUJARAT_DISTRICTS,
        required=True,
        widget=forms.Select(attrs={'class': 'admin-form-select', 'id': 'user_district'})
    )
    taluka = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'admin-form-control', 'id': 'user_taluka', 'placeholder': 'Taluka / Tehsil'})
    )
    farm_location = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'admin-form-control', 'id': 'user_farm_location', 'placeholder': 'Village / Farm Name'})
    )
    is_active = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'admin-checkbox', 'id': 'user_is_active'})
    )
    is_staff = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'admin-checkbox', 'id': 'user_is_staff'})
    )

    def __init__(self, target_user, *args, **kwargs):
        self.target_user = target_user
        super().__init__(*args, **kwargs)
        self.fields['username'].initial = target_user.username
        self.fields['email'].initial = target_user.email
        self.fields['is_active'].initial = target_user.is_active
        self.fields['is_staff'].initial = target_user.is_staff

        profile = getattr(target_user, 'farmer_profile', None)
        if profile:
            self.fields['full_name'].initial = profile.full_name
            self.fields['phone'].initial = profile.phone
            self.fields['district'].initial = profile.district
            self.fields['taluka'].initial = profile.taluka
            self.fields['farm_location'].initial = profile.farm_location
        else:
            self.fields['full_name'].initial = target_user.get_full_name() or target_user.username

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exclude(pk=self.target_user.pk).exists():
            raise ValidationError("This username is already taken by another user.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exclude(pk=self.target_user.pk).exists():
            raise ValidationError("This email is already in use by another user.")
        return email

    def save(self):
        data = self.cleaned_data
        self.target_user.username = data['username']
        self.target_user.email = data['email']
        self.target_user.is_active = data['is_active']
        self.target_user.is_staff = data['is_staff']
        
        parts = data['full_name'].split()
        self.target_user.first_name = parts[0] if parts else ''
        self.target_user.last_name = ' '.join(parts[1:]) if len(parts) > 1 else ''
        self.target_user.save()

        profile, created = FarmerProfile.objects.get_or_create(user=self.target_user)
        profile.full_name = data['full_name']
        profile.phone = data.get('phone', '')
        profile.state = 'Gujarat'
        profile.district = data.get('district', 'Ahmedabad')
        profile.taluka = data.get('taluka', '')
        profile.farm_location = data.get('farm_location', '')
        profile.save()
        return self.target_user


class AdminCropEditForm(forms.ModelForm):
    """
    Form allowing Administrators to update any farmer's Gujarat crop record.
    """
    class Meta:
        model = Crop
        fields = [
            'crop_name',
            'farmer',
            'crop_type',
            'region',
            'season',
            'farm_area',
            'planting_date',
            'expected_harvest_date',
            'status',
            'notes',
        ]
        widgets = {
            'crop_name': forms.TextInput(attrs={'class': 'admin-form-control', 'id': 'crop_name'}),
            'farmer': forms.Select(attrs={'class': 'admin-form-select', 'id': 'crop_farmer'}),
            'crop_type': forms.Select(attrs={'class': 'admin-form-select', 'id': 'crop_type'}),
            'region': forms.Select(attrs={'class': 'admin-form-select', 'id': 'crop_region'}),
            'season': forms.Select(attrs={'class': 'admin-form-select', 'id': 'season'}),
            'farm_area': forms.NumberInput(attrs={'class': 'admin-form-control', 'step': '0.01', 'id': 'farm_area'}),
            'planting_date': forms.DateInput(attrs={'class': 'admin-form-control', 'type': 'date', 'id': 'planting_date'}),
            'expected_harvest_date': forms.DateInput(attrs={'class': 'admin-form-control', 'type': 'date', 'id': 'expected_harvest_date'}),
            'status': forms.Select(attrs={'class': 'admin-form-select', 'id': 'status'}),
            'notes': forms.Textarea(attrs={'class': 'admin-form-control', 'rows': 4, 'id': 'notes'}),
        }

    def clean_farm_area(self):
        farm_area = self.cleaned_data.get('farm_area')
        if farm_area is not None and farm_area <= 0:
            raise ValidationError("Farm area must be greater than zero.")
        return farm_area

    def clean(self):
        cleaned_data = super().clean()
        planting_date = cleaned_data.get('planting_date')
        expected_harvest_date = cleaned_data.get('expected_harvest_date')

        if planting_date and expected_harvest_date:
            if expected_harvest_date < planting_date:
                self.add_error('expected_harvest_date', "Expected harvest date cannot be earlier than planting date.")
        return cleaned_data


class AdminFarmingTipForm(forms.ModelForm):
    """
    Form allowing Administrators to create and update Farming Tips.
    """
    class Meta:
        model = FarmingTip
        fields = ['title', 'category', 'description', 'level', 'icon', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'admin-form-control',
                'placeholder': 'e.g., Soil Testing & pH Balance',
                'id': 'tip_title'
            }),
            'category': forms.Select(attrs={
                'class': 'admin-form-select',
                'id': 'tip_category'
            }),
            'description': forms.Textarea(attrs={
                'class': 'admin-form-control',
                'rows': 4,
                'placeholder': 'Describe best agricultural practices in detail...',
                'id': 'tip_description'
            }),
            'level': forms.TextInput(attrs={
                'class': 'admin-form-control',
                'placeholder': 'e.g., Essential, Best Practice, Organic, Water-Saver',
                'id': 'tip_level'
            }),
            'icon': forms.TextInput(attrs={
                'class': 'admin-form-control',
                'placeholder': 'FontAwesome class, e.g., fa-seedling, fa-faucet-drip, fa-mountain-sun',
                'id': 'tip_icon'
            }),
            'image': forms.FileInput(attrs={
                'class': 'admin-form-control',
                'id': 'tip_image'
            }),
        }


class ForgotPasswordRequestForm(forms.Form):
    """
    Form for requesting a 6-digit password reset OTP by entering registered email address.
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your registered email address',
            'id': 'forgot_email',
            'autocomplete': 'email',
            'style': 'padding-left: 2.75rem;'
        })
    )


class PasswordResetConfirmForm(forms.Form):
    """
    Form for creating a new password after successful OTP verification.
    Enforces minimum 8 characters, mismatch validation, and Django password rules.
    """
    new_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your new password (min. 8 characters)',
            'id': 'new_password',
            'autocomplete': 'new-password',
            'style': 'padding-left: 2.75rem; padding-right: 2.75rem;'
        })
    )
    confirm_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your new password',
            'id': 'confirm_password',
            'autocomplete': 'new-password',
            'style': 'padding-left: 2.75rem; padding-right: 2.75rem;'
        })
    )

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match. Please verify and retype.")

        if new_password:
            if len(new_password) < 8:
                self.add_error('new_password', "Password must contain at least 8 characters.")
            else:
                from django.contrib.auth.password_validation import validate_password
                try:
                    validate_password(new_password, user=self.user)
                except ValidationError as err:
                    for error in err.messages:
                        self.add_error('new_password', error)

        return cleaned_data

