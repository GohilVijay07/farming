/**
 * AgriConnect — Smart Farming Management System
 * Global Modern JavaScript Interactive Framework & Micro-Interactions
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
        if (alertElement.parentNode) {
            alertElement.parentNode.removeChild(alertElement);
        }
    }, 350);
}


/* ==========================================================================
   5. Real-time Crop Search Filter
   ========================================================================== */
function initCropSearch() {
    const searchInput = document.getElementById('cropSearchInput');
    const cropCards = document.querySelectorAll('.crop-item-card');
    const noResultsMsg = document.getElementById('noCropResults');

    if (searchInput && cropCards.length > 0) {
        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase().trim();
            let visibleCount = 0;

            cropCards.forEach(card => {
                const name = card.getAttribute('data-name') || '';
                const type = card.getAttribute('data-type') || '';
                const season = card.getAttribute('data-season') || '';
                const soil = card.getAttribute('data-soil') || '';
                const description = card.querySelector('.crop-description')?.textContent || '';

                const combinedText = `${name} ${type} ${season} ${soil} ${description}`.toLowerCase();

                if (combinedText.includes(query)) {
                    card.style.display = 'flex';
                    visibleCount++;
                } else {
                    card.style.display = 'none';
                }
            });

            if (noResultsMsg) {
                noResultsMsg.style.display = (visibleCount === 0) ? 'block' : 'none';
            }
        });
    }
}


/* ==========================================================================
   6. Farming Tips Category Filter Tabs
   ========================================================================== */
function initTipsFilter() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const tipGroups = document.querySelectorAll('.tips-category-group');

    if (filterButtons.length > 0 && tipGroups.length > 0) {
        filterButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                filterButtons.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                const targetCategory = btn.getAttribute('data-filter');

                tipGroups.forEach(group => {
                    const groupSlug = group.getAttribute('data-slug');
                    if (targetCategory === 'all' || groupSlug === targetCategory) {
                        group.style.display = 'block';
                    } else {
                        group.style.display = 'none';
                    }
                });
            });
        });
    }
}


/* ==========================================================================
   7. Delete Confirmation Modal
   ========================================================================== */
let deleteTargetUrl = '';

function initDeleteConfirmation() {
    const deleteButtons = document.querySelectorAll('.btn-trigger-delete');
    const modalOverlay = document.getElementById('deleteModal');
    const modalCropName = document.getElementById('modalCropName');
    const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');
    const cancelDeleteBtn = document.getElementById('cancelDeleteBtn');

    if (deleteButtons.length > 0 && modalOverlay) {
        deleteButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                deleteTargetUrl = btn.getAttribute('data-url');
                const cropName = btn.getAttribute('data-name') || 'this crop';

                if (modalCropName) {
                    modalCropName.textContent = cropName;
                }

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
    const uvEl = document.getElementById('weatherUvDisplay');
    const precipEl = document.getElementById('weatherPrecipDisplay');
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

    async function fetchWeather(city) {
        if (!city || !city.trim()) return;
        const queryCity = city.trim();

        hideError();
        showLoading(true);

        try {
            const response = await fetch(`/api/weather/?city=${encodeURIComponent(queryCity)}`);
            const data = await response.json();

            if (!data.success) {
                showError(data.error || 'AgriConnect provides weather information only for Gujarat.');
                showLoading(false);
                return;
            }

            // 1. Update Current Weather Hero Elements
            if (locationCityEl) {
                locationCityEl.textContent = `${data.city}, ${data.district} (Gujarat, India)`;
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
            if (windEl) {
                windEl.innerHTML = `${data.wind_speed} km/h <span style="font-size: 0.8rem; font-weight: 500; opacity: 0.85;">${data.wind_dir || ''}</span>`;
            }
            if (pressureEl) pressureEl.textContent = `${data.pressure} mb`;
            if (visibilityEl) visibilityEl.textContent = `${data.visibility} km`;
            if (uvEl) uvEl.textContent = `${data.uv_index}`;
            if (precipEl) precipEl.textContent = `${data.precipitation} mm`;

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

            // 6. Sync inputs
            if (cityInput) cityInput.value = data.city;
            if (districtSelect) {
                for (let i = 0; i < districtSelect.options.length; i++) {
                    const optVal = districtSelect.options[i].value.toLowerCase();
                    if (optVal === data.district.toLowerCase() || optVal === data.city.toLowerCase()) {
                        districtSelect.selectedIndex = i;
                        break;
                    }
                }
            }

        } catch (err) {
            showError('Weather information is temporarily unavailable. Please try again later.', 'Connection Notice');
        } finally {
            showLoading(false);
        }
    }

    // Dropdown change listener
    if (districtSelect) {
        districtSelect.addEventListener('change', () => {
            const selected = districtSelect.value;
            if (selected) {
                fetchWeather(selected);
            }
        });
    }

    // Search form submit listener
    if (weatherForm) {
        weatherForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const inputVal = cityInput?.value;
            if (inputVal && inputVal.trim()) {
                fetchWeather(inputVal.trim());
            }
        });
    }

    // Quick District Badges
    const quickButtons = document.querySelectorAll('.btn-quick-city');
    quickButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const city = btn.getAttribute('data-city');
            if (city) {
                fetchWeather(city);
            }
        });
    });
}


/* ==========================================================================
   9. 6-Digit Email OTP Verification & Timers
   ========================================================================== */
function initOtpVerification() {
    const otpForm = document.getElementById('otpForm');
    if (!otpForm) return;

    const otpInputs = Array.from(document.querySelectorAll('.otp-box-input'));
    const fullOtpInput = document.getElementById('otp_full_code');
    const timerDisplay = document.getElementById('otpTimerDisplay');
    const resendBtn = document.getElementById('resendOtpBtn');
    const resendNotice = document.getElementById('resendCooldownNotice');
    const resendText = document.getElementById('resendBtnText');

    // Auto-focus and navigation among 6 digit inputs
    otpInputs.forEach((input, index) => {
        input.addEventListener('input', (e) => {
            const val = e.target.value.replace(/[^0-9]/g, '');
            input.value = val ? val[0] : '';

            if (input.value && index < otpInputs.length - 1) {
                otpInputs[index + 1].focus();
            }

            syncFullOtp();
        });

        input.addEventListener('keydown', (e) => {
            if (e.key === 'Backspace' && !input.value && index > 0) {
                otpInputs[index - 1].focus();
            }
        });

        input.addEventListener('paste', (e) => {
            e.preventDefault();
            const pasteData = (e.clipboardData || window.clipboardData).getData('text').trim();
            const digits = pasteData.replace(/[^0-9]/g, '').slice(0, 6);

            digits.split('').forEach((d, i) => {
                if (otpInputs[i]) {
                    otpInputs[i].value = d;
                }
            });

            if (digits.length === 6) {
                otpInputs[5].focus();
            } else if (digits.length > 0 && digits.length < 6) {
                otpInputs[digits.length].focus();
            }

            syncFullOtp();
        });
    });

    function syncFullOtp() {
        const fullCode = otpInputs.map(inp => inp.value).join('');
        if (fullOtpInput) {
            fullOtpInput.value = fullCode;
        }
    }

    // Countdown Timer for OTP Expiration
    let remainingSeconds = parseInt(otpForm.getAttribute('data-remaining') || '180', 10);
    let cooldownSeconds = parseInt(otpForm.getAttribute('data-cooldown') || '0', 10);

    function formatTime(sec) {
        const m = Math.floor(sec / 60);
        const s = sec % 60;
        return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
    }

    if (timerDisplay && remainingSeconds > 0) {
        timerDisplay.textContent = formatTime(remainingSeconds);
        const countdownInterval = setInterval(() => {
            remainingSeconds--;
            if (remainingSeconds <= 0) {
                clearInterval(countdownInterval);
                timerDisplay.textContent = 'Expired';
                timerDisplay.style.color = '#DC2626';
            } else {
                timerDisplay.textContent = formatTime(remainingSeconds);
            }
        }, 1000);
    }

    // Resend Cooldown
    if (resendBtn && cooldownSeconds > 0) {
        resendBtn.classList.add('disabled');
        resendBtn.style.pointerEvents = 'none';
        resendBtn.style.opacity = '0.6';
        if (resendNotice) resendNotice.style.display = 'block';

        const cooldownInterval = setInterval(() => {
            cooldownSeconds--;
            if (cooldownSeconds <= 0) {
                clearInterval(cooldownInterval);
                resendBtn.classList.remove('disabled');
                resendBtn.style.pointerEvents = 'auto';
                resendBtn.style.opacity = '1';
                if (resendText) resendText.textContent = 'Resend OTP';
                if (resendNotice) resendNotice.style.display = 'none';
            } else {
                if (resendText) resendText.textContent = `Resend in ${cooldownSeconds}s`;
            }
        }, 1000);
    }

    // Ensure full code is synced before form submission
    otpForm.addEventListener('submit', (e) => {
        syncFullOtp();
        if (fullOtpInput && fullOtpInput.value.length < 6) {
            e.preventDefault();
            const errorBox = document.getElementById('otpErrorMessage');
            if (errorBox) {
                errorBox.textContent = 'Please enter all 6 digits of the OTP code.';
                errorBox.style.display = 'block';
            }
        }
    });
}


/* ==========================================================================
   10. Scroll Reveal Animations (Intersection Observer)
   ========================================================================== */
function initScrollReveal() {
    const revealElements = document.querySelectorAll('.card, .crop-card, .feature-card, .stat-card, .tip-card');
    if (!('IntersectionObserver' in window)) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    revealElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(15px)';
        el.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
        observer.observe(el);
    });
}


/* ==========================================================================
   11. Back to Top Button
   ========================================================================== */
function initBackToTop() {
    const backBtn = document.getElementById('backToTopBtn');
    if (!backBtn) return;

    window.addEventListener('scroll', () => {
        if (window.scrollY > 400) {
            backBtn.classList.add('visible');
        } else {
            backBtn.classList.remove('visible');
        }
    }, { passive: true });

    backBtn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}


/* ==========================================================================
   12. Subtle 3D Card Hover Tilt
   ========================================================================== */
function init3DTiltEffects() {
    const tiltCards = document.querySelectorAll('.card-3d, .hero-3d-base-card');
    
    tiltCards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const deltaX = (x - centerX) / centerX;
            const deltaY = (y - centerY) / centerY;
            
            const rotateX = deltaY * -4;
            const rotateY = deltaX * 4;
            
            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-6px)`;
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0)';
        });
    });
}
