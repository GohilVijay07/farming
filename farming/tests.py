from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, timedelta
from .models import FarmerProfile, Crop, ContactMessage, EmailVerificationOTP, PasswordResetOTP, FarmingTip, ActivityLog



class AgriConnectModelsTestCase(TestCase):
    """
    Test suite for database models and validation logic.
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username='rajesh_farmer',
            email='rajesh@example.com',
            password='Password123!',
            first_name='Rajesh',
            last_name='Patel'
        )
        self.profile = FarmerProfile.objects.create(
            user=self.user,
            full_name='Rajesh Patel',
            phone='+91 9876543210',
            state='Gujarat',
            district='Rajkot',
            taluka='Gondal',
            farm_location='Gondal Farm'
        )

    def test_farmer_profile_creation(self):
        self.assertEqual(self.profile.full_name, 'Rajesh Patel')
        self.assertEqual(self.profile.district, 'Rajkot')
        self.assertEqual(self.profile.state, 'Gujarat')
        self.assertIn('Rajkot, Gujarat', self.profile.get_location_display())
        self.assertEqual(self.user.farmer_profile.phone, '+91 9876543210')

    def test_crop_creation(self):
        crop = Crop.objects.create(
            farmer=self.user,
            crop_name='Cotton (કપાસ)',
            crop_type='Cash Crop',
            region='Saurashtra',
            season='Kharif (Monsoon)',
            farm_area=12.50,
            planting_date=date.today(),
            expected_harvest_date=date.today() + timedelta(days=150),
            status='Growing',
            notes='Treated with bio-fertilizers.'
        )
        self.assertEqual(crop.farmer, self.user)
        self.assertEqual(crop.farm_area, 12.50)
        self.assertEqual(crop.region, 'Saurashtra')
        self.assertIn('Cotton (કપાસ)', str(crop))

    def test_contact_message_creation(self):
        msg = ContactMessage.objects.create(
            name='Amit Patel',
            email='amit@example.com',
            subject='Irrigation Inquiry',
            message='Need guidance on drip irrigation setup for cotton in Saurashtra.'
        )
        self.assertEqual(msg.name, 'Amit Patel')
        self.assertIn('Amit Patel', str(msg))


class AgriConnectViewsTestCase(TestCase):
    """
    Test suite for URL routing, view rendering, authentication, and crop security.
    """
    def setUp(self):
        self.client = Client()
        # Farmer 1
        self.user1 = User.objects.create_user(username='farmer1', email='farmer1@example.com', password='Password123!')
        self.profile1 = FarmerProfile.objects.create(
            user=self.user1,
            full_name='Farmer One',
            phone='1234567890',
            state='Gujarat',
            district='Ahmedabad',
            taluka='Daskroi',
            farm_location='Bavla Road'
        )
        self.crop1 = Crop.objects.create(
            farmer=self.user1,
            crop_name='Cotton (કપાસ)',
            crop_type='Cash Crop',
            region='Central Gujarat',
            season='Kharif (Monsoon)',
            farm_area=5.00,
            planting_date=date.today(),
            expected_harvest_date=date.today() + timedelta(days=150),
            status='Planted'
        )

        # Farmer 2 (unauthorized to modify farmer1's crops)
        self.user2 = User.objects.create_user(username='farmer2', email='farmer2@example.com', password='Password123!')
        self.profile2 = FarmerProfile.objects.create(
            user=self.user2,
            full_name='Farmer Two',
            phone='0987654321',
            state='Gujarat',
            district='Rajkot',
            taluka='Jasdan',
            farm_location='Jasdan Village'
        )

    def test_public_pages_status_200(self):
        """Verify public informational pages load with HTTP 200."""
        routes = ['home', 'about', 'crops', 'farming_tips', 'weather', 'contact', 'login', 'register']
        for route in routes:
            response = self.client.get(reverse(route))
            self.assertEqual(response.status_code, 200, f"Route '{route}' failed with status {response.status_code}")

    def test_contact_form_submission(self):
        """Test submitting the contact form saves to PostgreSQL database."""
        response = self.client.post(reverse('contact'), {
            'name': 'Test Visitor',
            'email': 'visitor@test.com',
            'subject': 'Help with soil testing in Gujarat',
            'message': 'Where can I find local KVK soil testing labs in Rajkot?'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ContactMessage.objects.filter(email='visitor@test.com').exists())

    def test_dashboard_requires_login(self):
        """Ensure dashboard and crop actions require authentication."""
        protected_routes = ['dashboard', 'my_crops', 'add_crop', 'profile']
        for route in protected_routes:
            response = self.client.get(reverse(route))
            self.assertRedirects(response, f"/login/?next={reverse(route)}")

    def test_farmer_login_and_dashboard(self):
        """Test login success and dashboard summary calculations."""
        login_success = self.client.login(username='farmer1', password='Password123!')
        self.assertTrue(login_success)

        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total_crops'], 1)
        self.assertEqual(response.context['active_crops'], 1)

    def test_add_crop_flow(self):
        """Test adding a Gujarat crop as logged-in farmer."""
        self.client.login(username='farmer1', password='Password123!')
        response = self.client.post(reverse('add_crop'), {
            'crop_name': 'Cotton BT-2',
            'crop_type': 'Cash Crop',
            'region': 'Saurashtra',
            'season': 'Kharif (Monsoon)',
            'farm_area': '8.50',
            'planting_date': '2026-06-01',
            'expected_harvest_date': '2026-11-15',
            'status': 'Planted',
            'notes': 'High yield Saurashtra variety.'
        }, follow=True)
        self.assertRedirects(response, reverse('my_crops'))
        self.assertTrue(Crop.objects.filter(crop_name='Cotton BT-2', farmer=self.user1).exists())

    def test_crop_ownership_security_prevent_unauthorized_edit(self):
        """Security: Farmer 2 must NOT be able to edit Farmer 1's crop."""
        self.client.login(username='farmer2', password='Password123!')
        # Farmer 2 attempts to post changes to Farmer 1's crop
        response = self.client.post(reverse('edit_crop', args=[self.crop1.id]), {
            'crop_name': 'Hacked Crop Name',
            'crop_type': 'Cereal / Grain',
            'region': 'Central Gujarat',
            'season': 'Kharif (Monsoon)',
            'farm_area': '10.00',
            'planting_date': '2026-06-01',
            'expected_harvest_date': '2026-11-15',
            'status': 'Growing'
        }, follow=True)
        # Should redirect back to my_crops with access denied error
        self.assertRedirects(response, reverse('my_crops'))
        self.crop1.refresh_from_db()
        self.assertEqual(self.crop1.crop_name, 'Cotton (કપાસ)')  # Name remains unchanged

    def test_crop_ownership_security_prevent_unauthorized_delete(self):
        """Security: Farmer 2 must NOT be able to delete Farmer 1's crop."""
        self.client.login(username='farmer2', password='Password123!')
        response = self.client.get(reverse('delete_crop', args=[self.crop1.id]), follow=True)
        self.assertRedirects(response, reverse('my_crops'))
        self.assertTrue(Crop.objects.filter(id=self.crop1.id).exists())  # Crop not deleted


class AgriConnectEmailOTPTestCase(TestCase):
    """
    Comprehensive test suite covering all 8 test cases for the 6-Digit Email OTP Verification System.
    """
    def setUp(self):
        self.client = Client()
        self.reg_data = {
            'full_name': 'Ramesh Patel',
            'username': 'ramesh_farmer',
            'email': 'ramesh@agriconnect.test',
            'phone': '+91 9876543210',
            'district': 'Anand',
            'taluka': 'Anand',
            'farm_location': 'Hadgood Village',
            'password': 'SecurePassword123!',
            'confirm_password': 'SecurePassword123!',
        }

    def test_1_registration_flow_creates_inactive_user_and_otp(self):
        """Test 1: Registration creates an inactive user, creates EmailVerificationOTP, and redirects to /verify-otp/."""
        response = self.client.post(reverse('register'), self.reg_data, follow=True)
        self.assertRedirects(response, reverse('verify_otp'))

        user = User.objects.filter(username='ramesh_farmer').first()
        self.assertIsNotNone(user)
        self.assertFalse(user.is_active, "New user must be inactive before OTP verification.")

        otp_record = EmailVerificationOTP.objects.filter(user=user, is_verified=False).first()
        self.assertIsNotNone(otp_record, "EmailVerificationOTP record must be created.")
        self.assertTrue(otp_record.otp_hash.startswith('pbkdf2_sha256$') or len(otp_record.otp_hash) > 40, "OTP must be stored as a cryptographic hash, not plain text.")
        self.assertNotEqual(len(otp_record.otp_hash), 6, "Plain OTP must not be stored.")

        self.assertFalse(otp_record.is_verified)
        self.assertEqual(otp_record.attempts, 0)
        self.assertEqual(self.client.session.get('otp_user_id'), user.id)

    def test_2_correct_otp_activates_user_and_allows_login(self):
        """Test 2: Submitting the correct 6-digit OTP activates user and allows subsequent login."""
        # 1. Register
        self.client.post(reverse('register'), self.reg_data)
        user = User.objects.get(username='ramesh_farmer')

        # 2. Inject known 6-digit OTP
        known_otp = "583214"
        otp_record = EmailVerificationOTP.objects.get(user=user, is_verified=False)
        otp_record.set_otp(known_otp)
        otp_record.save()

        # 3. Post OTP
        response = self.client.post(reverse('verify_otp'), {'otp': known_otp}, follow=True)
        self.assertRedirects(response, reverse('login'))

        # Check user is activated
        user.refresh_from_db()
        self.assertTrue(user.is_active, "User must be activated after correct OTP verification.")

        otp_record.refresh_from_db()
        self.assertTrue(otp_record.is_verified, "OTP record must be marked as verified.")

        # 4. Login with verified account
        login_response = self.client.post(reverse('login'), {
            'username': 'ramesh_farmer',
            'password': 'SecurePassword123!'
        }, follow=True)
        self.assertRedirects(login_response, reverse('dashboard'))

    def test_3_incorrect_otp_increments_attempts(self):
        """Test 3: Submitting an incorrect OTP increments the failed attempts counter and keeps user inactive."""
        self.client.post(reverse('register'), self.reg_data)
        user = User.objects.get(username='ramesh_farmer')

        otp_record = EmailVerificationOTP.objects.get(user=user, is_verified=False)
        otp_record.set_otp("123456")
        otp_record.save()

        # Enter wrong OTP
        response = self.client.post(reverse('verify_otp'), {'otp': '999999'}, follow=True)
        self.assertEqual(response.status_code, 200)

        otp_record.refresh_from_db()
        self.assertEqual(otp_record.attempts, 1)
        self.assertFalse(otp_record.is_verified)

        user.refresh_from_db()
        self.assertFalse(user.is_active)

    def test_4_five_incorrect_attempts_invalidates_otp(self):
        """Test 4: Entering incorrect OTP 5 times blocks verification and requires a new OTP."""
        self.client.post(reverse('register'), self.reg_data)
        user = User.objects.get(username='ramesh_farmer')

        otp_record = EmailVerificationOTP.objects.get(user=user, is_verified=False)
        otp_record.set_otp("123456")
        otp_record.save()

        # Submit wrong OTP 5 times
        for _ in range(5):
            self.client.post(reverse('verify_otp'), {'otp': '000000'})

        otp_record.refresh_from_db()
        self.assertEqual(otp_record.attempts, 5)

        # 6th attempt should be blocked even if entered correct OTP
        response = self.client.post(reverse('verify_otp'), {'otp': '123456'}, follow=True)
        self.assertIn("Too many incorrect attempts", response.content.decode())

        user.refresh_from_db()
        self.assertFalse(user.is_active)

    def test_5_expired_otp_is_rejected(self):
        """Test 5: OTP older than 3 minutes is rejected as expired."""
        from django.utils import timezone
        self.client.post(reverse('register'), self.reg_data)
        user = User.objects.get(username='ramesh_farmer')

        # Set expires_at to 1 minute in the past
        otp_record = EmailVerificationOTP.objects.get(user=user, is_verified=False)
        otp_record.set_otp("654321")
        otp_record.expires_at = timezone.now() - timedelta(minutes=1)
        otp_record.save()

        response = self.client.post(reverse('verify_otp'), {'otp': '654321'}, follow=True)
        self.assertIn("expired", response.content.decode().lower())

        user.refresh_from_db()
        self.assertFalse(user.is_active)

    def test_6_resend_otp_invalidates_old_and_generates_new(self):
        """Test 6: Resending OTP creates a fresh OTP, resets attempts and expiration, and invalidates old OTP."""
        from django.utils import timezone
        self.client.post(reverse('register'), self.reg_data)
        user = User.objects.get(username='ramesh_farmer')

        old_otp_record = EmailVerificationOTP.objects.get(user=user, is_verified=False)
        old_otp_record.set_otp("111111")
        # Backdate created_at to bypass 60s cooldown for testing resend
        old_otp_record.created_at = timezone.now() - timedelta(seconds=70)
        old_otp_record.save()

        # Request resend
        resend_response = self.client.get(reverse('resend_otp'), follow=True)
        self.assertRedirects(resend_response, reverse('verify_otp'))

        # Old OTP record deleted/invalidated, new one created
        new_otp_record = EmailVerificationOTP.objects.filter(user=user, is_verified=False).first()
        self.assertIsNotNone(new_otp_record)
        self.assertNotEqual(old_otp_record.id, new_otp_record.id)

        # Old OTP no longer works
        self.client.post(reverse('verify_otp'), {'otp': '111111'})
        user.refresh_from_db()
        self.assertFalse(user.is_active)

        # Set known code to new OTP and verify
        new_otp_record.set_otp("222222")
        new_otp_record.save()
        verify_response = self.client.post(reverse('verify_otp'), {'otp': '222222'}, follow=True)
        self.assertRedirects(verify_response, reverse('login'))
        user.refresh_from_db()
        self.assertTrue(user.is_active)

    def test_7_resend_cooldown_rate_limiting(self):
        """Test 7: Attempting to resend OTP within 60 seconds is blocked by rate limiting."""
        self.client.post(reverse('register'), self.reg_data)
        # Immediately attempt resend
        response = self.client.get(reverse('resend_otp'), follow=True)
        self.assertRedirects(response, reverse('verify_otp'))
        self.assertIn("Please wait", response.content.decode())

    def test_8_login_blocked_for_unverified_user(self):
        """Test 8: Unverified/inactive user attempting to log in is blocked with a verification warning."""
        self.client.post(reverse('register'), self.reg_data)

        # Attempt to log in before verifying OTP
        response = self.client.post(reverse('login'), {
            'username': 'ramesh_farmer',
            'password': 'SecurePassword123!'
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Please verify your email using the OTP before logging in", response.content.decode())
        self.assertIn("Verify Email", response.content.decode())
        self.assertIn("Resend OTP", response.content.decode())
        self.assertFalse(response.context['user'].is_authenticated)


class AgriConnectAdminTestCase(TestCase):
    """
    Complete test suite for the Admin Dashboard & Management System.
    """
    def setUp(self):
        self.client = Client()

        # 1. Staff Admin User
        self.admin_user = User.objects.create_user(
            username='admin_staff',
            email='admin@agriconnect.com',
            password='AdminPassword123!',
            is_staff=True
        )

        # 2. Superuser Admin
        self.superuser = User.objects.create_superuser(
            username='super_admin',
            email='super@agriconnect.com',
            password='SuperPassword123!'
        )

        # 3. Regular Verified Farmer
        self.farmer_user = User.objects.create_user(
            username='regular_farmer',
            email='farmer@example.com',
            password='FarmerPassword123!',
            is_active=True,
            is_staff=False,
            is_superuser=False
        )
        self.farmer_profile = FarmerProfile.objects.create(
            user=self.farmer_user,
            full_name='Regular Farmer Patel',
            phone='9876543210',
            state='Gujarat',
            district='Gir Somnath',
            taluka='Talala',
            farm_location='Talala Farm'
        )

        # 4. Regular Unverified Farmer
        self.unverified_user = User.objects.create_user(
            username='unverified_farmer',
            email='unverified@example.com',
            password='Password123!',
            is_active=False
        )

        # 5. Sample Crops
        self.crop1 = Crop.objects.create(
            farmer=self.farmer_user,
            crop_name='Groundnut GG-20',
            crop_type='Oilseed',
            region='Saurashtra',
            season='Kharif (Monsoon)',
            farm_area=10.0,
            planting_date=date.today(),
            expected_harvest_date=date.today() + timedelta(days=120),
            status='Growing'
        )
        self.crop2 = Crop.objects.create(
            farmer=self.farmer_user,
            crop_name='Cotton (કપાસ)',
            crop_type='Cash Crop',
            region='Saurashtra',
            season='Kharif (Monsoon)',
            farm_area=15.0,
            planting_date=date.today(),
            expected_harvest_date=date.today() + timedelta(days=150),
            status='Harvested'
        )

    def test_admin_login_success_staff_and_superuser(self):
        """Staff and Superuser accounts can log into the Admin portal."""
        # Staff Admin
        response = self.client.post(reverse('admin_login'), {
            'username': 'admin_staff',
            'password': 'AdminPassword123!'
        }, follow=True)
        self.assertRedirects(response, reverse('admin_dashboard'))
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertTrue(response.context['user'].is_staff)
        self.client.logout()

        # Superuser
        response = self.client.post(reverse('admin_login'), {
            'username': 'super_admin',
            'password': 'SuperPassword123!'
        }, follow=True)
        self.assertRedirects(response, reverse('admin_dashboard'))

    def test_admin_login_rejected_for_regular_farmer(self):
        """Non-staff regular farmers cannot log into /admin-login/."""
        response = self.client.post(reverse('admin_login'), {
            'username': 'regular_farmer',
            'password': 'FarmerPassword123!'
        }, follow=True)
        self.assertIn("Access restricted: This account does not have administrator privileges", response.content.decode())
        self.assertFalse(response.context['user'].is_authenticated)

    def test_admin_dashboard_access_denied_for_regular_farmer(self):
        """Logged-in regular farmer trying /admin-dashboard/ is redirected away."""
        self.client.login(username='regular_farmer', password='FarmerPassword123!')
        response = self.client.get(reverse('admin_dashboard'), follow=True)
        self.assertRedirects(response, reverse('dashboard'))
        self.assertIn("Access denied: Administrator privileges required", response.content.decode())

    def test_admin_dashboard_statistics_calculation(self):
        """Verify 9 core metrics calculation on executive dashboard."""
        self.client.login(username='admin_staff', password='AdminPassword123!')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)

        # 4 total users: admin_staff, super_admin, regular_farmer, unverified_farmer
        self.assertEqual(response.context['total_users'], 4)
        # 3 verified: admin_staff, super_admin, regular_farmer
        self.assertEqual(response.context['verified_users'], 3)
        # 1 unverified: unverified_farmer
        self.assertEqual(response.context['unverified_users'], 1)
        # 2 crops
        self.assertEqual(response.context['total_crops'], 2)
        # 1 active crop (Growing)
        self.assertEqual(response.context['active_crops'], 1)
        # 1 harvested crop
        self.assertEqual(response.context['harvested_crops'], 1)
        # Total area 10 + 15 = 25 Acres
        self.assertEqual(response.context['total_farm_area'], 25.0)

    def test_admin_user_management_search_and_toggle(self):
        """Test searching users and toggling account active status."""
        self.client.login(username='admin_staff', password='AdminPassword123!')

        # Search by farm location or district
        response = self.client.get(reverse('admin_users') + '?q=Gir+Somnath')
        self.assertEqual(response.status_code, 200)
        self.assertIn('regular_farmer', response.content.decode())

        # Toggle regular farmer status to inactive
        self.client.get(reverse('admin_user_toggle_status', args=[self.farmer_user.id]), follow=True)
        self.farmer_user.refresh_from_db()
        self.assertFalse(self.farmer_user.is_active)

        # Self-deactivation prevention test
        response = self.client.get(reverse('admin_user_toggle_status', args=[self.admin_user.id]), follow=True)
        self.admin_user.refresh_from_db()
        self.assertTrue(self.admin_user.is_active)
        self.assertIn("Security protection: You cannot deactivate your own administrative account", response.content.decode())

    def test_admin_user_delete_self_prevention(self):
        """Admin cannot delete their own account."""
        self.client.login(username='admin_staff', password='AdminPassword123!')
        response = self.client.post(reverse('admin_user_delete', args=[self.admin_user.id]), follow=True)
        self.assertTrue(User.objects.filter(username='admin_staff').exists())
        self.assertIn("Security protection: You cannot delete your own administrative account", response.content.decode())

    def test_contact_message_submission_and_auto_read(self):
        """Contact submission creates DB record, and admin viewing it auto-marks as Read."""
        # 1. Visitor submits inquiry
        self.client.post(reverse('contact'), {
            'name': 'Pooja Patel',
            'email': 'pooja@example.com',
            'subject': 'Soil Health Card Inquiry',
            'message': 'How do I submit soil samples through AgriConnect?'
        })
        msg = ContactMessage.objects.get(email='pooja@example.com')
        self.assertFalse(msg.is_read)
        self.assertIsNone(msg.read_at)

        # 2. Admin logs in and opens message detail
        self.client.login(username='admin_staff', password='AdminPassword123!')
        response = self.client.get(reverse('admin_message_detail', args=[msg.id]))
        self.assertEqual(response.status_code, 200)

        # 3. Message is automatically marked is_read=True
        msg.refresh_from_db()
        self.assertTrue(msg.is_read)
        self.assertIsNotNone(msg.read_at)

    def test_farming_tip_crud_flow(self):
        """Admin can create, edit, and delete farming tips."""
        self.client.login(username='admin_staff', password='AdminPassword123!')

        # Create
        self.client.post(reverse('admin_tip_add'), {
            'title': 'Drip Irrigation Maintenance',
            'category': 'Irrigation',
            'description': 'Flush laterals once every month with acid treatment.',
            'level': 'Best Practice',
            'icon': 'fa-faucet-drip'
        }, follow=True)
        tip = FarmingTip.objects.get(title='Drip Irrigation Maintenance')
        self.assertEqual(tip.category, 'Irrigation')

        # Edit
        self.client.post(reverse('admin_tip_edit', args=[tip.id]), {
            'title': 'Drip Irrigation Maintenance & Acid Wash',
            'category': 'Irrigation',
            'description': 'Updated maintenance schedule.',
            'level': 'Essential',
            'icon': 'fa-faucet-drip'
        }, follow=True)
        tip.refresh_from_db()
        self.assertEqual(tip.title, 'Drip Irrigation Maintenance & Acid Wash')

        # Delete
        self.client.post(reverse('admin_tip_delete', args=[tip.id]), follow=True)
        self.assertFalse(FarmingTip.objects.filter(id=tip.id).exists())

    def test_admin_logout_redirects_to_admin_login(self):
        """Logging out from admin portal redirects to /admin-login/."""
        self.client.login(username='admin_staff', password='AdminPassword123!')
        response = self.client.get(reverse('admin_logout'), follow=True)
        self.assertRedirects(response, reverse('admin_login'))
        self.assertFalse(response.context['user'].is_authenticated)


class AgriConnectPasswordResetTestCase(TestCase):
    """
    Test suite for complete Forgot Password -> Email OTP -> New Password flow.
    """
    def setUp(self):
        self.client = Client()
        self.farmer = User.objects.create_user(
            username='bhavesh_farmer',
            email='bhavesh@example.com',
            password='OldPassword123!',
            first_name='Bhavesh',
            last_name='Patel',
            is_active=True
        )
        self.profile = FarmerProfile.objects.create(
            user=self.farmer,
            full_name='Bhavesh Patel',
            phone='9898989898',
            state='Gujarat',
            district='Rajkot',
            taluka='Gondal'
        )

        self.unverified_farmer = User.objects.create_user(
            username='unverified_user',
            email='unverified_user@example.com',
            password='Password123!',
            is_active=False
        )

    def test_login_page_forgot_password_link_no_alert(self):
        """1. Login page contains link to /forgot-password/ and no college demo alert."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertIn(reverse('forgot_password'), content)
        self.assertNotIn("alert('For college demonstration", content)
        self.assertNotIn("default accounts can be reset or created", content)

    def test_forgot_password_page_renders_cleanly(self):
        """2. GET /forgot-password/ renders email input form."""
        response = self.client.get(reverse('forgot_password'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'farming/forgot_password.html')
        self.assertIn("Reset Your Password", response.content.decode())

    def test_forgot_password_generic_message_prevents_email_enumeration(self):
        """3. Submitting non-existent email returns generic message without leaking account existence."""
        response = self.client.post(reverse('forgot_password'), {
            'email': 'nonexistent_user@example.com'
        }, follow=True)
        self.assertRedirects(response, reverse('verify_password_reset_otp'))
        self.assertIn("If an account with this email exists, a verification OTP has been sent", response.content.decode())
        self.assertEqual(PasswordResetOTP.objects.count(), 0)

    def test_forgot_password_valid_user_creates_hashed_otp_and_sends_email(self):
        """4. Submitting registered email creates hashed PasswordResetOTP record with 10 min expiry."""
        response = self.client.post(reverse('forgot_password'), {
            'email': 'bhavesh@example.com'
        }, follow=True)
        self.assertRedirects(response, reverse('verify_password_reset_otp'))
        self.assertEqual(PasswordResetOTP.objects.filter(user=self.farmer).count(), 1)
        otp_rec = PasswordResetOTP.objects.get(user=self.farmer)
        self.assertFalse(otp_rec.is_verified)
        self.assertEqual(otp_rec.attempts, 0)
        self.assertFalse(otp_rec.is_expired())
        self.assertEqual(self.client.session.get('password_reset_user_id'), self.farmer.id)

    def test_forgot_password_unverified_account_redirects_to_email_verification(self):
        """5. Submitting email for an unverified user redirects to email verification."""
        response = self.client.post(reverse('forgot_password'), {
            'email': 'unverified_user@example.com'
        }, follow=True)
        self.assertRedirects(response, reverse('verify_otp'))
        self.assertIn("Your account has not been email-verified yet", response.content.decode())

    def test_verify_otp_valid_code_grants_reset_access(self):
        """6. Submitting correct OTP marks OTP verified and redirects to /forgot-password/reset/."""
        # Setup OTP
        raw_code = "654321"
        otp_rec = PasswordResetOTP(
            user=self.farmer,
            expires_at=timezone.now() + timedelta(minutes=10),
            attempts=0,
            is_verified=False
        )
        otp_rec.set_otp(raw_code)
        otp_rec.save()

        # Set session
        session = self.client.session
        session['password_reset_user_id'] = self.farmer.id
        session.save()

        response = self.client.post(reverse('verify_password_reset_otp'), {
            'otp_1': '6', 'otp_2': '5', 'otp_3': '4', 'otp_4': '3', 'otp_5': '2', 'otp_6': '1'
        }, follow=True)

        self.assertRedirects(response, reverse('reset_password'))
        otp_rec.refresh_from_db()
        self.assertTrue(otp_rec.is_verified)
        self.assertTrue(self.client.session.get('password_reset_verified'))

    def test_verify_otp_invalid_code_tracks_failed_attempts(self):
        """7. Submitting incorrect OTP increments attempts counter."""
        raw_code = "112233"
        otp_rec = PasswordResetOTP(
            user=self.farmer,
            expires_at=timezone.now() + timedelta(minutes=10),
            attempts=0,
            is_verified=False
        )
        otp_rec.set_otp(raw_code)
        otp_rec.save()

        session = self.client.session
        session['password_reset_user_id'] = self.farmer.id
        session.save()

        response = self.client.post(reverse('verify_password_reset_otp'), {
            'otp': '999999'
        }, follow=True)

        otp_rec.refresh_from_db()
        self.assertEqual(otp_rec.attempts, 1)
        self.assertFalse(otp_rec.is_verified)
        self.assertIn("Invalid OTP", response.content.decode())

    def test_verify_otp_five_failures_locks_otp(self):
        """8. Reaching 5 incorrect attempts invalidates the OTP."""
        raw_code = "112233"
        otp_rec = PasswordResetOTP(
            user=self.farmer,
            expires_at=timezone.now() + timedelta(minutes=10),
            attempts=4,
            is_verified=False
        )
        otp_rec.set_otp(raw_code)
        otp_rec.save()

        session = self.client.session
        session['password_reset_user_id'] = self.farmer.id
        session.save()

        response = self.client.post(reverse('verify_password_reset_otp'), {
            'otp': '000000'
        }, follow=True)

        otp_rec.refresh_from_db()
        self.assertEqual(otp_rec.attempts, 5)
        self.assertIn("Too many incorrect attempts", response.content.decode())

    def test_verify_otp_expired_code_is_rejected(self):
        """9. Expired OTP (>10 mins old) is rejected."""
        otp_rec = PasswordResetOTP(
            user=self.farmer,
            expires_at=timezone.now() - timedelta(minutes=1),
            attempts=0,
            is_verified=False
        )
        otp_rec.set_otp("123456")
        otp_rec.save()

        session = self.client.session
        session['password_reset_user_id'] = self.farmer.id
        session.save()

        response = self.client.post(reverse('verify_password_reset_otp'), {
            'otp': '123456'
        }, follow=True)

        self.assertIn("Your OTP has expired", response.content.decode())

    def test_resend_otp_rate_limiting_and_new_otp(self):
        """10. Resend OTP respects 60s cooldown, invalidates older OTP, and dispatches new one."""
        session = self.client.session
        session['password_reset_user_id'] = self.farmer.id
        session.save()

        # First request
        otp1 = PasswordResetOTP(
            user=self.farmer,
            expires_at=timezone.now() + timedelta(minutes=10),
            attempts=0,
            is_verified=False
        )
        otp1.set_otp("111111")
        otp1.save()

        # Attempt resend immediately (<60s)
        response = self.client.get(reverse('resend_password_reset_otp'), follow=True)
        self.assertIn("Please wait", response.content.decode())

        # Age the OTP created_at to >60 seconds ago
        PasswordResetOTP.objects.filter(id=otp1.id).update(
            created_at=timezone.now() - timedelta(seconds=65)
        )

        response2 = self.client.get(reverse('resend_password_reset_otp'), follow=True)
        self.assertIn("A new password reset OTP has been sent", response2.content.decode())
        self.assertEqual(PasswordResetOTP.objects.filter(user=self.farmer, is_verified=False).count(), 1)
        new_otp = PasswordResetOTP.objects.filter(user=self.farmer, is_verified=False).first()
        self.assertNotEqual(new_otp.id, otp1.id)

    def test_reset_password_direct_access_blocked_without_otp(self):
        """11. Directly accessing /forgot-password/reset/ without verified OTP is blocked."""
        response = self.client.get(reverse('reset_password'), follow=True)
        self.assertRedirects(response, reverse('forgot_password'))
        self.assertIn("Please verify your OTP before resetting your password", response.content.decode())

    def test_reset_password_success_flow_and_login(self):
        """12. Complete password reset changes password and enables login with new credentials."""
        # Set verified session
        session = self.client.session
        session['password_reset_user_id'] = self.farmer.id
        session['password_reset_verified'] = True
        session['password_reset_verified_at'] = timezone.now().timestamp()
        session.save()

        # Submit new password
        response = self.client.post(reverse('reset_password'), {
            'new_password': 'BrandNewPassword2026!',
            'confirm_password': 'BrandNewPassword2026!'
        }, follow=True)

        self.assertRedirects(response, reverse('password_reset_success'))
        self.assertIn("Password Reset Successfully", response.content.decode())

        # Verify database password update
        self.farmer.refresh_from_db()
        self.assertTrue(self.farmer.check_password('BrandNewPassword2026!'))
        self.assertFalse(self.farmer.check_password('OldPassword123!'))

        # Verify login with new password (by username)
        login_res1 = self.client.post(reverse('login'), {
            'username': 'bhavesh_farmer',
            'password': 'BrandNewPassword2026!'
        }, follow=True)
        self.assertEqual(login_res1.status_code, 200)
        self.assertTrue(login_res1.context['user'].is_authenticated)
        self.client.logout()

        # Verify login with new password (by email)
        login_res2 = self.client.post(reverse('login'), {
            'username': 'bhavesh@example.com',
            'password': 'BrandNewPassword2026!'
        }, follow=True)

class AgriConnectWeatherTestCase(TestCase):
    """
    Test suite for Gujarat Agricultural WeatherAPI.com backend integration,
    caching, 5-day forecast, and strict Gujarat whitelist validation.
    """
    def setUp(self):
        self.client = Client()

    def test_weather_page_render(self):
        """1. /weather/ page renders successfully with Gujarat branding and all 33 districts."""
        response = self.client.get(reverse('weather'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'farming/weather.html')
        content = response.content.decode()
        self.assertIn("Gujarat", content)
        self.assertIn("Farming Weather Advice", content)
        self.assertIn("Forecast", content)
        self.assertIn("Ahmedabad", content)
        self.assertIn("Surat", content)
        self.assertIn("Rajkot", content)

    def test_api_weather_valid_gujarat_locations(self):
        """2. /api/weather/?city=... returns live WeatherAPI.com data for Gujarat locations."""
        for city in ['Ahmedabad', 'Surat', 'Rajkot', 'Vadodara', 'Bhuj', 'Junagadh', 'Mehsana']:
            response = self.client.get(reverse('api_weather'), {'city': city})
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertTrue(data['success'])
            self.assertEqual(data['state'], 'Gujarat')
            self.assertEqual(data['country'], 'India')
            self.assertIn('temperature', data)
            self.assertIn('condition', data)
            self.assertIn('humidity', data)
            self.assertIn('wind_speed', data)
            self.assertIn('pressure', data)
            self.assertIn('forecast', data)
            self.assertIn('farming_advice', data)
            self.assertTrue(len(data['forecast']) > 0)
            self.assertIn('items', data['farming_advice'])

    def test_api_weather_rejects_outside_gujarat(self):
        """3. Outside-Gujarat locations must be strictly rejected with the required error message."""
        outside_locations = ['Mumbai', 'Delhi', 'Pune', 'Jaipur', 'Rajasthan', 'Punjab', 'Kolkata', 'Bangalore', 'London', 'New York']
        for loc in outside_locations:
            response = self.client.get(reverse('api_weather'), {'city': loc})
            self.assertEqual(response.status_code, 400)
            data = response.json()
            self.assertFalse(data['success'])
            self.assertEqual(data['error'], 'AgriConnect provides weather information only for Gujarat.')

    def test_api_weather_caching(self):
        """4. WeatherAPI responses are cached in Django memory cache."""
        from django.core.cache import cache
        cache.clear()
        
        # First call fetches from API and caches
        res1 = self.client.get(reverse('api_weather'), {'city': 'Ahmedabad'})
        self.assertEqual(res1.status_code, 200)
        
        # Check cache entry
        cached_data = cache.get('agri_weatherapi_ahmedabad')
        self.assertIsNotNone(cached_data)
        self.assertEqual(cached_data['city'], 'Ahmedabad')
        
        # Second call retrieves from cache
        res2 = self.client.get(reverse('api_weather'), {'city': 'Ahmedabad'})
        self.assertEqual(res2.status_code, 200)
        self.assertEqual(res2.json()['city'], 'Ahmedabad')


