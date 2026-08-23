import os
import json
import logging
import urllib.request
import urllib.parse
import urllib.error
from functools import wraps
from datetime import timedelta, datetime
from django.utils import timezone
from django.conf import settings
from django.core.cache import cache
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.db.models.functions import TruncMonth
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseForbidden, JsonResponse

from .models import (
    FarmerProfile,
    Crop,
    ContactMessage,
    EmailVerificationOTP,
    PasswordResetOTP,
    FarmingTip,
    ActivityLog,
    log_activity
)
from .forms import (
    FarmerRegistrationForm,
    FarmerLoginForm,
    FarmerProfileUpdateForm,
    CropForm,
    ContactForm,
    AdminLoginForm,
    AdminUserEditForm,
    AdminCropEditForm,
    AdminFarmingTipForm,
    ForgotPasswordRequestForm,
    PasswordResetConfirmForm
)


def admin_required(view_func):
    """
    Decorator for views that checks if the user is authenticated and has administrative
    privileges (is_staff or is_superuser).
    Redirects unauthenticated users to /admin-login/.
    Redirects non-admin farmers to /dashboard/ with an error notice.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f'/admin-login/?next={request.path}')
        if not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, "Access denied: Administrator privileges required to access this portal.")
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view



# ==========================================
# PUBLIC INFORMATIONAL VIEWS (GUJARAT FOCUS)
# ==========================================

# 33 Official Gujarat Districts List
GUJARAT_DISTRICTS_LIST = [
    'Ahmedabad', 'Amreli', 'Anand', 'Aravalli', 'Banaskantha', 'Bharuch', 'Bhavnagar',
    'Botad', 'Chhota Udepur', 'Dahod', 'Dang', 'Devbhoomi Dwarka', 'Gandhinagar',
    'Gir Somnath', 'Jamnagar', 'Junagadh', 'Kheda', 'Kutch', 'Mahisagar', 'Mehsana',
    'Morbi', 'Narmada', 'Navsari', 'Panchmahal', 'Patan', 'Porbandar', 'Rajkot',
    'Sabarkantha', 'Surat', 'Surendranagar', 'Tapi', 'Vadodara', 'Valsad'
]

# Canonical Gujarat locations whitelist & lookup mapping for WeatherAPI
GUJARAT_LOCATIONS_MAP = {
    'ahmedabad': {'district': 'Ahmedabad', 'city': 'Ahmedabad', 'region': 'Central Gujarat', 'query': 'Ahmedabad, Gujarat, India'},
    'amreli': {'district': 'Amreli', 'city': 'Amreli', 'region': 'Saurashtra', 'query': 'Amreli, Gujarat, India'},
    'anand': {'district': 'Anand', 'city': 'Anand', 'region': 'Central Gujarat (Charotar)', 'query': 'Anand, Gujarat, India'},
    'aravalli': {'district': 'Aravalli', 'city': 'Modasa', 'region': 'North Gujarat', 'query': 'Modasa, Gujarat, India'},
    'banaskantha': {'district': 'Banaskantha', 'city': 'Palanpur', 'region': 'North Gujarat', 'query': 'Palanpur, Gujarat, India'},
    'bharuch': {'district': 'Bharuch', 'city': 'Bharuch', 'region': 'South Gujarat', 'query': 'Bharuch, Gujarat, India'},
    'bhavnagar': {'district': 'Bhavnagar', 'city': 'Bhavnagar', 'region': 'Saurashtra', 'query': 'Bhavnagar, Gujarat, India'},
    'botad': {'district': 'Botad', 'city': 'Botad', 'region': 'Saurashtra', 'query': 'Botad, Gujarat, India'},
    'chhota udepur': {'district': 'Chhota Udepur', 'city': 'Chhota Udepur', 'region': 'Central Gujarat', 'query': 'Chhota Udepur, Gujarat, India'},
    'chhota udaipur': {'district': 'Chhota Udepur', 'city': 'Chhota Udepur', 'region': 'Central Gujarat', 'query': 'Chhota Udepur, Gujarat, India'},
    'dahod': {'district': 'Dahod', 'city': 'Dahod', 'region': 'Eastern Gujarat', 'query': 'Dahod, Gujarat, India'},
    'dang': {'district': 'Dang', 'city': 'Ahwa', 'region': 'South Gujarat', 'query': 'Ahwa, Gujarat, India'},
    'dangs': {'district': 'Dang', 'city': 'Ahwa', 'region': 'South Gujarat', 'query': 'Ahwa, Gujarat, India'},
    'the dangs': {'district': 'Dang', 'city': 'Ahwa', 'region': 'South Gujarat', 'query': 'Ahwa, Gujarat, India'},
    'devbhoomi dwarka': {'district': 'Devbhoomi Dwarka', 'city': 'Dwarka', 'region': 'Saurashtra', 'query': 'Dwarka, Gujarat, India'},
    'devbhumi dwarka': {'district': 'Devbhoomi Dwarka', 'city': 'Dwarka', 'region': 'Saurashtra', 'query': 'Dwarka, Gujarat, India'},
    'dwarka': {'district': 'Devbhoomi Dwarka', 'city': 'Dwarka', 'region': 'Saurashtra', 'query': 'Dwarka, Gujarat, India'},
    'gandhinagar': {'district': 'Gandhinagar', 'city': 'Gandhinagar', 'region': 'North Gujarat', 'query': 'Gandhinagar, Gujarat, India'},
    'gir somnath': {'district': 'Gir Somnath', 'city': 'Veraval', 'region': 'Saurashtra', 'query': 'Veraval, Gujarat, India'},
    'somnath': {'district': 'Gir Somnath', 'city': 'Somnath', 'region': 'Saurashtra', 'query': 'Veraval, Gujarat, India'},
    'veraval': {'district': 'Gir Somnath', 'city': 'Veraval', 'region': 'Saurashtra', 'query': 'Veraval, Gujarat, India'},
    'jamnagar': {'district': 'Jamnagar', 'city': 'Jamnagar', 'region': 'Saurashtra', 'query': 'Jamnagar, Gujarat, India'},
    'junagadh': {'district': 'Junagadh', 'city': 'Junagadh', 'region': 'Saurashtra', 'query': 'Junagadh, Gujarat, India'},
    'kheda': {'district': 'Kheda', 'city': 'Nadiad', 'region': 'Central Gujarat', 'query': 'Nadiad, Gujarat, India'},
    'nadiad': {'district': 'Kheda', 'city': 'Nadiad', 'region': 'Central Gujarat', 'query': 'Nadiad, Gujarat, India'},
    'kutch': {'district': 'Kutch', 'city': 'Bhuj', 'region': 'Kutch', 'query': 'Bhuj, Gujarat, India'},
    'kachchh': {'district': 'Kutch', 'city': 'Bhuj', 'region': 'Kutch', 'query': 'Bhuj, Gujarat, India'},
    'bhuj': {'district': 'Kutch', 'city': 'Bhuj', 'region': 'Kutch', 'query': 'Bhuj, Gujarat, India'},
    'gandhidham': {'district': 'Kutch', 'city': 'Gandhidham', 'region': 'Kutch', 'query': 'Gandhidham, Gujarat, India'},
    'mandvi': {'district': 'Kutch', 'city': 'Mandvi', 'region': 'Kutch', 'query': 'Mandvi, Gujarat, India'},
    'mahisagar': {'district': 'Mahisagar', 'city': 'Lunawada', 'region': 'Central Gujarat', 'query': 'Lunawada, Gujarat, India'},
    'lunawada': {'district': 'Mahisagar', 'city': 'Lunawada', 'region': 'Central Gujarat', 'query': 'Lunawada, Gujarat, India'},
    'mehsana': {'district': 'Mehsana', 'city': 'Mehsana', 'region': 'North Gujarat', 'query': 'Mehsana, Gujarat, India'},
    'mahesana': {'district': 'Mehsana', 'city': 'Mehsana', 'region': 'North Gujarat', 'query': 'Mehsana, Gujarat, India'},
    'unjha': {'district': 'Mehsana', 'city': 'Unjha', 'region': 'North Gujarat', 'query': 'Unjha, Gujarat, India'},
    'morbi': {'district': 'Morbi', 'city': 'Morbi', 'region': 'Saurashtra', 'query': 'Morbi, Gujarat, India'},
    'narmada': {'district': 'Narmada', 'city': 'Rajpipla', 'region': 'South Gujarat', 'query': 'Rajpipla, Gujarat, India'},
    'rajpipla': {'district': 'Narmada', 'city': 'Rajpipla', 'region': 'South Gujarat', 'query': 'Rajpipla, Gujarat, India'},
    'navsari': {'district': 'Navsari', 'city': 'Navsari', 'region': 'South Gujarat', 'query': 'Navsari, Gujarat, India'},
    'panchmahal': {'district': 'Panchmahal', 'city': 'Godhra', 'region': 'Central Gujarat', 'query': 'Godhra, Gujarat, India'},
    'godhra': {'district': 'Panchmahal', 'city': 'Godhra', 'region': 'Central Gujarat', 'query': 'Godhra, Gujarat, India'},
    'patan': {'district': 'Patan', 'city': 'Patan', 'region': 'North Gujarat', 'query': 'Patan, Gujarat, India'},
    'porbandar': {'district': 'Porbandar', 'city': 'Porbandar', 'region': 'Saurashtra', 'query': 'Porbandar, Gujarat, India'},
    'rajkot': {'district': 'Rajkot', 'city': 'Rajkot', 'region': 'Saurashtra', 'query': 'Rajkot, Gujarat, India'},
    'gondal': {'district': 'Rajkot', 'city': 'Gondal', 'region': 'Saurashtra', 'query': 'Gondal, Gujarat, India'},
    'jetpur': {'district': 'Rajkot', 'city': 'Jetpur', 'region': 'Saurashtra', 'query': 'Jetpur, Gujarat, India'},
    'sabarkantha': {'district': 'Sabarkantha', 'city': 'Himatnagar', 'region': 'North Gujarat', 'query': 'Himatnagar, Gujarat, India'},
    'himatnagar': {'district': 'Sabarkantha', 'city': 'Himatnagar', 'region': 'North Gujarat', 'query': 'Himatnagar, Gujarat, India'},
    'surat': {'district': 'Surat', 'city': 'Surat', 'region': 'South Gujarat', 'query': 'Surat, Gujarat, India'},
    'surendranagar': {'district': 'Surendranagar', 'city': 'Surendranagar', 'region': 'Saurashtra', 'query': 'Surendranagar, Gujarat, India'},
    'tapi': {'district': 'Tapi', 'city': 'Vyara', 'region': 'South Gujarat', 'query': 'Vyara, Gujarat, India'},
    'vyara': {'district': 'Tapi', 'city': 'Vyara', 'region': 'South Gujarat', 'query': 'Vyara, Gujarat, India'},
    'vadodara': {'district': 'Vadodara', 'city': 'Vadodara', 'region': 'Central Gujarat', 'query': 'Vadodara, Gujarat, India'},
    'baroda': {'district': 'Vadodara', 'city': 'Vadodara', 'region': 'Central Gujarat', 'query': 'Vadodara, Gujarat, India'},
    'valsad': {'district': 'Valsad', 'city': 'Valsad', 'region': 'South Gujarat', 'query': 'Valsad, Gujarat, India'},
    'vapi': {'district': 'Valsad', 'city': 'Vapi', 'region': 'South Gujarat', 'query': 'Vapi, Gujarat, India'},
    'palanpur': {'district': 'Banaskantha', 'city': 'Palanpur', 'region': 'North Gujarat', 'query': 'Palanpur, Gujarat, India'},
    'deesa': {'district': 'Banaskantha', 'city': 'Deesa', 'region': 'North Gujarat', 'query': 'Deesa, Gujarat, India'},
    'ankleshwar': {'district': 'Bharuch', 'city': 'Ankleshwar', 'region': 'South Gujarat', 'query': 'Ankleshwar, Gujarat, India'},
    'mahuva': {'district': 'Bhavnagar', 'city': 'Mahuva', 'region': 'Saurashtra', 'query': 'Mahuva, Gujarat, India'},
    'ahwa': {'district': 'Dang', 'city': 'Ahwa', 'region': 'South Gujarat', 'query': 'Ahwa, Gujarat, India'},
    'modasa': {'district': 'Aravalli', 'city': 'Modasa', 'region': 'North Gujarat', 'query': 'Modasa, Gujarat, India'},
}


def home_view(request):
    """
    Landing Home Page localized to Gujarat, India agriculture.
    Displays live statistics calculated dynamically from PostgreSQL database.
    """
    total_farmers = User.objects.filter(is_staff=False).count() or User.objects.count()
    verified_farmers = User.objects.filter(is_active=True, is_staff=False).count() or User.objects.filter(is_active=True).count()
    total_crops_managed = Crop.objects.count()
    total_area_agg = Crop.objects.aggregate(total=Sum('farm_area'))
    total_farm_area = total_area_agg['total'] or 0.0

    # Featured Gujarat Agricultural Crops
    featured_gujarat_crops = [
        {
            'name': 'Cotton (કપાસ)',
            'type': 'Cash Crop / White Gold',
            'season': 'Kharif (Monsoon)',
            'region': 'Saurashtra & North Gujarat',
            'water': '600 - 800 mm',
            'soil': 'Deep Black Cotton Soil (Regur)',
            'icon': 'fa-shirt',
            'description': 'Gujarat is India\'s top cotton producing state. Flourishes in Saurashtra and Central Gujarat with drip irrigation and warm sunshine.'
        },
        {
            'name': 'Groundnut (મગફળી)',
            'type': 'Oilseed / Legume',
            'season': 'Kharif / Summer',
            'region': 'Saurashtra (Rajkot, Junagadh, Amreli)',
            'water': '450 - 550 mm',
            'soil': 'Well-drained Sandy Loam',
            'icon': 'fa-shapes',
            'description': 'Prime cash oilseed of Saurashtra. Fixes nitrogen naturally in soil while yielding premium edible groundnut oil and cake.'
        },
        {
            'name': 'Wheat (ઘઉં — Bhalia / Tukdi)',
            'type': 'Cereal / Food Grain',
            'season': 'Rabi (Winter)',
            'region': 'Bhal Region, Ahmedabad & Mehsana',
            'water': '400 - 600 mm (Conserved Monsoon Moisture)',
            'soil': 'Heavy Clayey & Rich Loam',
            'icon': 'fa-wheat-awn',
            'description': 'Renowned GI-tagged Gujarat Bhalia wheat grown on conserved soil moisture without artificial watering, rich in protein.'
        },
        {
            'name': 'Cumin / Jeera (જીરું)',
            'type': 'High-Value Spice',
            'season': 'Rabi (Winter)',
            'region': 'Banaskantha, Patan, Mehsana, Kutch',
            'water': 'Low (150 - 250 mm)',
            'soil': 'Well-drained Light Sandy Loam',
            'icon': 'fa-spa',
            'description': 'Gujarat produces the largest share of India\'s cumin spice. Thrives in cool, dry North Gujarat and Kutch winter climate.'
        },
        {
            'name': 'Castor / Divela (દિવેલા)',
            'type': 'Industrial Oilseed',
            'season': 'Kharif / Rabi',
            'region': 'North & Central Gujarat',
            'water': 'Moderate (400 - 600 mm)',
            'soil': 'Medium Sandy Loam to Clay Loam',
            'icon': 'fa-seedling',
            'description': 'Gujarat is the global leader in castor production, highly tolerant to drought and semi-arid conditions.'
        },
        {
            'name': 'Bajra / Pearl Millet (બાજરી)',
            'type': 'Nutri-Cereal / Dryland Grain',
            'season': 'Kharif / Summer',
            'region': 'Banaskantha, Kutch, Saurashtra',
            'water': 'Low (300 - 450 mm)',
            'soil': 'Drought-tolerant Sandy Soil',
            'icon': 'fa-bowl-rice',
            'description': 'Nutritious drought-hardy grain traditional to rural Gujarat, essential for food security and livestock fodder.'
        }
    ]

    context = {
        'page_title': 'AgriConnect — Smart Farming Platform for Gujarat',
        'active_page': 'home',
        'total_farmers': total_farmers,
        'verified_farmers': verified_farmers,
        'total_crops_managed': total_crops_managed,
        'total_farm_area': total_farm_area,
        'featured_crops': featured_gujarat_crops,
    }
    return render(request, 'farming/home.html', context)


def about_view(request):
    """
    About AgriConnect: Gujarat-focused digital agricultural management platform,
    empowering Saurashtra, North Gujarat, Central Gujarat, South Gujarat, and Kutch.
    """
    context = {
        'page_title': 'About Gujarat Agriculture & AgriConnect | AgriConnect',
        'active_page': 'about',
    }
    return render(request, 'farming/about.html', context)


def crops_view(request):
    """
    Gujarat Crop Catalog displaying essential agricultural crops of Gujarat with
    detailed specifications (Region, Season, Water Requirement, Soil Type, Description).
    """
    crops_catalog = [
        {
            'name': 'Cotton (કપાસ)',
            'type': 'Cash Crop / Fiber',
            'region': 'Saurashtra, Central Gujarat, North Gujarat',
            'season': 'Kharif (Monsoon)',
            'water': 'Moderate (600 - 800 mm)',
            'soil': 'Deep Black Cotton Soil (Regur)',
            'duration': '150 - 180 Days',
            'image': 'cotton.jpg',
            'icon': 'fa-shirt',
            'badge_color': 'tag-blue',
            'description': 'The premier commercial crop of Gujarat, leading nationwide production. Extensively cultivated across Rajkot, Surendranagar, Bhavnagar, and Vadodara.'
        },
        {
            'name': 'Groundnut (મગફળી)',
            'type': 'Oilseed / Legume',
            'region': 'Saurashtra (Rajkot, Junagadh, Amreli, Jamnagar)',
            'season': 'Kharif / Summer',
            'water': 'Low to Moderate (400 - 500 mm)',
            'soil': 'Well-aerated Sandy Loam with Calcium',
            'duration': '105 - 125 Days',
            'image': 'groundnut.jpg',
            'icon': 'fa-shapes',
            'badge_color': 'tag-brown',
            'description': 'The backbone of Saurashtra\'s agrarian economy. Enriches soil fertility through atmospheric nitrogen fixation and produces top-grade cooking oil.'
        },
        {
            'name': 'Wheat (ઘઉં — Bhalia & Tukdi)',
            'type': 'Cereal / Grain',
            'region': 'Bhal Region, Ahmedabad, Mehsana, Anand',
            'season': 'Rabi (Winter)',
            'water': 'Moderate (400 - 600 mm)',
            'soil': 'Heavy Clayey & Well-drained Loam',
            'duration': '110 - 130 Days',
            'image': 'wheat.jpg',
            'icon': 'fa-wheat-awn',
            'badge_color': 'tag-gold',
            'description': 'Important Rabi crop in Gujarat. Includes the famed GI-tagged Daudkhani/Bhalia wheat grown naturally on conserved monsoon soil moisture in the Bhal tract.'
        },
        {
            'name': 'Bajra (બાજરી — Pearl Millet)',
            'type': 'Cereal / Dryland Grain',
            'region': 'Banaskantha, Kutch, Sabarkantha, Mehsana',
            'season': 'Kharif & Summer',
            'water': 'Low (250 - 400 mm)',
            'soil': 'Light Sandy Loam to Poor Soils',
            'duration': '75 - 90 Days',
            'image': 'bajra.jpg',
            'icon': 'fa-seedling',
            'badge_color': 'tag-amber',
            'description': 'Primary staple dryland crop of North Gujarat and Kutch. Highly heat and drought tolerant, rich in iron, zinc, and dietary fiber.'
        },
        {
            'name': 'Cumin / Jeera (જીરું)',
            'type': 'High-Value Spice / Seed',
            'region': 'Banaskantha, Patan, Mehsana, Kutch, Surendranagar',
            'season': 'Rabi (Winter)',
            'water': 'Low (150 - 250 mm)',
            'soil': 'Well-drained Sandy Loam with good aeration',
            'duration': '100 - 120 Days',
            'image': 'cumin.jpg',
            'icon': 'fa-spa',
            'badge_color': 'tag-green',
            'description': 'Unjha in North Gujarat is Asia\'s largest cumin trading hub. Requires cool, dry, frost-free weather and careful moisture management to prevent wilt.'
        },
        {
            'name': 'Castor / Divela (દિવેલા / એરંડા)',
            'type': 'Industrial Oilseed',
            'region': 'North Gujarat, Central Gujarat, Saurashtra',
            'season': 'Kharif / Rabi',
            'water': 'Moderate (400 - 600 mm)',
            'soil': 'Well-drained Medium Sandy Loam',
            'duration': '150 - 180 Days',
            'image': 'castor.jpg',
            'icon': 'fa-seedling',
            'badge_color': 'tag-brown',
            'description': 'Gujarat commands over 80% of India\'s castor production. Crucial commercial crop yielding specialized oil for industrial, medicinal, and lubricant uses.'
        },
        {
            'name': 'Sesame / Til (તલ)',
            'type': 'Oilseed',
            'region': 'Saurashtra (Amreli, Bhavnagar), Kutch',
            'season': 'Kharif / Summer',
            'water': 'Low (300 - 450 mm)',
            'soil': 'Well-drained Fertile Light Loam',
            'duration': '80 - 100 Days',
            'image': 'sesame.jpg',
            'icon': 'fa-leaf',
            'badge_color': 'tag-gold',
            'description': 'High-value oilseed crop extensively exported from Gujarat. White sesame (tal) produces premium edible oil and confectionery seeds.'
        },
        {
            'name': 'Maize / Makai (મકાઈ)',
            'type': 'Cereal / Food & Fodder',
            'region': 'Dahod, Panchmahal, Sabarkantha, Aravalli',
            'season': 'Kharif & Rabi',
            'water': 'Moderate (500 - 700 mm)',
            'soil': 'Fertile Deep Loamy Soil',
            'duration': '90 - 110 Days',
            'image': 'maize.jpg',
            'icon': 'fa-cubes-stacked',
            'badge_color': 'tag-amber',
            'description': 'Major tribal and agrarian grain crop of Eastern Gujarat (Dahod, Panchmahal). Serves as staple food, poultry feed, and starch manufacturing material.'
        },
        {
            'name': 'Rice / Paddy (ડાંગર)',
            'type': 'Cereal / Food Grain',
            'region': 'Kheda, Anand, Ahmedabad, South Gujarat (Surat, Navsari)',
            'season': 'Kharif (Monsoon)',
            'water': 'High (1000 - 1400 mm)',
            'soil': 'Clayey Loam & Alluvial Soil',
            'duration': '115 - 140 Days',
            'image': 'rice.jpg',
            'icon': 'fa-bowl-rice',
            'badge_color': 'tag-green',
            'description': 'Grown in canal-irrigated command areas of Central Gujarat (Charotar) and high-rainfall South Gujarat belts, featuring fragrant varieties like Gurjari and GR-11.'
        },
        {
            'name': 'Sugarcane (શેરડી)',
            'type': 'Cash Crop / Commercial',
            'region': 'South Gujarat (Surat, Navsari, Valsad, Bharuch, Narmada)',
            'season': 'Year-Round (Perennial)',
            'water': 'High (1500 - 2200 mm)',
            'soil': 'Heavy Alluvial Soil with Good Drainage',
            'duration': '300 - 365 Days',
            'image': 'sugarcane.jpg',
            'icon': 'fa-cubes',
            'badge_color': 'tag-green',
            'description': 'Cornerstone of South Gujarat\'s cooperative sugar industry. Requires tropical humid climate, canal/drip water, and rich organic nutrition.'
        },
        {
            'name': 'Onion (ડુંગળી)',
            'type': 'Vegetable / Bulb',
            'region': 'Bhavnagar (Mahuva), Junagadh, Rajkot',
            'season': 'Kharif / Late Kharif / Rabi',
            'water': 'Regular Light Irrigation (350 - 500 mm)',
            'soil': 'Well-drained Silty Loam rich in organic matter',
            'duration': '110 - 130 Days',
            'image': 'onion.jpg',
            'icon': 'fa-circle-dot',
            'badge_color': 'tag-red',
            'description': 'Mahuva in Bhavnagar district is India\'s largest white onion dehydration center. Red and white onion varieties are grown extensively across Saurashtra.'
        },
        {
            'name': 'Tomato (ટામેટા)',
            'type': 'Horticulture / Vegetable',
            'region': 'Central Gujarat, Kheda, Anand, Surat',
            'season': 'Year-Round (Kharif / Rabi)',
            'water': 'Controlled Drip (400 - 600 mm)',
            'soil': 'Well-drained Sandy Loam to Clay Loam',
            'duration': '80 - 120 Days',
            'image': 'tomato.jpg',
            'icon': 'fa-apple-whole',
            'badge_color': 'tag-red',
            'description': 'Important vegetable cash crop grown with staking and mulching in Central and South Gujarat for local APMC markets and processing.'
        },
        {
            'name': 'Tobacco (તમાકુ)',
            'type': 'Commercial Cash Crop',
            'region': 'Charotar Belt (Anand, Kheda, Vadodara)',
            'season': 'Rabi (Winter)',
            'water': 'Moderate (400 - 550 mm)',
            'soil': 'Goradu (Sandy Loam) Soils',
            'duration': '120 - 140 Days',
            'image': 'tobacco.jpg',
            'icon': 'fa-leaf',
            'badge_color': 'tag-gold',
            'description': 'Specialty crop of the fertile Charotar tract in Central Gujarat. Thrives in sandy-loam Goradu soils under well-managed winter conditions.'
        },
        {
            'name': 'Chickpea / Chana (ચણા)',
            'type': 'Pulse / Legume',
            'region': 'Saurashtra, Bhal, Central Gujarat',
            'season': 'Rabi (Winter)',
            'water': 'Low (200 - 350 mm)',
            'soil': 'Medium to Deep Black Soils',
            'duration': '90 - 110 Days',
            'image': 'chickpea.jpg',
            'icon': 'fa-seedling',
            'badge_color': 'tag-amber',
            'description': 'Major winter pulse crop of Gujarat. Natural nitrogen builder that thrives on residual soil moisture after Kharif harvest.'
        }
    ]

    context = {
        'page_title': 'Gujarat Crops Catalog | AgriConnect',
        'active_page': 'crops',
        'crops': crops_catalog,
    }
    return render(request, 'farming/crops.html', context)


def seed_default_tips_if_empty():
    """
    Seeds comprehensive Gujarat farming best practices across 10 agricultural categories.
    """
    if FarmingTip.objects.exists():
        return
    default_tips = [
        # Soil Preparation
        ('Soil Preparation', 'Deep Summer Plowing for Pest Reduction', 'Plow Saurashtra and North Gujarat soils deeply during May-June to expose white grub larvae, fungal pathogens, and weed roots to intense heat.', 'Essential', 'fa-mountain-sun'),
        ('Soil Preparation', 'Goradu & Black Cotton Soil Amendment', 'Apply 8-10 tonnes of FYM per acre in black cotton soils to improve drainage and prevent surface crusting during early monsoon rains.', 'Soil Health', 'fa-mountain-sun'),
        ('Soil Preparation', 'Soil Health Card Testing', 'Conduct soil nutrient analysis every 2-3 years at local Krishi Vigyan Kendra (KVK) to assess EC, pH, and zinc/iron micronutrient deficiencies.', 'Essential', 'fa-mountain-sun'),
        
        # Irrigation & Drip Technology
        ('Irrigation', 'Adopt GGRC Micro-Irrigation / Drip', 'Install drip irrigation for cotton, groundnut, and vegetable crops to save 40-60% water while maximizing fertigation efficiency in water-scarce zones.', 'Water-Saver', 'fa-faucet-drip'),
        ('Irrigation', 'Critical Stage Irrigation Scheduling', 'Ensure irrigation during flowering and pegging stages in groundnut and boll formation in cotton to prevent drastic yield drops.', 'Yield Booster', 'fa-faucet-drip'),
        
        # Water Management
        ('Water Management', 'Farm Ponds (Khet Talavadi) Rainwater Harvesting', 'Construct farm ponds to capture monsoon runoff for critical life-saving supplemental irrigation during dry spells in Saurashtra and Kutch.', 'Drought Shield', 'fa-hand-holding-droplet'),
        ('Water Management', 'Plastic / Organic Mulching', 'Use silver-black plastic mulch or groundnut shell mulch in dry regions to suppress evaporative loss and regulate root-zone temperature.', 'Moisture Shield', 'fa-hand-holding-droplet'),
        
        # Fertilizer & Soil Nutrition
        ('Fertilizer', 'Balanced N-P-K & Zinc Application', 'Avoid excess nitrogen (Urea) in cotton to prevent vegetative rank growth. Supplement with Zinc Sulphate (25 kg/ha) for high boll retention.', 'Balanced', 'fa-flask-vial'),
        ('Fertilizer', 'Split Fertigation Dosing', 'Deliver water-soluble fertilizers (19:19:19, 12:61:00, 0:0:50) through drip lines in 4-6 split doses to prevent nutrient leaching in sandy soils.', 'Technique', 'fa-flask-vial'),
        
        # Pest & Disease Control
        ('Pest Control', 'Pink Bollworm Management in Cotton', 'Install pheromone traps (5 traps/acre) and release Trichogramma egg parasitoids. Avoid prolonged ratoon cotton crops.', 'IPM Practice', 'fa-shield-virus'),
        ('Pest Control', 'White Grub & Stem Rot Control in Groundnut', 'Seed treatment with Trichoderma viride (10g/kg) and soil drenching with Metarhizium anisopliae to protect groundnut roots.', 'Biological', 'fa-shield-virus'),
        ('Pest Control', 'Cumin Wilt & Blight Protection', 'Treat cumin seeds with Carbendazim + Thiram and avoid flood irrigation during cloudy, humid North Gujarat weather.', 'Preventive', 'fa-shield-virus'),
        
        # Crop Rotation
        ('Crop Rotation', 'Rotate Cotton with Groundnut / Pulses', 'Rotate heavy-feeding cotton crops with nitrogen-fixing groundnut or green gram (Moong) to rejuvenate soil fertility.', 'Soil Renewal', 'fa-arrows-rotate'),
        ('Crop Rotation', 'Green Manuring with Dhaincha (IKAD)', 'Sow Dhaincha or Sunn hemp with pre-monsoon showers and incorporate into the soil after 45 days before planting Rabi crops.', 'Organic Nitrogen', 'fa-arrows-rotate'),
        
        # Organic Farming (Prakrutik Kheti)
        ('Organic Farming', 'Jeevamrutha Preparation & Application', 'Prepare Jeevamrutha using Desi Gir cow dung, urine, jaggery, and gram flour. Apply with irrigation water every 15 days to activate soil microbes.', 'Prakrutik Kheti', 'fa-leaf'),
        ('Organic Farming', 'Neemastra & Brahmastra Natural Pesticides', 'Use boiling neem leaves, cow urine, and local bitter herbs for effective sucking pest control without chemical residues.', 'Bio-Shield', 'fa-leaf'),
        
        # Monsoon Farming (Kharif Season)
        ('Monsoon Farming', 'Timely Sowing with 75-100 mm Rain', 'Sow Kharif groundnut and cotton only after the soil receives at least 75-100 mm of steady soaking monsoon rainfall to ensure uniform germination.', 'Kharif Guideline', 'fa-cloud-showers-heavy'),
        ('Monsoon Farming', 'Broad Bed Furrow (BBF) Drainage', 'Adopt Broad Bed Furrow system in heavy clay soils to drain excess water during heavy Saurashtra/South Gujarat rains while retaining sub-soil moisture.', 'Field Drainage', 'fa-cloud-showers-heavy'),
        
        # Winter Farming (Rabi Season)
        ('Rabi Farming', 'Optimal Sowing Window for Wheat & Cumin', 'Sow Rabi wheat between 15th to 30th November when minimum temperatures drop below 20°C for optimal tillering and grain weight.', 'Rabi Guideline', 'fa-snowflake'),
        ('Rabi Farming', 'Cold Wave & Frost Protection in North Gujarat', 'Apply light evening irrigation during cold wave alerts to raise canopy temperature and protect tender cumin/mustard blossoms.', 'Frost Shield', 'fa-snowflake'),
    ]
    for cat, title, desc, lvl, icon in default_tips:
        FarmingTip.objects.create(
            category=cat,
            title=title,
            description=desc,
            level=lvl,
            icon=icon
        )


def farming_tips_view(request):
    """
    Actionable agricultural tips categorized by domain for Gujarat farmers.
    Loaded dynamically from database with automatic fallback seeding.
    """
    seed_default_tips_if_empty()

    category_slug_map = {
        'Soil Preparation': ('soil', 'fa-mountain-sun'),
        'Irrigation': ('irrigation', 'fa-faucet-drip'),
        'Water Management': ('water', 'fa-hand-holding-droplet'),
        'Fertilizer': ('fertilizer', 'fa-flask-vial'),
        'Fertilizer & Nutrition': ('fertilizer', 'fa-flask-vial'),
        'Pest Control': ('pest', 'fa-shield-virus'),
        'Pest & Disease Control': ('pest', 'fa-shield-virus'),
        'Crop Rotation': ('rotation', 'fa-arrows-rotate'),
        'Organic Farming': ('organic', 'fa-leaf'),
        'Monsoon Farming': ('monsoon', 'fa-cloud-showers-heavy'),
        'Rabi Farming': ('rabi', 'fa-snowflake'),
        'Kharif Farming': ('kharif', 'fa-seedling'),
    }

    all_tips = FarmingTip.objects.all().order_by('category', '-created_at')
    category_dict = {}

    for tip in all_tips:
        cat_name = tip.category
        if cat_name not in category_dict:
            slug, default_icon = category_slug_map.get(cat_name, (cat_name.lower().replace(' ', '-'), tip.icon or 'fa-seedling'))
            category_dict[cat_name] = {
                'slug': slug,
                'name': cat_name,
                'icon': default_icon,
                'tips': []
            }
        category_dict[cat_name]['tips'].append({
            'title': tip.title,
            'text': tip.description,
            'level': tip.level,
            'icon': tip.icon,
            'image': tip.image.url if tip.image else None,
        })

    categories = list(category_dict.values())

    context = {
        'page_title': 'Gujarat Farming Tips & Best Practices | AgriConnect',
        'active_page': 'tips',
        'categories': categories,
    }
    return render(request, 'farming/farming_tips.html', context)


def get_gujarat_location_info(query):
    """
    Validates whether the provided query belongs to Gujarat.
    Returns normalized dictionary or None if location is outside Gujarat.
    """
    if not query or not str(query).strip():
        return GUJARAT_LOCATIONS_MAP['ahmedabad']
    q = str(query).strip().lower()
    q_clean = q.replace(', gujarat, india', '').replace(', gujarat', '').replace(', india', '').replace(' district', '').strip()
    
    if q_clean in GUJARAT_LOCATIONS_MAP:
        return GUJARAT_LOCATIONS_MAP[q_clean]
    
    for key, info in GUJARAT_LOCATIONS_MAP.items():
        if key == q_clean:
            return info
        if len(q_clean) >= 3 and (key.startswith(q_clean) or q_clean.startswith(key)):
            return info
            
    return None


def generate_farming_weather_advice(temp_c, feels_like, humidity, wind_kph, rain_chance, precip_mm, condition_text, region_name):
    """
    Generates dynamic agronomic advisories and general suggestions from live weather metrics.
    """
    advice_items = []
    
    # 1. Rain & Irrigation Advisory
    if rain_chance >= 55 or precip_mm >= 3.0:
        advice_items.append({
            'icon': 'fa-cloud-showers-heavy',
            'type': 'warning',
            'title': 'Rain Expected — Delay Irrigation',
            'text': f'Rain probability is elevated at {rain_chance}% (expected {precip_mm} mm). Delay scheduled canal/drip irrigation and inspect field drainage channels to prevent water stagnation.'
        })
    elif rain_chance >= 30:
        advice_items.append({
            'icon': 'fa-cloud-rain',
            'type': 'info',
            'title': 'Moderate Rain Chance — Monitor Soil Moisture',
            'text': f'Scattered rain chance ({rain_chance}%). Check active soil moisture in standing crops before running drip irrigation.'
        })
    else:
        advice_items.append({
            'icon': 'fa-droplet',
            'type': 'success',
            'title': 'Dry / Low Rain Probability — Regular Irrigation',
            'text': f'Low rain chance ({rain_chance}%). Continue regular irrigation scheduling for cotton, groundnut, vegetables, and fodder crops.'
        })

    # 2. Wind & Spraying Advisory
    if wind_kph >= 22:
        advice_items.append({
            'icon': 'fa-wind',
            'type': 'danger',
            'title': 'Strong Winds — Avoid Foliar Spraying',
            'text': f'Wind speeds are high at {wind_kph} km/h. Avoid pesticide, bio-fungicide, and foliar fertilizer sprays to prevent chemical drift and wastage.'
        })
    elif wind_kph >= 15:
        advice_items.append({
            'icon': 'fa-wind',
            'type': 'info',
            'title': 'Breezy Weather — Spray During Calm Morning Hours',
            'text': f'Moderate wind speed ({wind_kph} km/h). Conduct any necessary foliar spraying during calm early morning or late evening hours.'
        })
    else:
        advice_items.append({
            'icon': 'fa-spray-can-sparkles',
            'type': 'success',
            'title': 'Calm Winds — Favorable for Crop Spraying',
            'text': f'Gentle breeze ({wind_kph} km/h). Atmospheric conditions are optimal for micronutrient and protective bio-pesticide applications.'
        })

    # 3. Temperature & Heat Stress Advisory
    if temp_c >= 38 or feels_like >= 40:
        advice_items.append({
            'icon': 'fa-temperature-arrow-up',
            'type': 'danger',
            'title': 'High Temperature Alert — Protect Crops from Heat Stress',
            'text': f'Intense heat ({temp_c}°C, feels like {feels_like}°C). Irrigate early morning or post-sunset to prevent moisture evaporation and crop wilting.'
        })
    elif temp_c <= 15:
        advice_items.append({
            'icon': 'fa-temperature-arrow-down',
            'type': 'info',
            'title': 'Cool Temperature — Favorable for Rabi Crops',
            'text': f'Cool atmospheric temperature ({temp_c}°C). Ideal for wheat, mustard, and cumin tillering. Protect young seedlings from cold drafts.'
        })
    else:
        advice_items.append({
            'icon': 'fa-sun',
            'type': 'success',
            'title': 'Suitable Thermal Range — Normal Field Operations',
            'text': f'Comfortable temperature ({temp_c}°C). Favorable for weeding, intercultural operations, and fertilizer top-dressing.'
        })

    # 4. Humidity & Disease Advisory
    if humidity >= 75:
        advice_items.append({
            'icon': 'fa-shield-virus',
            'type': 'warning',
            'title': 'High Humidity Alert — Inspect for Fungal Pathogens',
            'text': f'High humidity ({humidity}%) promotes fungal mildew, blight, and sucking pest activity. Inspect crop canopy and keep neem-based bio-pesticides ready.'
        })
    elif humidity <= 35 and temp_c >= 30:
        advice_items.append({
            'icon': 'fa-seedling',
            'type': 'warning',
            'title': 'Dry Atmospheric Air — Maintain Soil Mulch',
            'text': f'Dry conditions ({humidity}% humidity). Maintain organic straw or plastic mulch to conserve root-zone soil moisture.'
        })

    return {
        'title': 'Farming Weather Advice',
        'region': region_name,
        'summary': f'Live agricultural advisory based on real-time {condition_text} conditions in {region_name}.',
        'items': advice_items,
        'disclaimer': 'These are automated general informational suggestions based on atmospheric data. Please evaluate local field conditions, crop maturity, and soil moisture before performing critical farm operations.'
    }


def fetch_gujarat_weather(city_query):
    """
    Fetches real-time weather and 5-day forecast from WeatherAPI.com for Gujarat locations.
    Keeps API key server-side, validates Gujarat whitelist, caches response for 10 minutes.
    """
    location_info = get_gujarat_location_info(city_query)
    if not location_info:
        return {
            'success': False,
            'error': 'AgriConnect provides weather information only for Gujarat.'
        }

    canonical_city = location_info['city']
    cache_key = f"agri_weatherapi_{canonical_city.lower()}"
    cached_payload = cache.get(cache_key)
    if cached_payload:
        return cached_payload

    api_key = getattr(settings, 'WEATHER_API_KEY', '') or os.getenv('WEATHER_API_KEY', '')
    if not api_key:
        return {
            'success': False,
            'error': 'Weather information is temporarily unavailable. Please try again.'
        }

    try:
        query_param = location_info['query']
        encoded_q = urllib.parse.quote(query_param)
        api_url = f"https://api.weatherapi.com/v1/forecast.json?key={api_key}&q={encoded_q}&days=5&aqi=no&alerts=no"
        req = urllib.request.Request(
            api_url,
            headers={
                'User-Agent': 'AgriConnect-Django/1.0',
                'Accept': 'application/json'
            }
        )

        with urllib.request.urlopen(req, timeout=8) as response:
            if response.status != 200:
                return {
                    'success': False,
                    'error': 'Weather information is temporarily unavailable. Please try again.'
                }
            raw_data = json.loads(response.read().decode('utf-8'))

        # Validate location returned is in Gujarat, India
        loc = raw_data.get('location', {})
        api_region = str(loc.get('region', '')).strip().lower()
        api_country = str(loc.get('country', '')).strip().lower()

        is_gujarat = 'gujarat' in api_region or api_region in ('agol', 'gujarat state') or api_country == 'india'
        if not is_gujarat:
            return {
                'success': False,
                'error': 'AgriConnect provides weather information only for Gujarat.'
            }

        curr = raw_data.get('current', {})
        forecast_days = raw_data.get('forecast', {}).get('forecastday', [])

        temp_c = round(float(curr.get('temp_c', 0)), 1)
        feels_like = round(float(curr.get('feelslike_c', temp_c)), 1)
        cond_text = curr.get('condition', {}).get('text', 'Clear')
        cond_icon = curr.get('condition', {}).get('icon', '')
        if cond_icon.startswith('//'):
            cond_icon = 'https:' + cond_icon

        humidity = int(curr.get('humidity', 0))
        wind_kph = round(float(curr.get('wind_kph', 0)), 1)
        wind_dir = curr.get('wind_dir', 'N')
        pressure_mb = round(float(curr.get('pressure_mb', 1013)), 1)
        vis_km = round(float(curr.get('vis_km', 10.0)), 1)
        uv_val = curr.get('uv', 0)
        cloud_val = int(curr.get('cloud', 0))
        precip_mm = round(float(curr.get('precip_mm', 0.0)), 2)

        # Process 5-day forecast
        forecast_list = []
        today_rain_chance = 0
        today_precip = 0.0

        for i, fd in enumerate(forecast_days[:5]):
            f_date_str = fd.get('date', '')
            try:
                dt = datetime.strptime(f_date_str, '%Y-%m-%d')
                if i == 0:
                    day_name = 'Today'
                elif i == 1:
                    day_name = 'Tomorrow'
                else:
                    day_name = dt.strftime('%A')
                formatted_date = dt.strftime('%d %b')
            except Exception:
                day_name = f'Day {i+1}'
                formatted_date = f_date_str

            day_obj = fd.get('day', {})
            f_max = round(float(day_obj.get('maxtemp_c', 0)), 1)
            f_min = round(float(day_obj.get('mintemp_c', 0)), 1)
            f_rain_chance = int(day_obj.get('daily_chance_of_rain', 0))
            f_precip = round(float(day_obj.get('totalprecip_mm', 0.0)), 1)
            f_cond_text = day_obj.get('condition', {}).get('text', 'Sunny')
            f_cond_icon = day_obj.get('condition', {}).get('icon', '')
            if f_cond_icon.startswith('//'):
                f_cond_icon = 'https:' + f_cond_icon

            if i == 0:
                today_rain_chance = f_rain_chance
                today_precip = f_precip

            forecast_list.append({
                'date': f_date_str,
                'formatted_date': formatted_date,
                'day_name': day_name,
                'max_temp': f_max,
                'min_temp': f_min,
                'rain_chance': f_rain_chance,
                'precip_mm': f_precip,
                'condition': f_cond_text,
                'icon': f_cond_icon,
                'max_wind_kph': round(float(day_obj.get('maxwind_kph', 0)), 1),
                'avg_humidity': int(day_obj.get('avghumidity', 0)),
                'uv': day_obj.get('uv', 0),
            })

        advice = generate_farming_weather_advice(
            temp_c=temp_c,
            feels_like=feels_like,
            humidity=humidity,
            wind_kph=wind_kph,
            rain_chance=today_rain_chance or (int(precip_mm > 0) * 50),
            precip_mm=today_precip or precip_mm,
            condition_text=cond_text,
            region_name=location_info['region']
        )

        result = {
            'success': True,
            'city': location_info['city'],
            'district': location_info['district'],
            'region': location_info['region'],
            'state': 'Gujarat',
            'country': 'India',
            'location_display': f"{location_info['city']}, {location_info['district']} (Gujarat, India)",
            'temperature': temp_c,
            'feels_like': feels_like,
            'condition': cond_text,
            'condition_icon': cond_icon,
            'humidity': humidity,
            'wind_speed': wind_kph,
            'wind_dir': wind_dir,
            'pressure': pressure_mb,
            'visibility': vis_km,
            'uv_index': uv_val,
            'cloud_cover': cloud_val,
            'precipitation': precip_mm,
            'is_day': curr.get('is_day', 1),
            'last_updated': curr.get('last_updated', ''),
            'forecast': forecast_list,
            'farming_advice': advice
        }

        cache.set(cache_key, result, timeout=600)
        return result

    except urllib.error.HTTPError:
        return {
            'success': False,
            'error': 'Weather information is temporarily unavailable. Please try again.'
        }
    except urllib.error.URLError:
        return {
            'success': False,
            'error': 'Weather information is temporarily unavailable. Please check your internet connection.'
        }
    except Exception:
        return {
            'success': False,
            'error': 'Weather information is temporarily unavailable. Please try again.'
        }


def api_weather_view(request):
    """
    JSON API endpoint for Gujarat Agricultural Weather.
    GET /api/weather/?city=Ahmedabad
    Restricts access strictly to Gujarat locations.
    """
    city_query = request.GET.get('city', 'Ahmedabad').strip()
    data = fetch_gujarat_weather(city_query)
    
    status_code = 200 if data.get('success') else 400
    return JsonResponse(data, status=status_code)


def weather_view(request):
    """
    Gujarat Agricultural Weather Page:
    Loads real live WeatherAPI.com weather & 5-day forecast for Gujarat locations.
    Defaults to Ahmedabad, Gujarat, India.
    """
    city_query = request.GET.get('city', 'Ahmedabad').strip() or 'Ahmedabad'
    
    # Server-side validation of Gujarat location
    loc_info = get_gujarat_location_info(city_query)
    if not loc_info:
        messages.warning(request, f"'{city_query}' is outside Gujarat. AgriConnect provides weather information only for Gujarat. Showing weather for Ahmedabad, Gujarat.")
        city_query = 'Ahmedabad'
        loc_info = GUJARAT_LOCATIONS_MAP['ahmedabad']
        
    initial_weather = fetch_gujarat_weather(loc_info['city'])
    
    context = {
        'page_title': f'Gujarat Weather ({loc_info["district"]}) | AgriConnect',
        'active_page': 'weather',
        'selected_district': loc_info['district'],
        'selected_city': loc_info['city'],
        'city_query': loc_info['city'],
        'gujarat_districts': GUJARAT_DISTRICTS_LIST,
        'initial_weather': initial_weather,
    }
    return render(request, 'farming/weather.html', context)


def send_admin_contact_notification(contact_msg):
    """
    Dispatches rich HTML & Plain-Text notification email to Admin upon visitor message.
    Uses ADMIN_EMAIL setting.
    """
    admin_email = getattr(settings, 'ADMIN_EMAIL', None) or getattr(settings, 'EMAIL_HOST_USER', None) or 'admin@example.com'
    subject = f"New AgriConnect Contact Message: {contact_msg.subject}"

    text_content = (
        f"You have received a new contact message from AgriConnect.\n\n"
        f"Name: {contact_msg.name}\n"
        f"Email: {contact_msg.email}\n"
        f"Subject: {contact_msg.subject}\n\n"
        f"Message:\n{contact_msg.message}\n\n"
        f"Login to the AgriConnect Admin Dashboard to view and manage this message."
    )

    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>New AgriConnect Contact Message</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #F7FAF7; margin: 0; padding: 24px 12px; color: #1F2937; line-height: 1.6; }}
        .email-container {{ max-width: 580px; margin: 0 auto; background: #ffffff; border-radius: 14px; overflow: hidden; box-shadow: 0 8px 24px rgba(27, 94, 32, 0.12); border: 1px solid #E5E7EB; }}
        .email-header {{ background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%); color: #ffffff; padding: 24px; text-align: center; }}
        .email-body {{ padding: 28px 24px; }}
        .badge {{ display: inline-block; background: #E8F5E9; color: #1B5E20; font-weight: 700; font-size: 12px; padding: 4px 10px; border-radius: 20px; }}
        .info-table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        .info-table td {{ padding: 8px 12px; border-bottom: 1px solid #F3F4F6; }}
        .info-table td.label {{ width: 100px; font-weight: 600; color: #4B5563; }}
        .msg-box {{ background: #F9FAFB; border-left: 4px solid #1B5E20; padding: 16px; border-radius: 6px; margin: 18px 0; white-space: pre-wrap; }}
        .email-footer {{ background: #F9FAFB; padding: 18px; text-align: center; font-size: 12px; color: #6B7280; border-top: 1px solid #E5E7EB; }}
    </style>
</head>
<body>
    <div class="email-container">
        <div class="email-header">
            <h2 style="margin:0; font-size:22px;">🌱 AgriConnect Admin Notification</h2>
            <p style="margin:4px 0 0; color:#C8E6C9; font-size:13px;">New Contact Inbound Inquiry</p>
        </div>
        <div class="email-body">
            <span class="badge">New Inquiry</span>
            <p>You have received a new contact inquiry from the AgriConnect website:</p>
            <table class="info-table">
                <tr><td class="label">Name:</td><td><strong>{contact_msg.name}</strong></td></tr>
                <tr><td class="label">Email:</td><td><a href="mailto:{contact_msg.email}">{contact_msg.email}</a></td></tr>
                <tr><td class="label">Subject:</td><td><strong>{contact_msg.subject}</strong></td></tr>
            </table>
            <div class="msg-box">{contact_msg.message}</div>
            <p style="font-size: 13px; color: #6B7280;">Login to the AgriConnect Admin Dashboard to view and manage this message.</p>
        </div>
        <div class="email-footer">
            AgriConnect Smart Farming Management System &bull; Automated Admin Notification
        </div>
    </div>
</body>
</html>"""

    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None) or f"AgriConnect <{getattr(settings, 'EMAIL_HOST_USER', 'noreply@agriconnect.com')}>"
    try:
        msg = EmailMultiAlternatives(subject, text_content, from_email, [admin_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=True)
    except Exception:
        pass


def contact_view(request):
    """
    Contact Us page with message submission saved to PostgreSQL database,
    instant Admin email notification dispatch, and activity audit logging.
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_msg = form.save()
            # 1. Dispatch Email to Admin
            send_admin_contact_notification(contact_msg)
            # 2. Log Activity
            log_activity(
                action='Message Received',
                details=f"Inquiry from {contact_msg.name} ({contact_msg.email}): {contact_msg.subject}",
                user=request.user if request.user.is_authenticated else None,
                icon='fa-envelope'
            )
            messages.success(
                request,
                "Thank you for contacting AgriConnect! Your message has been received. Our agriculture support team will respond shortly."
            )
            return redirect('contact')
        else:
            messages.error(request, "Please correct the highlighted errors below before submitting.")
    else:
        form = ContactForm()

    context = {
        'page_title': 'Contact Support | AgriConnect',
        'active_page': 'contact',
        'form': form,
    }
    return render(request, 'farming/contact.html', context)


# ==========================================
# AUTHENTICATION & EMAIL OTP VIEWS
# ==========================================

def send_otp_verification_email(user, raw_otp):
    """
    Dispatches both Plain-Text and Rich HTML 6-Digit Email Verification OTP.
    Follows AgriConnect brand design with green accents and security guidelines.
    """
    subject = "Your AgriConnect Email Verification OTP"
    first_name = user.first_name if user.first_name else user.username

    text_content = (
        f"Hello {first_name},\n\n"
        f"Welcome to AgriConnect!\n\n"
        f"Your email verification OTP is:\n\n"
        f"{raw_otp}\n\n"
        f"This OTP is valid for 3 minutes.\n\n"
        f"Please do not share this OTP with anyone.\n\n"
        f"If you did not create this account, you can safely ignore this email.\n\n"
        f"Regards,\n"
        f"AgriConnect Team\n"
    )

    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AgriConnect Email Verification OTP</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #F7FAF7; margin: 0; padding: 24px 12px; color: #1F2937; line-height: 1.6; }}
        .email-container {{ max-width: 560px; margin: 0 auto; background: #ffffff; border-radius: 16px; overflow: hidden; box-shadow: 0 10px 25px rgba(27, 94, 32, 0.12); border: 1px solid #E5E7EB; }}
        .email-header {{ background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%); color: #ffffff; padding: 32px 24px; text-align: center; }}
        .email-header h1 {{ margin: 0; font-size: 26px; font-weight: 800; letter-spacing: -0.5px; }}
        .email-header p {{ margin: 6px 0 0; font-size: 13px; color: #C8E6C9; font-weight: 500; }}
        .email-body {{ padding: 32px 28px; }}
        .salutation {{ font-size: 18px; font-weight: 700; color: #1B5E20; margin-bottom: 12px; }}
        .otp-container {{ background: #E8F5E9; border: 2px dashed #2E7D32; border-radius: 12px; padding: 24px 16px; text-align: center; margin: 28px 0; }}
        .otp-label {{ font-size: 12px; text-transform: uppercase; letter-spacing: 1.5px; color: #2E7D32; font-weight: 700; margin-bottom: 8px; }}
        .otp-code {{ font-size: 38px; font-weight: 800; letter-spacing: 12px; color: #1B5E20; font-family: 'Courier New', Courier, monospace; margin: 0; padding-left: 12px; }}
        .otp-expiry {{ font-size: 13px; color: #B45309; margin-top: 10px; font-weight: 600; }}
        .security-notice {{ background: #FEF3C7; border-left: 4px solid #F59E0B; padding: 14px 16px; border-radius: 6px; font-size: 13px; color: #92400E; margin: 24px 0 16px; }}
        .email-footer {{ background: #F9FAFB; padding: 24px; text-align: center; border-top: 1px solid #E5E7EB; font-size: 12px; color: #6B7280; }}
    </style>
</head>
<body>
    <div class="email-container">
        <div class="email-header">
            <h1>🌱 AgriConnect</h1>
            <p>Smart Farming Management System</p>
        </div>
        <div class="email-body">
            <div class="salutation">Hello {first_name},</div>
            <p>Welcome to <strong>AgriConnect</strong>! Thank you for registering your farm. To verify your email address and activate your account, please enter the 6-digit verification code below:</p>
            
            <div class="otp-container">
                <div class="otp-label">Your Verification Code</div>
                <div class="otp-code">{raw_otp}</div>
                <div class="otp-expiry">⏱️ Valid for 3 minutes only</div>
            </div>

            <div class="security-notice">
                <strong>Security Notice:</strong> Please do not share this OTP with anyone. AgriConnect staff will never ask for your verification code.
            </div>

            <p style="font-size: 13px; color: #6B7280; margin-top: 20px;">If you did not create an account on AgriConnect, you can safely ignore this email.</p>
        </div>
        <div class="email-footer">
            &copy; 2026 AgriConnect. All Rights Reserved. Smart Farming for a Better Future.<br>
            This is an automated system email. Please do not reply directly to this message.
        </div>
    </div>
</body>
</html>"""

    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None) or f"AgriConnect <{getattr(settings, 'EMAIL_HOST_USER', 'noreply@agriconnect.com')}>"
    msg = EmailMultiAlternatives(subject, text_content, from_email, [user.email])
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=False)


def send_password_reset_otp_email(user, raw_otp):
    """
    Dispatches both Plain-Text and Rich HTML 6-Digit Password Reset OTP.
    Valid for 10 minutes, styled with AgriConnect green branding & security warning.
    """
    subject = "AgriConnect Password Reset OTP"
    first_name = user.first_name if user.first_name else user.username

    text_content = (
        f"Hello,\n\n"
        f"We received a request to reset your AgriConnect account password.\n\n"
        f"Your password reset OTP is:\n\n"
        f"{raw_otp}\n\n"
        f"This OTP is valid for 10 minutes.\n\n"
        f"Do not share this OTP with anyone.\n\n"
        f"If you did not request a password reset, you can safely ignore this email.\n\n"
        f"Regards,\n"
        f"AgriConnect Team\n"
    )

    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AgriConnect Password Reset OTP</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #F7FAF7; margin: 0; padding: 24px 12px; color: #1F2937; line-height: 1.6; }}
        .email-container {{ max-width: 560px; margin: 0 auto; background: #ffffff; border-radius: 16px; overflow: hidden; box-shadow: 0 10px 25px rgba(27, 94, 32, 0.12); border: 1px solid #E5E7EB; }}
        .email-header {{ background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%); color: #ffffff; padding: 32px 24px; text-align: center; }}
        .email-header h1 {{ margin: 0; font-size: 26px; font-weight: 800; letter-spacing: -0.5px; }}
        .email-header p {{ margin: 6px 0 0; font-size: 13px; color: #C8E6C9; font-weight: 500; }}
        .email-body {{ padding: 32px 28px; }}
        .salutation {{ font-size: 18px; font-weight: 700; color: #1B5E20; margin-bottom: 12px; }}
        .otp-container {{ background: #E8F5E9; border: 2px dashed #2E7D32; border-radius: 12px; padding: 24px 16px; text-align: center; margin: 28px 0; }}
        .otp-label {{ font-size: 12px; text-transform: uppercase; letter-spacing: 1.5px; color: #2E7D32; font-weight: 700; margin-bottom: 8px; }}
        .otp-code {{ font-size: 38px; font-weight: 800; letter-spacing: 12px; color: #1B5E20; font-family: 'Courier New', Courier, monospace; margin: 0; padding-left: 12px; }}
        .otp-expiry {{ font-size: 13px; color: #B45309; margin-top: 10px; font-weight: 600; }}
        .security-notice {{ background: #FEF3C7; border-left: 4px solid #F59E0B; padding: 14px 16px; border-radius: 6px; font-size: 13px; color: #92400E; margin: 24px 0 16px; }}
        .email-footer {{ background: #F9FAFB; padding: 24px; text-align: center; border-top: 1px solid #E5E7EB; font-size: 12px; color: #6B7280; }}
    </style>
</head>
<body>
    <div class="email-container">
        <div class="email-header">
            <h1>🌱 AgriConnect</h1>
            <p>Smart Farming Management System</p>
        </div>
        <div class="email-body">
            <div class="salutation">Hello {first_name},</div>
            <p>We received a request to reset your <strong>AgriConnect</strong> account password. To proceed with setting a new password, please enter the 6-digit verification code below:</p>
            
            <div class="otp-container">
                <div class="otp-label">Your Password Reset OTP</div>
                <div class="otp-code">{raw_otp}</div>
                <div class="otp-expiry">⏱️ Valid for 10 minutes only</div>
            </div>

            <div class="security-notice">
                <strong>Security Alert:</strong> Do not share this OTP with anyone. If you did not request a password reset, you can safely ignore this email — your existing password remains unchanged.
            </div>

            <p style="font-size: 13px; color: #6B7280; margin-top: 20px;">If you have concerns about your account security, contact us at support@agriconnect.com.</p>
        </div>
        <div class="email-footer">
            &copy; 2026 AgriConnect. All Rights Reserved. Smart Farming for a Better Future.<br>
            This is an automated system email. Please do not reply directly to this message.
        </div>
    </div>
</body>
</html>"""

    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None) or f"AgriConnect <{getattr(settings, 'EMAIL_HOST_USER', 'noreply@agriconnect.com')}>"
    msg = EmailMultiAlternatives(subject, text_content, from_email, [user.email])
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=False)



def register_view(request):
    """
    Farmer Registration: creates inactive Django User (is_active=False),
    FarmerProfile, generates a secure 6-digit OTP, sends verification email,
    and redirects to OTP verification page.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = FarmerRegistrationForm(request.POST)
        if form.is_valid():
            # 1. Create User with is_active = False
            user = form.save()
            user.is_active = False
            user.save()

            # 2. Invalidate any previous pending OTPs
            EmailVerificationOTP.objects.filter(user=user, is_verified=False).delete()

            # 3. Generate secure 6-digit OTP (3-minute expiration)
            raw_otp = EmailVerificationOTP.generate_otp_code()
            otp_record = EmailVerificationOTP(
                user=user,
                expires_at=timezone.now() + timedelta(minutes=3),
                attempts=0,
                is_verified=False
            )

            otp_record.set_otp(raw_otp)
            otp_record.save()

            # 4. Store user session ID for OTP verification step
            request.session['otp_user_id'] = user.id

            # 5. Dispatch verification email
            try:
                send_otp_verification_email(user, raw_otp)
                messages.success(
                    request,
                    f"Account created! We've sent a 6-digit OTP to {user.email}. Please verify your email."
                )
            except Exception as e:
                messages.warning(
                    request,
                    f"Account created, but email could not be sent ({e}). If testing locally, check terminal console."
                )

            # 6. Log activity
            log_activity(
                action='User Registered',
                details=f"New farmer registered: {user.username} ({user.email})",
                user=user,
                icon='fa-user-plus'
            )

            return redirect('verify_otp')
        else:
            messages.error(request, "Registration failed. Please check the form errors below.")

    else:
        form = FarmerRegistrationForm()

    context = {
        'page_title': 'Farmer Registration | AgriConnect',
        'active_page': 'register',
        'form': form,
    }
    return render(request, 'farming/register.html', context)


def verify_otp_view(request):
    """
    6-Digit OTP Verification View.
    Validates entered OTP, expiration (10 min), and attempt limits (max 5).
    Activates user account upon successful verification.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    user_id = request.session.get('otp_user_id')
    user = None
    if user_id:
        user = User.objects.filter(id=user_id).first()

    if not user:
        messages.warning(request, "No pending verification session found. Please register or log in.")
        return redirect('login')

    if user.is_active:
        messages.info(request, "Your email is already verified. Please log in.")
        return redirect('login')

    latest_otp = EmailVerificationOTP.objects.filter(user=user, is_verified=False).order_by('-created_at').first()

    if request.method == 'POST':
        # Retrieve digits from individual input boxes or single input
        otp_digits = [request.POST.get(f'otp_{i}', '').strip() for i in range(1, 7)]
        entered_otp = "".join(otp_digits)
        if not entered_otp:
            entered_otp = request.POST.get('otp', '').strip()

        if not entered_otp or len(entered_otp) != 6 or not entered_otp.isdigit():
            messages.error(request, "Please enter a valid 6-digit numeric OTP.")
            return redirect('verify_otp')

        if not latest_otp:
            messages.error(request, "No pending OTP found. Please request a new OTP.")
            return redirect('verify_otp')

        # Check 1: Expiration (10 minutes)
        if latest_otp.is_expired():
            messages.error(request, "Your OTP has expired. Please request a new OTP.")
            return redirect('verify_otp')

        # Check 2: Attempt Limit (5 attempts max)
        if latest_otp.attempts >= 5:
            messages.error(request, "Too many incorrect attempts. Please request a new OTP.")
            return redirect('verify_otp')

        # Check 3: Validate against hashed OTP
        if latest_otp.check_otp(entered_otp):
            # Mark OTP as verified
            latest_otp.is_verified = True
            latest_otp.save()

            # Activate User
            user.is_active = True
            user.save()

            # Clear session
            request.session.pop('otp_user_id', None)

            # Log activity
            log_activity(
                action='Email Verified',
                details=f"Farmer {user.username} verified email ({user.email})",
                user=user,
                icon='fa-circle-check'
            )

            messages.success(
                request,
                "Email verified successfully! Your account is now active. You can login to AgriConnect."
            )
            return redirect('login')
        else:
            latest_otp.attempts += 1
            latest_otp.save()

            if latest_otp.attempts >= 5:
                messages.error(
                    request,
                    "Too many incorrect attempts. Your OTP has been invalidated. Please request a new OTP."
                )
            else:
                remaining = 5 - latest_otp.attempts
                messages.error(
                    request,
                    f"Invalid OTP. Please check the OTP and try again. ({remaining} attempt{'s' if remaining > 1 else ''} remaining)"
                )
            return redirect('verify_otp')

    # Compute remaining time for client-side JavaScript countdowns
    remaining_seconds = 0
    resend_cooldown_remaining = 0

    if latest_otp and not latest_otp.is_expired():
        remaining_seconds = max(0, int((latest_otp.expires_at - timezone.now()).total_seconds()))

    if latest_otp:
        elapsed = (timezone.now() - latest_otp.created_at).total_seconds()
        resend_cooldown_remaining = max(0, int(60 - elapsed))

    email = user.email
    if '@' in email:
        local, domain = email.split('@', 1)
        masked_local = local[0] + '***' if len(local) > 1 else local + '***'
        masked_email = f"{masked_local}@{domain}"
    else:
        masked_email = email

    context = {
        'page_title': 'Verify Your Email | AgriConnect',
        'active_page': 'verify_otp',
        'user_email': user.email,
        'masked_email': masked_email,
        'remaining_seconds': remaining_seconds,
        'resend_cooldown_remaining': resend_cooldown_remaining,
        'is_expired': latest_otp.is_expired() if latest_otp else True,
        'too_many_attempts': (latest_otp.attempts >= 5) if latest_otp else False,
    }
    return render(request, 'farming/verify_otp.html', context)


def resend_otp_view(request):
    """
    Resend OTP View with strict 60-second cooldown rate limit.
    Invalidates older OTPs, generates new 6-digit OTP, resets expiry & attempts,
    and sends new verification email.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    user_id = request.session.get('otp_user_id')
    user = None
    if user_id:
        user = User.objects.filter(id=user_id).first()

    if not user:
        messages.warning(request, "No pending verification session found. Please register or log in.")
        return redirect('login')

    if user.is_active:
        messages.info(request, "Your email is already verified. Please log in.")
        return redirect('login')

    # Rate limiting: 60-second cooldown check
    latest_otp = EmailVerificationOTP.objects.filter(user=user).order_by('-created_at').first()
    if latest_otp:
        elapsed = (timezone.now() - latest_otp.created_at).total_seconds()
        if elapsed < 60:
            remaining_cooldown = int(60 - elapsed)
            messages.warning(
                request,
                f"Please wait {remaining_cooldown} seconds before requesting a new OTP."
            )
            return redirect('verify_otp')

    # Invalidate previous OTP records
    EmailVerificationOTP.objects.filter(user=user, is_verified=False).delete()

    # Generate fresh OTP
    raw_otp = EmailVerificationOTP.generate_otp_code()
    new_otp_record = EmailVerificationOTP(
        user=user,
        expires_at=timezone.now() + timedelta(minutes=3),
        attempts=0,
        is_verified=False
    )

    new_otp_record.set_otp(raw_otp)
    new_otp_record.save()

    # Dispatch email
    try:
        send_otp_verification_email(user, raw_otp)
        messages.success(request, f"A new OTP has been sent to {user.email}.")
    except Exception as e:
        messages.warning(
            request,
            f"Could not send OTP email ({e}). If using console backend, check your terminal."
        )

    return redirect('verify_otp')


# ==========================================
# FORGOT PASSWORD & PASSWORD RESET VIEWS
# ==========================================

def forgot_password_view(request):
    """
    Step 1 of Password Reset:
    Accepts registered email, generates a secure 6-digit OTP (10 min expiry),
    hashes OTP in PasswordResetOTP model, and sends password reset email.
    Uses generic messages to prevent user enumeration.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = ForgotPasswordRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email', '').strip().lower()
            candidate_user = User.objects.filter(email__iexact=email).first()

            if candidate_user:
                # If the user account is not active / verified yet, require verification first
                if not candidate_user.is_active:
                    request.session['otp_user_id'] = candidate_user.id
                    messages.warning(
                        request,
                        "Your account has not been email-verified yet. Please verify your email first."
                    )
                    return redirect('verify_otp')

                # 1. Invalidate any existing pending password reset OTPs
                PasswordResetOTP.objects.filter(user=candidate_user, is_verified=False).delete()

                # 2. Generate secure 6-digit OTP (10-minute validity)
                raw_otp = PasswordResetOTP.generate_otp_code()
                otp_record = PasswordResetOTP(
                    user=candidate_user,
                    expires_at=timezone.now() + timedelta(minutes=10),
                    attempts=0,
                    is_verified=False
                )
                otp_record.set_otp(raw_otp)
                otp_record.save()

                # 3. Store user ID in session for the verification step
                request.session['password_reset_user_id'] = candidate_user.id
                request.session['password_reset_email'] = candidate_user.email
                request.session['password_reset_verified'] = False

                # 4. Dispatch email
                try:
                    send_password_reset_otp_email(candidate_user, raw_otp)
                except Exception:
                    pass

                # 5. Log activity
                log_activity(
                    action='Password Reset Requested',
                    details=f"Password reset requested for {candidate_user.username} ({candidate_user.email})",
                    user=candidate_user,
                    icon='fa-key'
                )
            else:
                # Protect against user enumeration: set dummy placeholder session
                request.session['password_reset_user_id'] = -1
                request.session['password_reset_email'] = email
                request.session['password_reset_verified'] = False

            # Security: Always show generic message to prevent email enumeration
            messages.success(
                request,
                "If an account with this email exists, a verification OTP has been sent."
            )
            return redirect('verify_password_reset_otp')
        else:
            messages.error(request, "Please enter a valid email address.")
    else:
        form = ForgotPasswordRequestForm()

    context = {
        'page_title': 'Reset Your Password | AgriConnect',
        'active_page': 'forgot_password',
        'form': form,
    }
    return render(request, 'farming/forgot_password.html', context)


def verify_password_reset_otp_view(request):
    """
    Step 2 of Password Reset:
    Validates entered 6-digit OTP, checks 10-minute expiry and 5-attempt limit.
    Upon success, marks OTP verified and enables transition to /forgot-password/reset/.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    user_id = request.session.get('password_reset_user_id')
    session_email = request.session.get('password_reset_email', '')

    if not user_id:
        messages.warning(request, "Please enter your registered email to request a password reset.")
        return redirect('forgot_password')

    user = None
    if user_id != -1:
        user = User.objects.filter(id=user_id).first()

    latest_otp = PasswordResetOTP.objects.filter(user=user, is_verified=False).order_by('-created_at').first() if user else None

    if request.method == 'POST':
        otp_digits = [request.POST.get(f'otp_{i}', '').strip() for i in range(1, 7)]
        entered_otp = "".join(otp_digits)
        if not entered_otp:
            entered_otp = request.POST.get('otp', '').strip()

        if not entered_otp or len(entered_otp) != 6 or not entered_otp.isdigit():
            messages.error(request, "Please enter a valid 6-digit numeric OTP.")
            return redirect('verify_password_reset_otp')

        if not latest_otp or not user:
            messages.error(request, "Invalid OTP. Please check and try again.")
            return redirect('verify_password_reset_otp')

        # Check 1: Expiration (10 minutes)
        if latest_otp.is_expired():
            messages.error(request, "Your OTP has expired. Please request a new OTP.")
            return redirect('verify_password_reset_otp')

        # Check 2: Attempt Limit (5 attempts max)
        if latest_otp.attempts >= 5:
            messages.error(request, "Too many incorrect attempts. Please request a new OTP.")
            return redirect('verify_password_reset_otp')

        # Check 3: Validate against hashed OTP
        if latest_otp.check_otp(entered_otp):
            latest_otp.is_verified = True
            latest_otp.save()

            # Set verified session token
            request.session['password_reset_verified'] = True
            request.session['password_reset_verified_at'] = timezone.now().timestamp()

            log_activity(
                action='Password Reset OTP Verified',
                details=f"Password reset OTP verified for {user.username}",
                user=user,
                icon='fa-shield-check'
            )

            messages.success(request, "OTP verified successfully. Please create your new password.")
            return redirect('reset_password')
        else:
            latest_otp.attempts += 1
            latest_otp.save()

            if latest_otp.attempts >= 5:
                messages.error(
                    request,
                    "Too many incorrect attempts. Your OTP has been invalidated. Please request a new OTP."
                )
            else:
                remaining = 5 - latest_otp.attempts
                messages.error(
                    request,
                    f"Invalid OTP. Please check and try again. ({remaining} attempt{'s' if remaining > 1 else ''} remaining)"
                )
            return redirect('verify_password_reset_otp')

    # Compute remaining time for client-side JavaScript countdown (10 minutes)
    remaining_seconds = 600
    resend_cooldown_remaining = 0

    if latest_otp and not latest_otp.is_expired():
        remaining_seconds = max(0, int((latest_otp.expires_at - timezone.now()).total_seconds()))

    if latest_otp:
        elapsed = (timezone.now() - latest_otp.created_at).total_seconds()
        resend_cooldown_remaining = max(0, int(60 - elapsed))

    email_display = user.email if user else session_email
    if '@' in email_display:
        local, domain = email_display.split('@', 1)
        masked_local = local[0] + '***' + (local[-1] if len(local) > 2 else '')
        masked_email = f"{masked_local}@{domain}"
    else:
        masked_email = email_display

    context = {
        'page_title': 'Verify Password Reset OTP | AgriConnect',
        'active_page': 'verify_password_reset_otp',
        'user_email': email_display,
        'masked_email': masked_email,
        'remaining_seconds': remaining_seconds,
        'resend_cooldown_remaining': resend_cooldown_remaining,
        'is_expired': latest_otp.is_expired() if latest_otp else False,
        'too_many_attempts': (latest_otp.attempts >= 5) if latest_otp else False,
    }
    return render(request, 'farming/verify_password_otp.html', context)


def resend_password_reset_otp_view(request):
    """
    Resend Password Reset OTP with 60-second cooldown rate limiting.
    Invalidates old OTP, generates new 6-digit OTP (10 min expiry), and sends email.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    user_id = request.session.get('password_reset_user_id')
    if not user_id:
        messages.warning(request, "No pending password reset session found. Please enter your email.")
        return redirect('forgot_password')

    user = None
    if user_id != -1:
        user = User.objects.filter(id=user_id).first()

    if not user:
        messages.success(request, "A new password reset OTP has been sent if the account exists.")
        return redirect('verify_password_reset_otp')

    latest_otp = PasswordResetOTP.objects.filter(user=user).order_by('-created_at').first()
    if latest_otp:
        elapsed = (timezone.now() - latest_otp.created_at).total_seconds()
        if elapsed < 60:
            remaining_cooldown = int(60 - elapsed)
            messages.warning(
                request,
                f"Please wait {remaining_cooldown} seconds before requesting a new OTP."
            )
            return redirect('verify_password_reset_otp')

    # Invalidate previous OTPs
    PasswordResetOTP.objects.filter(user=user, is_verified=False).delete()

    # Generate fresh OTP (10 minutes)
    raw_otp = PasswordResetOTP.generate_otp_code()
    new_otp_record = PasswordResetOTP(
        user=user,
        expires_at=timezone.now() + timedelta(minutes=10),
        attempts=0,
        is_verified=False
    )
    new_otp_record.set_otp(raw_otp)
    new_otp_record.save()

    # Dispatch email
    try:
        send_password_reset_otp_email(user, raw_otp)
        messages.success(request, f"A new password reset OTP has been sent to {user.email}.")
    except Exception as e:
        messages.warning(
            request,
            f"Could not send OTP email ({e}). If testing locally, check your terminal console."
        )

    return redirect('verify_password_reset_otp')



def reset_password_view(request):
    """
    Step 3 of Password Reset:
    Requires verified OTP session. Validates new password (min 8 chars, matching),
    updates password with user.set_password(), clears reset session, and redirects to success.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    user_id = request.session.get('password_reset_user_id')
    is_verified = request.session.get('password_reset_verified')
    verified_at = request.session.get('password_reset_verified_at')

    # Strict access control: only allowed if OTP verification succeeded
    if not (user_id and is_verified and verified_at):
        messages.warning(request, "Please verify your OTP before resetting your password.")
        return redirect('forgot_password')

    # Verify session has not expired (15 minutes limit post-verification)
    if (timezone.now().timestamp() - float(verified_at)) > 900:
        request.session.pop('password_reset_user_id', None)
        request.session.pop('password_reset_verified', None)
        request.session.pop('password_reset_verified_at', None)
        messages.error(request, "Your password reset session has expired. Please start again.")
        return redirect('forgot_password')

    user = User.objects.filter(id=user_id).first()
    if not user:
        messages.error(request, "User account not found. Please start the password reset again.")
        return redirect('forgot_password')

    if request.method == 'POST':
        form = PasswordResetConfirmForm(user=user, data=request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.save()

            # Invalidate all password reset OTPs for this user
            PasswordResetOTP.objects.filter(user=user).delete()

            # Clear reset session
            request.session.pop('password_reset_user_id', None)
            request.session.pop('password_reset_verified', None)
            request.session.pop('password_reset_verified_at', None)

            # Log activity
            log_activity(
                action='Password Reset Successful',
                details=f"Password changed successfully for farmer {user.username}",
                user=user,
                icon='fa-lock'
            )

            messages.success(
                request,
                "Your password has been changed successfully! You can now log in using your new password."
            )
            return redirect('password_reset_success')
        else:
            messages.error(request, "Please correct the errors below to update your password.")
    else:
        form = PasswordResetConfirmForm(user=user)

    context = {
        'page_title': 'Create New Password | AgriConnect',
        'active_page': 'reset_password',
        'form': form,
        'user_username': user.username,
    }
    return render(request, 'farming/reset_password.html', context)


def password_reset_success_view(request):
    """
    Step 4: Success confirmation page after password change.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    context = {
        'page_title': 'Password Reset Successfully | AgriConnect',
        'active_page': 'password_reset_success',
    }
    return render(request, 'farming/password_reset_success.html', context)



def login_view(request):
    """
    Farmer Login view with split layout, remember-me support,
    and inactive account detection preventing unverified login.
    Supports login via username or registered email.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    unverified_user = None

    if request.method == 'POST':
        form = FarmerLoginForm(request.POST)
        if form.is_valid():
            username_input = form.cleaned_data.get('username', '').strip()
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')

            # Check if user exists by username OR email
            candidate_user = User.objects.filter(
                Q(username__iexact=username_input) | Q(email__iexact=username_input)
            ).first()

            if candidate_user and candidate_user.check_password(password) and not candidate_user.is_active:
                request.session['otp_user_id'] = candidate_user.id
                unverified_user = candidate_user
                messages.warning(
                    request,
                    "Please verify your email using the OTP before logging in."
                )
            else:
                # Use resolved username so authentication succeeds with either username or email
                auth_username = candidate_user.username if candidate_user else username_input
                user = authenticate(request, username=auth_username, password=password)
                if user is not None:
                    login(request, user)
                    if not remember_me:
                        request.session.set_expiry(0)  # Session expires when browser closes
                    else:
                        request.session.set_expiry(1209600)  # 2 weeks session

                    messages.success(request, f"Welcome back, {user.username}! You are now logged in.")
                    next_url = request.GET.get('next')
                    if next_url:
                        return redirect(next_url)
                    return redirect('dashboard')
                else:
                    messages.error(request, "Invalid username/email or password. Please try again.")
        else:
            messages.error(request, "Please enter both username and password.")
    else:
        form = FarmerLoginForm()


    context = {
        'page_title': 'Farmer Login | AgriConnect',
        'active_page': 'login',
        'form': form,
        'unverified_user': unverified_user,
    }
    return render(request, 'farming/login.html', context)


def logout_view(request):
    """
    Logout view: destroys session, adds confirmation message, and redirects to login.
    """
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')



# ==========================================
# FARMER DASHBOARD & CROP CRUD VIEWS
# ==========================================

@login_required
def dashboard_view(request):
    """
    Farmer Dashboard: summarizes crops, active acreages, status breakdowns,
    and recent farming logs.
    """
    user = request.user
    user_crops = Crop.objects.filter(farmer=user)

    total_crops = user_crops.count()
    active_crops = user_crops.filter(status__in=['Planted', 'Growing']).count()
    ready_crops = user_crops.filter(status='Ready to Harvest').count()
    harvested_crops = user_crops.filter(status='Harvested').count()

    total_area_agg = user_crops.aggregate(total_area=Sum('farm_area'))
    total_area = total_area_agg['total_area'] or 0.0

    recent_crops = user_crops.order_by('-created_at')[:5]

    context = {
        'page_title': 'Farmer Dashboard | AgriConnect',
        'active_page': 'dashboard',
        'total_crops': total_crops,
        'active_crops': active_crops,
        'ready_crops': ready_crops,
        'harvested_crops': harvested_crops,
        'total_area': total_area,
        'recent_crops': recent_crops,
    }
    return render(request, 'farming/dashboard.html', context)


@login_required
def my_crops_view(request):
    """
    List of all crops owned by the logged-in farmer with responsive table and actions.
    """
    status_filter = request.GET.get('status', '')
    season_filter = request.GET.get('season', '')

    crops = Crop.objects.filter(farmer=request.user)

    if status_filter:
        crops = crops.filter(status=status_filter)
    if season_filter:
        crops = crops.filter(season=season_filter)

    crops = crops.order_by('-created_at')

    context = {
        'page_title': 'My Crops | AgriConnect',
        'active_page': 'my_crops',
        'crops': crops,
        'status_filter': status_filter,
        'season_filter': season_filter,
    }
    return render(request, 'farming/my_crops.html', context)


@login_required
def add_crop_view(request):
    """
    Add a new crop to the logged-in farmer's inventory.
    """
    if request.method == 'POST':
        form = CropForm(request.POST)
        if form.is_valid():
            crop = form.save(commit=False)
            crop.farmer = request.user
            crop.save()
            log_activity('Crop Added', f"Farmer {request.user.username} added crop '{crop.crop_name}' ({crop.farm_area} Acres)", user=request.user, icon='fa-seedling')
            messages.success(request, f"Crop '{crop.crop_name}' added successfully!")
            return redirect('my_crops')
        else:
            messages.error(request, "Could not add crop. Please check form validation errors.")
    else:
        form = CropForm()

    context = {
        'page_title': 'Add New Crop | AgriConnect',
        'active_page': 'add_crop',
        'form': form,
    }
    return render(request, 'farming/add_crop.html', context)


@login_required
def edit_crop_view(request, id):
    """
    Edit existing crop. Strictly ensures the logged-in farmer is the owner.
    """
    crop = get_object_or_404(Crop, id=id)

    # Ownership security check
    if crop.farmer != request.user:
        messages.error(request, "Access denied: You are not authorized to modify another farmer's crop.")
        return redirect('my_crops')

    if request.method == 'POST':
        form = CropForm(request.POST, instance=crop)
        if form.is_valid():
            form.save()
            log_activity('Crop Updated', f"Farmer {request.user.username} updated crop '{crop.crop_name}'", user=request.user, icon='fa-pen-to-square')
            messages.success(request, f"Crop '{crop.crop_name}' updated successfully!")
            return redirect('my_crops')
        else:
            messages.error(request, "Failed to update crop. Please correct the errors.")
    else:
        form = CropForm(instance=crop)

    context = {
        'page_title': f'Edit Crop: {crop.crop_name} | AgriConnect',
        'active_page': 'my_crops',
        'crop': crop,
        'form': form,
    }
    return render(request, 'farming/edit_crop.html', context)


@login_required
def delete_crop_view(request, id):
    """
    Delete a crop with ownership validation.
    """
    crop = get_object_or_404(Crop, id=id)

    # Ownership security check
    if crop.farmer != request.user:
        messages.error(request, "Access denied: You cannot delete crops that do not belong to you.")
        return redirect('my_crops')

    crop_name = crop.crop_name
    crop.delete()
    log_activity('Crop Deleted', f"Farmer {request.user.username} removed crop '{crop_name}'", user=request.user, icon='fa-trash-can')
    messages.success(request, f"Crop '{crop_name}' was removed successfully from your farm records.")
    return redirect('my_crops')


@login_required
def profile_view(request):
    """
    Farmer Profile View and Update.
    """
    profile, _ = FarmerProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'full_name': request.user.get_full_name() or request.user.username,
            'phone': '',
            'state': 'Gujarat',
            'district': 'Ahmedabad',
            'taluka': '',
            'farm_location': '',
        }
    )

    if request.method == 'POST':
        form = FarmerProfileUpdateForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile details have been updated successfully.")
            return redirect('profile')
        else:
            messages.error(request, "Could not update profile. Please verify your entries.")
    else:
        form = FarmerProfileUpdateForm(request.user)

    context = {
        'page_title': 'My Farmer Profile | AgriConnect',
        'active_page': 'profile',
        'form': form,
        'profile': profile,
    }
    return render(request, 'farming/profile.html', context)


# ==========================================
# ADMIN DASHBOARD & MANAGEMENT PORTAL
# ==========================================

def get_admin_common_context(active_nav='dashboard'):
    """
    Returns common context data needed across all Admin views,
    such as unread message counts and active navigation state.
    """
    unread_messages_count = ContactMessage.objects.filter(is_read=False).count()
    return {
        'admin_active_nav': active_nav,
        'admin_unread_messages_count': unread_messages_count,
    }


def admin_login_view(request):
    """
    Dedicated, secure Administrator Login view.
    Validates is_staff or is_superuser permissions.
    """
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect('admin_dashboard')
        else:
            messages.warning(request, "You are logged in as a farmer. Admin credentials are required for the Admin Portal.")

    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Authenticate candidate user
            user = authenticate(request, username=username, password=password)
            if user is None:
                # Check if email was used instead of username
                candidate = User.objects.filter(email__iexact=username).first()
                if candidate:
                    user = authenticate(request, username=candidate.username, password=password)

            if user is not None:
                if user.is_staff or user.is_superuser:
                    login(request, user)
                    log_activity(
                        action='Admin Login',
                        details=f"Admin '{user.username}' successfully logged into the Admin Management Portal.",
                        user=user,
                        icon='fa-shield-halved'
                    )
                    messages.success(request, f"Welcome to AgriConnect Admin Portal, {user.get_full_name() or user.username}!")
                    next_url = request.GET.get('next')
                    if next_url:
                        return redirect(next_url)
                    return redirect('admin_dashboard')
                else:
                    messages.error(request, "Access restricted: This account does not have administrator privileges. Please use the Farmer Login.")
            else:
                messages.error(request, "Invalid administrator username or password. Please verify your credentials.")
        else:
            messages.error(request, "Please fill in all required login fields.")
    else:
        form = AdminLoginForm()

    context = {
        'page_title': 'Admin Login | AgriConnect Management Portal',
        'form': form,
    }
    return render(request, 'admin_dashboard/login.html', context)


def admin_logout_view(request):
    """
    Administrator Logout view. Destroys session and redirects to /admin-login/.
    """
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        log_activity(
            action='Admin Logout',
            details=f"Admin '{request.user.username}' logged out.",
            user=request.user,
            icon='fa-right-from-bracket'
        )
    logout(request)
    messages.info(request, "You have been logged out of the Admin Portal.")
    return redirect('admin_login')


@admin_required
def admin_dashboard_view(request):
    """
    Main Admin Dashboard View:
    Aggregates full-system statistics, recent users, recent crops, recent contact inquiries,
    and the real-time activity timeline.
    """
    total_users = User.objects.count()
    verified_users = User.objects.filter(is_active=True).count()
    unverified_users = User.objects.filter(is_active=False).count()

    total_crops = Crop.objects.count()
    active_crops = Crop.objects.filter(status__in=['Planted', 'Growing', 'Ready to Harvest']).count()
    harvested_crops = Crop.objects.filter(status='Harvested').count()

    total_area_agg = Crop.objects.aggregate(total_area=Sum('farm_area'))
    total_farm_area = total_area_agg['total_area'] or 0.0

    total_messages = ContactMessage.objects.count()
    unread_messages = ContactMessage.objects.filter(is_read=False).count()

    # Recent Data Streams
    recent_users = User.objects.select_related('farmer_profile').order_by('-date_joined')[:5]
    recent_crops = Crop.objects.select_related('farmer').order_by('-created_at')[:5]
    recent_messages = ContactMessage.objects.order_by('-created_at')[:5]
    recent_activities = ActivityLog.objects.select_related('user').order_by('-created_at')[:10]

    # Top crop distributions for mini dashboard bar visual
    top_crops = Crop.objects.values('crop_name').annotate(count=Count('id'), area=Sum('farm_area')).order_by('-count')[:5]

    context = {
        'page_title': 'Admin Dashboard | AgriConnect Management Portal',
        **get_admin_common_context('dashboard'),
        'total_users': total_users,
        'verified_users': verified_users,
        'unverified_users': unverified_users,
        'total_crops': total_crops,
        'active_crops': active_crops,
        'harvested_crops': harvested_crops,
        'total_farm_area': total_farm_area,
        'total_messages': total_messages,
        'unread_messages': unread_messages,
        'recent_users': recent_users,
        'recent_crops': recent_crops,
        'recent_messages': recent_messages,
        'recent_activities': recent_activities,
        'top_crops': top_crops,
    }
    return render(request, 'admin_dashboard/dashboard.html', context)


@admin_required
def admin_users_view(request):
    """
    User Management:
    Lists all registered users with search, filters (All, Verified, Unverified, Active, Inactive, Staff),
    and pagination.
    """
    search_query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', 'all').strip()

    users_qs = User.objects.select_related('farmer_profile').annotate(
        crops_count=Count('crops'),
        total_farm_area=Sum('crops__farm_area')
    ).order_by('-date_joined')

    # Apply Search
    if search_query:
        users_qs = users_qs.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(farmer_profile__full_name__icontains=search_query) |
            Q(farmer_profile__phone__icontains=search_query) |
            Q(farmer_profile__district__icontains=search_query) |
            Q(farmer_profile__taluka__icontains=search_query) |
            Q(farmer_profile__farm_location__icontains=search_query)
        )

    # Apply Filter
    if status_filter == 'verified' or status_filter == 'active':
        users_qs = users_qs.filter(is_active=True)
    elif status_filter == 'unverified' or status_filter == 'inactive':
        users_qs = users_qs.filter(is_active=False)
    elif status_filter == 'staff':
        users_qs = users_qs.filter(is_staff=True)

    # Counts for Filter Badges
    count_all = User.objects.count()
    count_verified = User.objects.filter(is_active=True).count()
    count_unverified = User.objects.filter(is_active=False).count()
    count_staff = User.objects.filter(is_staff=True).count()

    paginator = Paginator(users_qs, 15)
    page_number = request.GET.get('page')
    users_page = paginator.get_page(page_number)

    context = {
        'page_title': 'User Management | AgriConnect Admin',
        **get_admin_common_context('users'),
        'users': users_page,
        'search_query': search_query,
        'status_filter': status_filter,
        'count_all': count_all,
        'count_verified': count_verified,
        'count_unverified': count_unverified,
        'count_staff': count_staff,
    }
    return render(request, 'admin_dashboard/users.html', context)


@admin_required
def admin_user_detail_view(request, id):
    """
    Detailed User Profile View:
    Displays complete farmer details, verification status, registered crops, and recent activity.
    """
    target_user = get_object_or_404(User.objects.select_related('farmer_profile'), id=id)
    user_crops = Crop.objects.filter(farmer=target_user).order_by('-created_at')
    crops_count = user_crops.count()
    total_area_agg = user_crops.aggregate(total_area=Sum('farm_area'))
    total_area = total_area_agg['total_area'] or 0.0

    otp_records = EmailVerificationOTP.objects.filter(user=target_user).order_by('-created_at')[:10]
    user_activities = ActivityLog.objects.filter(user=target_user).order_by('-created_at')[:10]

    context = {
        'page_title': f'User Details: {target_user.username} | AgriConnect Admin',
        **get_admin_common_context('users'),
        'target_user': target_user,
        'user_crops': user_crops,
        'crops_count': crops_count,
        'total_area': total_area,
        'otp_records': otp_records,
        'user_activities': user_activities,
    }
    return render(request, 'admin_dashboard/user_detail.html', context)


@admin_required
def admin_user_edit_view(request, id):
    """
    Edit User & Profile information.
    """
    target_user = get_object_or_404(User, id=id)

    if request.method == 'POST':
        form = AdminUserEditForm(target_user, request.POST)
        if form.is_valid():
            form.save()
            log_activity(
                action='User Updated',
                details=f"Admin '{request.user.username}' updated profile and credentials for '{target_user.username}'",
                user=request.user,
                icon='fa-user-gear'
            )
            messages.success(request, f"User '{target_user.username}' updated successfully.")
            return redirect('admin_user_detail', id=target_user.id)
        else:
            messages.error(request, "Failed to update user. Please correct the errors below.")
    else:
        form = AdminUserEditForm(target_user)

    context = {
        'page_title': f'Edit User: {target_user.username} | AgriConnect Admin',
        **get_admin_common_context('users'),
        'target_user': target_user,
        'form': form,
    }
    return render(request, 'admin_dashboard/user_edit.html', context)


@admin_required
def admin_user_toggle_status_view(request, id):
    """
    Quickly toggles a user's active/inactive status.
    Guards against self-deactivation.
    """
    target_user = get_object_or_404(User, id=id)

    if target_user == request.user:
        messages.error(request, "Security protection: You cannot deactivate your own administrative account.")
        return redirect('admin_users')

    target_user.is_active = not target_user.is_active
    target_user.save()

    status_str = "activated" if target_user.is_active else "deactivated"
    log_activity(
        action='User Status Changed',
        details=f"Admin '{request.user.username}' {status_str} account for '{target_user.username}'",
        user=request.user,
        icon='fa-user-gear'
    )
    messages.success(request, f"User '{target_user.username}' has been {status_str}.")
    return redirect(request.META.get('HTTP_REFERER', 'admin_users'))


@admin_required
def admin_user_delete_view(request, id):
    """
    Deletes a user account with strict safeguards against self-deletion.
    """
    target_user = get_object_or_404(User, id=id)

    if target_user == request.user:
        messages.error(request, "Security protection: You cannot delete your own administrative account.")
        return redirect('admin_users')

    if request.method == 'POST':
        username = target_user.username
        target_user.delete()
        log_activity(
            action='User Deleted',
            details=f"Admin '{request.user.username}' deleted user account '{username}'",
            user=request.user,
            icon='fa-user-xmark'
        )
        messages.success(request, f"User '{username}' and all associated farm records have been removed.")
        return redirect('admin_users')

    messages.error(request, "Invalid deletion request.")
    return redirect('admin_users')


@admin_required
def admin_crops_view(request):
    """
    Crop Management:
    Lists all crops from all farmers with search (crop name, farmer, season, type) and status filters.
    """
    search_query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', 'all').strip()
    season_filter = request.GET.get('season', 'all').strip()

    crops_qs = Crop.objects.select_related('farmer', 'farmer__farmer_profile').order_by('-created_at')

    # Apply Search
    if search_query:
        crops_qs = crops_qs.filter(
            Q(crop_name__icontains=search_query) |
            Q(farmer__username__icontains=search_query) |
            Q(farmer__farmer_profile__full_name__icontains=search_query) |
            Q(crop_type__icontains=search_query) |
            Q(season__icontains=search_query)
        )

    # Apply Status Filter
    if status_filter != 'all' and status_filter in ['Planted', 'Growing', 'Ready to Harvest', 'Harvested']:
        crops_qs = crops_qs.filter(status=status_filter)

    # Apply Season Filter
    if season_filter != 'all' and season_filter:
        crops_qs = crops_qs.filter(season=season_filter)

    # Counts
    count_all = Crop.objects.count()
    count_planted = Crop.objects.filter(status='Planted').count()
    count_growing = Crop.objects.filter(status='Growing').count()
    count_ready = Crop.objects.filter(status='Ready to Harvest').count()
    count_harvested = Crop.objects.filter(status='Harvested').count()

    paginator = Paginator(crops_qs, 15)
    page_number = request.GET.get('page')
    crops_page = paginator.get_page(page_number)

    context = {
        'page_title': 'Crop Management | AgriConnect Admin',
        **get_admin_common_context('crops'),
        'crops': crops_page,
        'search_query': search_query,
        'status_filter': status_filter,
        'season_filter': season_filter,
        'count_all': count_all,
        'count_planted': count_planted,
        'count_growing': count_growing,
        'count_ready': count_ready,
        'count_harvested': count_harvested,
    }
    return render(request, 'admin_dashboard/crops.html', context)


@admin_required
def admin_crop_edit_view(request, id):
    """
    Allows Admin to edit any crop details.
    """
    crop = get_object_or_404(Crop, id=id)

    if request.method == 'POST':
        form = AdminCropEditForm(request.POST, instance=crop)
        if form.is_valid():
            form.save()
            log_activity(
                action='Crop Updated',
                details=f"Admin '{request.user.username}' edited crop '{crop.crop_name}' for farmer '{crop.farmer.username}'",
                user=request.user,
                icon='fa-pen-to-square'
            )
            messages.success(request, f"Crop '{crop.crop_name}' updated successfully.")
            return redirect('admin_crops')
        else:
            messages.error(request, "Could not update crop. Please correct the errors below.")
    else:
        form = AdminCropEditForm(instance=crop)

    context = {
        'page_title': f'Edit Crop: {crop.crop_name} | AgriConnect Admin',
        **get_admin_common_context('crops'),
        'crop': crop,
        'form': form,
    }
    return render(request, 'admin_dashboard/crop_edit.html', context)


@admin_required
def admin_crop_delete_view(request, id):
    """
    Allows Admin to delete a crop record.
    """
    crop = get_object_or_404(Crop, id=id)

    if request.method == 'POST':
        crop_name = crop.crop_name
        farmer_name = crop.farmer.username
        crop.delete()
        log_activity(
            action='Crop Deleted',
            details=f"Admin '{request.user.username}' deleted crop '{crop_name}' (Farmer: {farmer_name})",
            user=request.user,
            icon='fa-trash-can'
        )
        messages.success(request, f"Crop '{crop_name}' was removed from records.")
        return redirect('admin_crops')

    messages.error(request, "Invalid deletion request.")
    return redirect('admin_crops')


@admin_required
def admin_messages_view(request):
    """
    Contact Inquiries Management:
    Lists all contact inquiries, highlights unread items, supports search and read/unread filtering.
    """
    search_query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', 'all').strip()

    messages_qs = ContactMessage.objects.all().order_by('-created_at')

    # Apply Search
    if search_query:
        messages_qs = messages_qs.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(subject__icontains=search_query) |
            Q(message__icontains=search_query)
        )

    # Apply Status Filter
    if status_filter == 'unread':
        messages_qs = messages_qs.filter(is_read=False)
    elif status_filter == 'read':
        messages_qs = messages_qs.filter(is_read=True)

    # Counts
    total_count = ContactMessage.objects.count()
    unread_count = ContactMessage.objects.filter(is_read=False).count()
    read_count = ContactMessage.objects.filter(is_read=True).count()

    paginator = Paginator(messages_qs, 15)
    page_number = request.GET.get('page')
    messages_page = paginator.get_page(page_number)

    context = {
        'page_title': 'Contact Messages | AgriConnect Admin',
        **get_admin_common_context('messages'),
        'messages_list': messages_page,
        'search_query': search_query,
        'status_filter': status_filter,
        'total_count': total_count,
        'unread_count': unread_count,
        'read_count': read_count,
    }
    return render(request, 'admin_dashboard/messages.html', context)


@admin_required
def admin_message_detail_view(request, id):
    """
    Displays the full message content.
    Automatically marks unread messages as Read upon opening.
    """
    msg_obj = get_object_or_404(ContactMessage, id=id)

    # Automatically mark as read if not already read
    if not msg_obj.is_read:
        msg_obj.is_read = True
        msg_obj.read_at = timezone.now()
        msg_obj.save()
        log_activity(
            action='Message Read',
            details=f"Admin '{request.user.username}' viewed inquiry from {msg_obj.name}: {msg_obj.subject}",
            user=request.user,
            icon='fa-envelope-open-text'
        )

    context = {
        'page_title': f'Message: {msg_obj.subject} | AgriConnect Admin',
        **get_admin_common_context('messages'),
        'msg': msg_obj,
    }
    return render(request, 'admin_dashboard/message_detail.html', context)


@admin_required
def admin_message_toggle_read_view(request, id):
    """
    Allows Admin to manually toggle read/unread state of a message.
    """
    msg_obj = get_object_or_404(ContactMessage, id=id)
    msg_obj.is_read = not msg_obj.is_read
    if msg_obj.is_read and not msg_obj.read_at:
        msg_obj.read_at = timezone.now()
    msg_obj.save()

    status_str = "Read" if msg_obj.is_read else "Unread"
    messages.success(request, f"Message marked as {status_str}.")
    return redirect(request.META.get('HTTP_REFERER', 'admin_messages'))


@admin_required
def admin_message_delete_view(request, id):
    """
    Allows Admin to delete a contact message.
    """
    msg_obj = get_object_or_404(ContactMessage, id=id)

    if request.method == 'POST':
        subject = msg_obj.subject
        msg_obj.delete()
        log_activity(
            action='Message Deleted',
            details=f"Admin '{request.user.username}' deleted message '{subject}'",
            user=request.user,
            icon='fa-trash-can'
        )
        messages.success(request, "Message has been deleted.")
        return redirect('admin_messages')

    messages.error(request, "Invalid deletion request.")
    return redirect('admin_messages')


@admin_required
def admin_otp_view(request):
    """
    Email OTP Management & Audit:
    Displays OTP request metrics, pending unverified accounts, and secure audit history.
    Never exposes raw OTP strings.
    """
    total_otps = EmailVerificationOTP.objects.count()
    verified_otps = EmailVerificationOTP.objects.filter(is_verified=True).count()
    pending_otps = EmailVerificationOTP.objects.filter(is_verified=False, expires_at__gte=timezone.now()).count()
    expired_otps = EmailVerificationOTP.objects.filter(is_verified=False, expires_at__lt=timezone.now()).count()

    # Password Reset OTP metrics
    total_reset_otps = PasswordResetOTP.objects.count()
    verified_reset_otps = PasswordResetOTP.objects.filter(is_verified=True).count()
    pending_reset_otps = PasswordResetOTP.objects.filter(is_verified=False, expires_at__gte=timezone.now()).count()
    expired_reset_otps = PasswordResetOTP.objects.filter(is_verified=False, expires_at__lt=timezone.now()).count()

    # Pending User Accounts
    pending_users = User.objects.filter(is_active=False).order_by('-date_joined')

    # Recent OTP audit logs (without exposing OTP)
    otp_logs = EmailVerificationOTP.objects.select_related('user').order_by('-created_at')[:40]
    password_reset_logs = PasswordResetOTP.objects.select_related('user').order_by('-created_at')[:40]

    context = {
        'page_title': 'Email OTP Verification | AgriConnect Admin',
        **get_admin_common_context('otp'),
        'total_otps': total_otps,
        'verified_otps': verified_otps,
        'pending_otps': pending_otps,
        'expired_otps': expired_otps,
        'total_reset_otps': total_reset_otps,
        'verified_reset_otps': verified_reset_otps,
        'pending_reset_otps': pending_reset_otps,
        'expired_reset_otps': expired_reset_otps,
        'pending_users': pending_users,
        'otp_logs': otp_logs,
        'password_reset_logs': password_reset_logs,
    }
    return render(request, 'admin_dashboard/otp.html', context)



@admin_required
def admin_resend_otp_view(request, user_id):
    """
    Allows Admin to trigger a fresh OTP email for a pending unverified user.
    """
    target_user = get_object_or_404(User, id=user_id)

    if target_user.is_active:
        messages.info(request, f"User '{target_user.username}' is already verified.")
        return redirect('admin_otp')

    # Invalidate older pending OTPs
    EmailVerificationOTP.objects.filter(user=target_user, is_verified=False).delete()

    # Generate fresh 6-digit OTP
    raw_otp = EmailVerificationOTP.generate_otp_code()
    new_otp_record = EmailVerificationOTP(
        user=target_user,
        expires_at=timezone.now() + timedelta(minutes=10),
        attempts=0,
        is_verified=False
    )
    new_otp_record.set_otp(raw_otp)
    new_otp_record.save()

    # Dispatch email
    try:
        send_otp_verification_email(target_user, raw_otp)
        log_activity(
            action='OTP Resent',
            details=f"Admin '{request.user.username}' triggered OTP resend for '{target_user.username}' ({target_user.email})",
            user=request.user,
            icon='fa-envelope-circle-check'
        )
        messages.success(request, f"New OTP generated and sent to {target_user.email}.")
    except Exception as e:
        messages.warning(request, f"OTP generated, but email delivery reported: {e}")

    return redirect('admin_otp')


@admin_required
def admin_tips_view(request):
    """
    Farming Tips Management:
    Displays all tips with add, edit, and delete management features.
    """
    seed_default_tips_if_empty()
    tips = FarmingTip.objects.all().order_by('category', '-created_at')

    context = {
        'page_title': 'Farming Tips Management | AgriConnect Admin',
        **get_admin_common_context('tips'),
        'tips': tips,
    }
    return render(request, 'admin_dashboard/tips.html', context)


@admin_required
def admin_tip_add_view(request):
    """
    Add a new Farming Tip.
    """
    if request.method == 'POST':
        form = AdminFarmingTipForm(request.POST, request.FILES)
        if form.is_valid():
            tip = form.save()
            log_activity(
                action='Tip Added',
                details=f"Admin '{request.user.username}' added farming tip '{tip.title}' [{tip.category}]",
                user=request.user,
                icon='fa-lightbulb'
            )
            messages.success(request, f"Farming tip '{tip.title}' added successfully.")
            return redirect('admin_tips')
        else:
            messages.error(request, "Failed to add tip. Please review the form errors.")
    else:
        form = AdminFarmingTipForm()

    context = {
        'page_title': 'Add Farming Tip | AgriConnect Admin',
        **get_admin_common_context('tips'),
        'form': form,
        'action_mode': 'Add',
    }
    return render(request, 'admin_dashboard/tip_form.html', context)


@admin_required
def admin_tip_edit_view(request, id):
    """
    Edit an existing Farming Tip.
    """
    tip = get_object_or_404(FarmingTip, id=id)

    if request.method == 'POST':
        form = AdminFarmingTipForm(request.POST, request.FILES, instance=tip)
        if form.is_valid():
            form.save()
            log_activity(
                action='Tip Updated',
                details=f"Admin '{request.user.username}' updated tip '{tip.title}'",
                user=request.user,
                icon='fa-pen'
            )
            messages.success(request, f"Farming tip '{tip.title}' updated successfully.")
            return redirect('admin_tips')
        else:
            messages.error(request, "Failed to update tip. Please review the form errors.")
    else:
        form = AdminFarmingTipForm(instance=tip)

    context = {
        'page_title': f'Edit Tip: {tip.title} | AgriConnect Admin',
        **get_admin_common_context('tips'),
        'tip': tip,
        'form': form,
        'action_mode': 'Edit',
    }
    return render(request, 'admin_dashboard/tip_form.html', context)


@admin_required
def admin_tip_delete_view(request, id):
    """
    Delete a Farming Tip.
    """
    tip = get_object_or_404(FarmingTip, id=id)

    if request.method == 'POST':
        title = tip.title
        tip.delete()
        log_activity(
            action='Tip Deleted',
            details=f"Admin '{request.user.username}' deleted tip '{title}'",
            user=request.user,
            icon='fa-trash'
        )
        messages.success(request, f"Tip '{title}' has been removed.")
        return redirect('admin_tips')

    messages.error(request, "Invalid deletion request.")
    return redirect('admin_tips')


@admin_required
def admin_weather_view(request):
    """
    Weather Administration:
    Monitors WeatherAPI.com connectivity, environment configuration status without exposing keys,
    and provides administrative diagnostic lookups for Gujarat locations.
    """
    weather_key_present = bool(getattr(settings, 'WEATHER_API_KEY', '') or os.getenv('WEATHER_API_KEY'))

    context = {
        'page_title': 'Weather Module Status | AgriConnect Admin',
        **get_admin_common_context('weather'),
        'weather_api_configured': weather_key_present,
        'api_status_label': 'Operational (WeatherAPI.com Connected)' if weather_key_present else 'Configuration Required (WEATHER_API_KEY missing in .env)',
        'last_health_check': timezone.now(),
    }
    return render(request, 'admin_dashboard/weather.html', context)


@admin_required
def admin_analytics_view(request):
    """
    Gujarat Agricultural Analytics & Reporting:
    Generates statistics on user growth by month, crop status distributions,
    top Gujarat crop acreages, Gujarat regional distribution, and seasonal patterns.
    """
    # 1. User growth by month (last 6 months)
    users_by_month = (
        User.objects.annotate(month=TruncMonth('date_joined'))
        .values('month')
        .annotate(total=Count('id'))
        .order_by('month')
    )
    user_growth_labels = []
    user_growth_counts = []
    for item in users_by_month:
        if item['month']:
            user_growth_labels.append(item['month'].strftime('%b %Y'))
            user_growth_counts.append(item['total'])

    # 2. Crop Status Breakdown
    planted_count = Crop.objects.filter(status='Planted').count()
    growing_count = Crop.objects.filter(status='Growing').count()
    ready_count = Crop.objects.filter(status='Ready to Harvest').count()
    harvested_count = Crop.objects.filter(status='Harvested').count()

    # 3. Top Gujarat Crops by acreage
    top_crops_area = Crop.objects.values('crop_name').annotate(
        total_area=Sum('farm_area'),
        crop_count=Count('id')
    ).order_by('-total_area')[:8]

    # 4. Gujarat Regional Distribution (Saurashtra, North, Central, South, Kutch)
    region_distribution = Crop.objects.values('region').annotate(
        count=Count('id'),
        area=Sum('farm_area')
    ).order_by('-area')

    # 5. Gujarat Farmers by District
    farmers_by_district = FarmerProfile.objects.values('district').annotate(
        count=Count('id')
    ).order_by('-count')[:8]

    # 6. Season Distribution
    season_distribution = Crop.objects.values('season').annotate(
        count=Count('id'),
        area=Sum('farm_area')
    ).order_by('-count')

    # Total area summary
    total_area_agg = Crop.objects.aggregate(total_area=Sum('farm_area'))
    total_farm_area = total_area_agg['total_area'] or 0.0

    context = {
        'page_title': 'Gujarat Agriculture Analytics & Reports | AgriConnect Admin',
        **get_admin_common_context('analytics'),
        'user_growth_labels': user_growth_labels,
        'user_growth_counts': user_growth_counts,
        'planted_count': planted_count,
        'growing_count': growing_count,
        'ready_count': ready_count,
        'harvested_count': harvested_count,
        'top_crops_area': top_crops_area,
        'region_distribution': region_distribution,
        'farmers_by_district': farmers_by_district,
        'season_distribution': season_distribution,
        'total_farm_area': total_farm_area,
        'total_users': User.objects.count(),
        'total_crops': Crop.objects.count(),
    }
    return render(request, 'admin_dashboard/analytics.html', context)


@admin_required
def admin_activity_view(request):
    """
    Comprehensive System Audit & Activity Log:
    Lists all activity events with filtering by action type and pagination.
    """
    action_filter = request.GET.get('action', 'all').strip()

    activities_qs = ActivityLog.objects.select_related('user').order_by('-created_at')

    if action_filter != 'all' and action_filter:
        activities_qs = activities_qs.filter(action=action_filter)

    distinct_actions = ActivityLog.objects.values_list('action', flat=True).distinct()

    paginator = Paginator(activities_qs, 25)
    page_number = request.GET.get('page')
    activities_page = paginator.get_page(page_number)

    context = {
        'page_title': 'Activity Logs & System Audit | AgriConnect Admin',
        **get_admin_common_context('activity'),
        'activities': activities_page,
        'action_filter': action_filter,
        'distinct_actions': distinct_actions,
    }
    return render(request, 'admin_dashboard/activity.html', context)
