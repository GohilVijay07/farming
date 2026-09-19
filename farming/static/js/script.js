/**
 * AgriConnect — Smart Farming Management System
 * Global Modern JavaScript Interactive Framework & Micro-Interactions
 * Gujarat Focused (District -> Taluka -> Village Hierarchy)
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Initialize Sticky Navbar & Scroll Effects
    initNavbarScroll();

    // 2. Initialize Mobile Navigation Drawer
    initMobileNav();

    // 3. Initialize Password Show/Hide Toggles
    initPasswordToggles();

    // 4. Initialize Auto-dismiss for Flash Notification Messages
    initFlashMessages();

    // 5. Initialize Crop Catalog Real-time Search Filter
    initCropSearch();

    // 6. Initialize Farming Tips Category Filter Tabs
    initTipsFilter();

    // 7. Initialize Crop Delete Confirmation Modal
    initDeleteConfirmation();

    // 8. Initialize Interactive Gujarat Weather Lookup
    initWeatherSimulation();

    // 9. Initialize 6-Digit OTP Verification Form & Countdown Timers
    initOtpVerification();

    // 10. Initialize Scroll Reveal Animations
    initScrollReveal();

    // 11. Initialize Back to Top Button
    initBackToTop();

    // 12. Initialize 3D Card Hover Tilt Effects
    init3DTiltEffects();

    // 13. Initialize Gujarat Dependent Dropdowns (District -> Taluka -> Village)
    initGujaratLocationDropdowns();
});


/* ==========================================================================
   1. Sticky Navbar & Scroll State
   ========================================================================== */
function initNavbarScroll() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;

    window.addEventListener('scroll', () => {
        if (window.scrollY > 20) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    }, { passive: true });
}


/* ==========================================================================
   2. Mobile Navigation Toggle Drawer
   ========================================================================== */
function initMobileNav() {
    const hamburgerBtn = document.getElementById('hamburgerBtn');
    const navMenu = document.getElementById('navMenu');

    if (hamburgerBtn && navMenu) {
        hamburgerBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            const isActive = navMenu.classList.toggle('active');
            hamburgerBtn.setAttribute('aria-expanded', isActive ? 'true' : 'false');
            const icon = hamburgerBtn.querySelector('i');
            if (icon) {
                icon.className = isActive ? 'fa-solid fa-xmark' : 'fa-solid fa-bars';
            }
        });

        // Close nav when clicking outside
        document.addEventListener('click', (e) => {
            if (!navMenu.contains(e.target) && !hamburgerBtn.contains(e.target) && navMenu.classList.contains('active')) {
                navMenu.classList.remove('active');
                hamburgerBtn.setAttribute('aria-expanded', 'false');
                const icon = hamburgerBtn.querySelector('i');
                if (icon) icon.className = 'fa-solid fa-bars';
            }
        });
    }
}


/* ==========================================================================
   3. Password Visibility Toggle
   ========================================================================== */
function initPasswordToggles() {
    const toggleButtons = document.querySelectorAll('.password-toggle-btn');

    toggleButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetId = button.getAttribute('data-target');
            const inputField = document.getElementById(targetId);
            const icon = button.querySelector('i');

            if (inputField) {
                if (inputField.type === 'password') {
                    inputField.type = 'text';
                    if (icon) {
                        icon.classList.remove('fa-eye');
                        icon.classList.add('fa-eye-slash');
                    }
                } else {
                    inputField.type = 'password';
                    if (icon) {
                        icon.classList.remove('fa-eye-slash');
                        icon.classList.add('fa-eye');
                    }
                }
            }
        });
    });
}


/* ==========================================================================
   4. Auto-Dismiss Flash Messages
   ========================================================================== */
function initFlashMessages() {
    const alerts = document.querySelectorAll('.alert');

    alerts.forEach(alert => {
        const timer = setTimeout(() => {
            dismissAlert(alert);
        }, 5000);

        const closeBtn = alert.querySelector('.alert-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                clearTimeout(timer);
                dismissAlert(alert);
            });
        }
    });
}

function dismissAlert(alertElement) {
    alertElement.style.transition = 'opacity 0.35s ease, transform 0.35s ease';
    alertElement.style.opacity = '0';
    alertElement.style.transform = 'translateX(60px)';
    setTimeout(() => {
        alertElement.remove();
    }, 360);
}


/* ==========================================================================
   5. Crop Catalog Real-Time Search Filter (crops.html)
   ========================================================================== */
function initCropSearch() {
    const searchInput = document.getElementById('cropSearchInput');
    const cropCards = document.querySelectorAll('.crop-item-card');
    const noResults = document.getElementById('noCropsFound');

    if (searchInput && cropCards.length > 0) {
        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase().trim();
            let matchCount = 0;

            cropCards.forEach(card => {
                const name = (card.getAttribute('data-name') || '').toLowerCase();
                const region = (card.getAttribute('data-region') || '').toLowerCase();
                const season = (card.getAttribute('data-season') || '').toLowerCase();
                const type = (card.getAttribute('data-type') || '').toLowerCase();

                if (name.includes(query) || region.includes(query) || season.includes(query) || type.includes(query)) {
                    card.style.display = 'flex';
                    matchCount++;
                } else {
                    card.style.display = 'none';
                }
            });

            if (noResults) {
                noResults.style.display = (matchCount === 0) ? 'block' : 'none';
            }
        });
    }
}


/* ==========================================================================
   6. Farming Tips Category Filter Tabs (farming_tips.html)
   ========================================================================== */
function initTipsFilter() {
    const tabButtons = document.querySelectorAll('.filter-tabs .filter-btn, .tip-category-tab, .filter-btn[data-filter]');
    const categorySections = document.querySelectorAll('.tips-category-group, .tip-category-section');

    if (tabButtons.length > 0 && categorySections.length > 0) {
        tabButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                tabButtons.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                const targetFilter = btn.getAttribute('data-filter') || btn.getAttribute('data-category') || 'all';

                categorySections.forEach(section => {
                    const sectionSlug = section.getAttribute('data-slug') || section.getAttribute('data-category');
                    if (targetFilter === 'all' || sectionSlug === targetFilter) {
                        section.style.display = 'block';
                        section.style.opacity = '0';
                        section.style.transform = 'translateY(8px)';
                        section.style.transition = 'opacity 0.25s ease, transform 0.25s ease';
                        requestAnimationFrame(() => {
                            section.style.opacity = '1';
                            section.style.transform = 'translateY(0)';
                        });
                    } else {
                        section.style.display = 'none';
                    }
                });
            });
        });
    }
}


/* ==========================================================================
   7. Reusable Crop Delete Confirmation Modal
   ========================================================================== */
function initDeleteConfirmation() {
    const modalOverlay = document.getElementById('deleteModal');
    const modalCropName = document.getElementById('modalCropName');
    const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');
    const cancelDeleteBtn = document.getElementById('cancelDeleteBtn');

    if (modalOverlay) {
        let deleteTargetUrl = '';

        document.querySelectorAll('.btn-trigger-delete').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                deleteTargetUrl = btn.getAttribute('data-url');
                const cropName = btn.getAttribute('data-name') || 'this crop';
                if (modalCropName) modalCropName.textContent = cropName;
                modalOverlay.classList.add('active');
            });
        });

        if (confirmDeleteBtn) {
            confirmDeleteBtn.addEventListener('click', () => {
                if (deleteTargetUrl) {
                    window.location.href = deleteTargetUrl;
                }
            });
        }

        if (cancelDeleteBtn) {
            cancelDeleteBtn.addEventListener('click', () => {
                modalOverlay.classList.remove('active');
                deleteTargetUrl = '';
            });
        }

        modalOverlay.addEventListener('click', (e) => {
            if (e.target === modalOverlay) {
                modalOverlay.classList.remove('active');
                deleteTargetUrl = '';
            }
        });
    }
}


/* ==========================================================================
   8. Live Gujarat Agricultural WeatherAPI.com Integration & AJAX Lookup
   ========================================================================== */
function initWeatherSimulation() {
    const weatherForm = document.getElementById('weatherSearchForm');
    const districtSelect = document.getElementById('weatherDistrictSelect');
    const talukaInput = document.getElementById('weatherTalukaInput');
    const cityInput = document.getElementById('weatherCityInput');
    const loadingOverlay = document.getElementById('weatherLoadingOverlay');
    const errorBox = document.getElementById('weatherErrorBox');
    const errorTitle = document.getElementById('weatherErrorTitle');
    const errorMessage = document.getElementById('weatherErrorMessage');

    // UI elements for Current Weather
    const locationCityEl = document.getElementById('weatherCityDisplay');
    const tempEl = document.getElementById('weatherTempDisplay');
    const conditionEl = document.getElementById('weatherConditionDisplay');
    const conditionIconEl = document.getElementById('weatherConditionIcon');
    const feelsLikeEl = document.getElementById('weatherFeelsLikeDisplay');
    const humidityEl = document.getElementById('weatherHumidityDisplay');
    const windEl = document.getElementById('weatherWindDisplay');
    const rainEl = document.getElementById('weatherRainDisplay');
    const pressureEl = document.getElementById('weatherPressureDisplay');
    const visibilityEl = document.getElementById('weatherVisibilityDisplay');
    const sunriseEl = document.getElementById('weatherSunriseDisplay');
    const sunsetEl = document.getElementById('weatherSunsetDisplay');
    const lastUpdatedEl = document.getElementById('weatherLastUpdatedDisplay');

    // UI elements for Advice and Forecast
    const adviceSummaryEl = document.getElementById('weatherAdviceSummary');
    const adviceListEl = document.getElementById('weatherAdviceList');
    const adviceDisclaimerEl = document.getElementById('weatherAdviceDisclaimer');
    const forecastGridEl = document.getElementById('weatherForecastGrid');

    if (!weatherForm && !districtSelect) {
        return; // Not on weather page
    }

    function showLoading(show) {
        if (loadingOverlay) {
            loadingOverlay.style.display = show ? 'flex' : 'none';
        }
    }

    function showError(message, title = 'Gujarat Only Notice') {
        if (errorBox) {
            if (errorTitle) errorTitle.textContent = title;
            if (errorMessage) errorMessage.textContent = message;
            errorBox.style.display = 'block';
            errorBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        } else {
            alert(message);
        }
    }

    function hideError() {
        if (errorBox) {
            errorBox.style.display = 'none';
        }
    }

    async function fetchWeather(query) {
        if (!query || !query.trim()) return;
        const queryClean = query.trim();

        hideError();
        showLoading(true);

        try {
            const response = await fetch(`/api/weather/?city=${encodeURIComponent(queryClean)}`);
            const data = await response.json();

            if (!data.success) {
                showError(data.error || 'Please select a valid Gujarat location.');
                showLoading(false);
                return;
            }

            // 1. Update Current Weather Hero Elements
            if (locationCityEl) {
                locationCityEl.textContent = data.location_display || `${data.city}, ${data.district} (Gujarat, India)`;
            }
            if (tempEl) tempEl.textContent = `${data.temperature}°C`;
            if (conditionEl) conditionEl.textContent = data.condition;
            if (conditionIconEl && data.condition_icon) {
                conditionIconEl.src = data.condition_icon;
                conditionIconEl.alt = data.condition;
            }
            if (lastUpdatedEl) {
                lastUpdatedEl.textContent = data.last_updated || 'Just now';
            }

            // 2. Update Atmospheric Metric Boxes
            if (feelsLikeEl) feelsLikeEl.textContent = `${data.feels_like}°C`;
            if (humidityEl) humidityEl.textContent = `${data.humidity}%`;
            if (windEl) windEl.textContent = `${data.wind_speed} km/h`;
            if (pressureEl) pressureEl.textContent = `${data.pressure} mb`;
            if (visibilityEl) visibilityEl.textContent = `${data.visibility} km`;
            if (sunriseEl) sunriseEl.textContent = data.sunrise || '06:15 AM';
            if (sunsetEl) sunsetEl.textContent = data.sunset || '06:45 PM';

            // 3. Update Forecast Rain Chance in Hero
            if (rainEl && data.forecast && data.forecast.length > 0) {
                rainEl.textContent = `${data.forecast[0].rain_chance}%`;
            }

            // 4. Update Farming Weather Advice Section
            if (data.farming_advice) {
                if (adviceSummaryEl) adviceSummaryEl.textContent = data.farming_advice.summary || '';
                if (adviceDisclaimerEl) adviceDisclaimerEl.textContent = data.farming_advice.disclaimer || '';
                
                if (adviceListEl && Array.isArray(data.farming_advice.items)) {
                    adviceListEl.innerHTML = '';
                    data.farming_advice.items.forEach(item => {
                        let iconColor = '#176B2C';
                        if (item.type === 'danger') iconColor = '#DC2626';
                        else if (item.type === 'warning') iconColor = '#D97706';
                        else if (item.type === 'info') iconColor = '#0284C7';

                        const card = document.createElement('div');
                        card.className = `advisory-item-card advisory-${item.type || 'info'}`;
                        card.style.cssText = 'background: #FFFFFF; border: 1px solid var(--border); border-radius: var(--radius-md); padding: 1.15rem; display: flex; gap: 0.85rem; align-items: flex-start; box-shadow: var(--shadow-sm);';
                        card.innerHTML = `
                            <div style="font-size: 1.35rem; margin-top: 2px; color: ${iconColor};">
                                <i class="fa-solid ${item.icon || 'fa-circle-info'}"></i>
                            </div>
                            <div>
                                <strong style="display: block; font-size: 0.96rem; color: var(--primary-dark); margin-bottom: 0.25rem;">${item.title}</strong>
                                <p style="margin: 0; font-size: 0.88rem; color: var(--text-muted); line-height: 1.55;">${item.text}</p>
                            </div>
                        `;
                        adviceListEl.appendChild(card);
                    });
                }
            }

            // 5. Update 5-Day Forecast Grid
            if (forecastGridEl && Array.isArray(data.forecast)) {
                forecastGridEl.innerHTML = '';
                data.forecast.forEach(day => {
                    const rainColor = day.rain_chance > 40 ? '#DC2626' : 'var(--primary)';
                    const card = document.createElement('div');
                    card.className = 'card forecast-day-card';
                    card.style.cssText = 'text-align: center; padding: 1.35rem 0.85rem; box-shadow: var(--shadow-sm); border: 1px solid var(--border); transition: transform 0.2s, box-shadow 0.2s; border-radius: var(--radius-lg);';
                    card.innerHTML = `
                        <div style="font-weight: 800; color: var(--primary-dark); font-size: 1.05rem; margin-bottom: 0.2rem;">${day.day_name}</div>
                        <div style="font-size: 0.78rem; color: var(--text-muted); margin-bottom: 0.5rem;">${day.formatted_date || day.date}</div>
                        
                        <img src="${day.icon}" alt="${day.condition}" style="width: 52px; height: 52px; margin: 0 auto 0.4rem; display: block;">
                        
                        <div style="font-size: 1.2rem; font-weight: 800; color: var(--primary); margin-bottom: 0.35rem;">
                            ${day.max_temp}° <span style="font-size: 0.95rem; font-weight: 600; color: var(--text-muted);">/ ${day.min_temp}°C</span>
                        </div>
                        
                        <div style="font-size: 0.82rem; font-weight: 600; color: var(--text); margin-bottom: 0.5rem; min-height: 2.2em; display: flex; align-items: center; justify-content: center;">
                            ${day.condition}
                        </div>
                        
                        <div style="display: flex; flex-direction: column; gap: 0.25rem; font-size: 0.78rem; border-top: 1px solid var(--border); padding-top: 0.5rem; text-align: left;">
                            <div style="display: flex; justify-content: space-between;">
                                <span style="color: var(--text-muted);"><i class="fa-solid fa-cloud-rain" style="color: #0284C7;"></i> Rain:</span>
                                <strong style="color: ${rainColor};">${day.rain_chance}%</strong>
                            </div>
                            <div style="display: flex; justify-content: space-between;">
                                <span style="color: var(--text-muted);"><i class="fa-solid fa-droplet" style="color: #0284C7;"></i> Precip:</span>
                                <strong>${day.precip_mm} mm</strong>
                            </div>
                            <div style="display: flex; justify-content: space-between;">
                                <span style="color: var(--text-muted);"><i class="fa-solid fa-wind" style="color: #6B7280;"></i> Max Wind:</span>
                                <strong>${day.max_wind_kph} km/h</strong>
                            </div>
                        </div>
                    `;
                    forecastGridEl.appendChild(card);
                });
            }
        } catch (err) {
            showError('Could not connect to Gujarat weather service. Please check your connection.');
        } finally {
            showLoading(false);
        }
    }

    // District Selector Handler
    if (districtSelect) {
        districtSelect.addEventListener('change', () => {
            const selectedDist = districtSelect.value;
            if (cityInput) cityInput.value = selectedDist;
            if (talukaInput) {
                talukaInput.value = '';
                loadTalukasForDatalist(selectedDist, 'weather_taluka_datalist');
            }
            fetchWeather(selectedDist);
        });

        // Initialize talukas for selected district on page load
        if (districtSelect.value) {
            loadTalukasForDatalist(districtSelect.value, 'weather_taluka_datalist');
        }
    }

    // Taluka change handler
    if (talukaInput) {
        talukaInput.addEventListener('change', () => {
            const taluka = talukaInput.value.trim();
            const dist = districtSelect ? districtSelect.value : '';
            if (taluka) {
                const combined = `${taluka}, ${dist}`;
                if (cityInput) cityInput.value = combined;
                fetchWeather(combined);
            }
        });
    }

    // Form Search Handler
    if (weatherForm && cityInput) {
        weatherForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const val = cityInput.value.trim();
            if (val) fetchWeather(val);
        });
    }

    // Quick City Shortcuts
    document.querySelectorAll('.btn-quick-city').forEach(btn => {
        btn.addEventListener('click', () => {
            const city = btn.getAttribute('data-city');
            if (city) {
                if (cityInput) cityInput.value = city;
                if (districtSelect) {
                    for (let opt of districtSelect.options) {
                        if (opt.value.toLowerCase() === city.toLowerCase()) {
                            districtSelect.value = opt.value;
                            if (talukaInput) {
                                talukaInput.value = '';
                                loadTalukasForDatalist(opt.value, 'weather_taluka_datalist');
                            }
                            break;
                        }
                    }
                }
                fetchWeather(city);
            }
        });
    });
}


/* ==========================================================================
   9. 6-Digit OTP Verification Form & Countdown Timers
   ========================================================================== */
function initOtpVerification() {
    const otpBoxes = document.querySelectorAll('.otp-box-input');
    const fullOtpInput = document.getElementById('otp_full_code');
    const timerDisplay = document.getElementById('otpTimerDisplay');
    const resendBtn = document.getElementById('resendOtpBtn');
    const resendCooldownDisplay = document.getElementById('resendCooldownTimer');

    if (otpBoxes.length === 6) {
        otpBoxes.forEach((box, index) => {
            box.addEventListener('input', (e) => {
                const val = e.target.value;
                if (val.length === 1 && index < 5) {
                    otpBoxes[index + 1].focus();
                }
                updateFullOtpCode();
            });

            box.addEventListener('keydown', (e) => {
                if (e.key === 'Backspace' && !box.value && index > 0) {
                    otpBoxes[index - 1].focus();
                }
            });

            box.addEventListener('paste', (e) => {
                e.preventDefault();
                const pasteData = (e.clipboardData || window.clipboardData).getData('text').trim();
                if (/^\d{6}$/.test(pasteData)) {
                    pasteData.split('').forEach((digit, i) => {
                        if (otpBoxes[i]) otpBoxes[i].value = digit;
                    });
                    updateFullOtpCode();
                    otpBoxes[5].focus();
                }
            });
        });

        function updateFullOtpCode() {
            let code = '';
            otpBoxes.forEach(b => { code += b.value; });
            if (fullOtpInput) fullOtpInput.value = code;
        }

        // 1. Expiration Countdown Timer
        if (timerDisplay) {
            let remainingSec = parseInt(timerDisplay.getAttribute('data-remaining') || '180', 10);
            const interval = setInterval(() => {
                remainingSec--;
                if (remainingSec <= 0) {
                    clearInterval(interval);
                    timerDisplay.textContent = '00:00 (Expired)';
                    timerDisplay.style.color = '#DC2626';
                } else {
                    const m = Math.floor(remainingSec / 60);
                    const s = remainingSec % 60;
                    timerDisplay.textContent = `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
                }
            }, 1000);
        }

        // 2. Resend 60-Second Cooldown Timer
        if (resendCooldownDisplay) {
            let cooldown = parseInt(resendCooldownDisplay.getAttribute('data-cooldown') || '60', 10);
            if (cooldown > 0 && resendBtn) {
                resendBtn.style.pointerEvents = 'none';
                resendBtn.style.opacity = '0.5';

                const cooldownInterval = setInterval(() => {
                    cooldown--;
                    if (cooldown <= 0) {
                        clearInterval(cooldownInterval);
                        resendCooldownDisplay.textContent = '';
                        resendBtn.style.pointerEvents = 'auto';
                        resendBtn.style.opacity = '1';
                    } else {
                        resendCooldownDisplay.textContent = ` (Wait ${cooldown}s)`;
                    }
                }, 1000);
            }
        }
    }
}


/* ==========================================================================
   10. Scroll Reveal Animations
   ========================================================================== */
function initScrollReveal() {
    const revealElements = document.querySelectorAll('.card-3d, .stat-card, .feature-card');

    if ('IntersectionObserver' in window && revealElements.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });

        revealElements.forEach(el => observer.observe(el));
    }
}


/* ==========================================================================
   11. Back to Top Button
   ========================================================================== */
function initBackToTop() {
    const backToTopBtn = document.getElementById('backToTopBtn');
    if (!backToTopBtn) return;

    window.addEventListener('scroll', () => {
        if (window.scrollY > 350) {
            backToTopBtn.classList.add('visible');
        } else {
            backToTopBtn.classList.remove('visible');
        }
    }, { passive: true });

    backToTopBtn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}


/* ==========================================================================
   12. 3D Card Hover Tilt Effects
   ========================================================================== */
function init3DTiltEffects() {
    const tiltCards = document.querySelectorAll('.card-3d');

    tiltCards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const rotateX = ((y - centerY) / centerY) * -4;
            const rotateY = ((x - centerX) / centerX) * 4;

            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-4px)`;
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0)';
        });
    });
}


/* ==========================================================================
   13. Gujarat Location Dependent Dropdowns (District -> Taluka -> Village)
   ========================================================================== */

/**
 * Loads Talukas for a given Gujarat District into a <datalist> or <select>
 */
async function loadTalukasForDatalist(districtName, datalistId) {
    if (!districtName) return;
    const datalist = document.getElementById(datalistId);
    if (!datalist) return;

    try {
        const res = await fetch(`/api/talukas/?district_name=${encodeURIComponent(districtName.trim())}`);
        const data = await res.json();
        if (data.success && Array.isArray(data.talukas)) {
            datalist.innerHTML = '';
            data.talukas.forEach(t => {
                const opt = document.createElement('option');
                opt.value = t.name;
                datalist.appendChild(opt);
            });
        }
    } catch (e) {
        console.warn('Could not fetch talukas:', e);
    }
}

/**
 * Loads Villages for a given Gujarat Taluka into a <datalist>
 */
async function loadVillagesForDatalist(talukaName, datalistId) {
    if (!talukaName) return;
    const datalist = document.getElementById(datalistId);
    if (!datalist) return;

    try {
        const res = await fetch(`/api/villages/?taluka_name=${encodeURIComponent(talukaName.trim())}`);
        const data = await res.json();
        if (data.success && Array.isArray(data.villages)) {
            datalist.innerHTML = '';
            data.villages.forEach(v => {
                const opt = document.createElement('option');
                opt.value = v.name;
                datalist.appendChild(opt);
            });
        }
    } catch (e) {
        console.warn('Could not fetch villages:', e);
    }
}

/**
 * Binds location cascading behavior across all form pairs (Register, Profile, Add Crop, Edit Crop)
 */
function initGujaratLocationDropdowns() {
    const pairs = [
        { dist: 'reg_district', taluka: 'reg_taluka', talukaList: 'reg_taluka_datalist', village: 'reg_farm_location', villageList: 'reg_village_datalist' },
        { dist: 'profile_district', taluka: 'profile_taluka', talukaList: 'profile_taluka_datalist', village: 'profile_farm_location', villageList: 'profile_village_datalist' },
        { dist: 'crop_district', taluka: 'crop_taluka', talukaList: 'crop_taluka_datalist', village: 'crop_village', villageList: 'crop_village_datalist' },
        { dist: 'user_district', taluka: 'user_taluka', talukaList: null, village: 'user_farm_location', villageList: null }
    ];

    pairs.forEach(pair => {
        const distEl = document.getElementById(pair.dist);
        const talukaEl = document.getElementById(pair.taluka);
        const villageEl = document.getElementById(pair.village);

        if (distEl) {
            // Bind datalists if specified
            if (pair.talukaList && talukaEl) {
                talukaEl.setAttribute('list', pair.talukaList);
            }
            if (pair.villageList && villageEl) {
                villageEl.setAttribute('list', pair.villageList);
            }

            // On District Change
            distEl.addEventListener('change', () => {
                const distVal = distEl.value;
                if (pair.talukaList) {
                    loadTalukasForDatalist(distVal, pair.talukaList);
                }
                if (talukaEl && !talukaEl.value) {
                    talukaEl.placeholder = `Select Taluka in ${distVal}...`;
                }
            });

            // Initial load for pre-selected district
            if (distEl.value && pair.talukaList) {
                loadTalukasForDatalist(distEl.value, pair.talukaList);
            }

            // On Taluka Input / Change
            if (talukaEl && pair.villageList) {
                talukaEl.addEventListener('input', () => {
                    const talukaVal = talukaEl.value.trim();
                    if (talukaVal.length >= 2) {
                        loadVillagesForDatalist(talukaVal, pair.villageList);
                    }
                });
                if (talukaEl.value) {
                    loadVillagesForDatalist(talukaEl.value, pair.villageList);
                }
            }
        }
    });
}
