/**
 * AgriConnect — Smart Farming Management System
 * JavaScript Interactive Functionality
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Initialize Mobile Navigation
    initMobileNav();

    // 2. Initialize Password Show/Hide Toggles
    initPasswordToggles();

    // 3. Initialize Auto-dismiss for Flash Messages
    initFlashMessages();

    // 4. Initialize Crop Catalog Search Filter
    initCropSearch();

    // 5. Initialize Farming Tips Category Filter
    initTipsFilter();

    // 6. Initialize Crop Delete Confirmation Modal
    initDeleteConfirmation();

    // 7. Initialize Interactive Weather Page Lookup
    initWeatherSimulation();

    // 8. Initialize 6-Digit OTP Verification Form & Timers
    initOtpVerification();
});



/* ==========================================================================
   1. Mobile Navigation Toggle
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
   2. Password Visibility Toggle
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
   3. Auto-Dismiss Flash Messages
   ========================================================================== */
function initFlashMessages() {
    const alerts = document.querySelectorAll('.alert');

    alerts.forEach(alert => {
        const timer = setTimeout(() => {
            dismissAlert(alert);
        }, 4500);

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
    alertElement.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
    alertElement.style.opacity = '0';
    alertElement.style.transform = 'translateX(50px)';
    setTimeout(() => {
        if (alertElement.parentNode) {
            alertElement.parentNode.removeChild(alertElement);
        }
    }, 400);
}


/* ==========================================================================
   4. Real-time Crop Search Filter
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
   5. Farming Tips Category Filter
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
   6. Delete Confirmation Modal
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
   7. Live Gujarat Agricultural WeatherAPI.com Integration & AJAX Lookup
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
                        let iconColor = '#16A34A';
                        if (item.type === 'danger') iconColor = '#DC2626';
                        else if (item.type === 'warning') iconColor = '#D97706';
                        else if (item.type === 'info') iconColor = '#2563EB';

                        const card = document.createElement('div');
                        card.className = `advisory-item-card advisory-${item.type || 'info'}`;
                        card.style.cssText = 'background: #F9FAFB; border: 1px solid var(--border); border-radius: var(--radius-md); padding: 1.1rem; display: flex; gap: 0.85rem; align-items: flex-start;';
                        card.innerHTML = `
                            <div style="font-size: 1.25rem; margin-top: 2px; color: ${iconColor};">
                                <i class="fa-solid ${item.icon || 'fa-info-circle'}"></i>
                            </div>
                            <div>
                                <strong style="display: block; font-size: 0.95rem; color: var(--primary); margin-bottom: 0.25rem;">${item.title}</strong>
                                <p style="margin: 0; font-size: 0.88rem; color: var(--text-dark); line-height: 1.5;">${item.text}</p>
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
                        <div style="font-weight: 800; color: var(--primary); font-size: 1.05rem; margin-bottom: 0.2rem;">${day.day_name}</div>
                        <div style="font-size: 0.78rem; color: var(--text-muted); margin-bottom: 0.5rem;">${day.formatted_date || day.date}</div>
                        
                        <img src="${day.icon}" alt="${day.condition}" style="width: 52px; height: 52px; margin: 0 auto 0.4rem; display: block;">
                        
                        <div style="font-size: 1.2rem; font-weight: 800; color: var(--primary); margin-bottom: 0.35rem;">
                            ${day.max_temp}° <span style="font-size: 0.95rem; font-weight: 600; color: var(--text-muted);">/ ${day.min_temp}°C</span>
                        </div>
                        
                        <div style="font-size: 0.82rem; font-weight: 600; color: var(--text-dark); margin-bottom: 0.5rem; min-height: 2.2em; display: flex; align-items: center; justify-content: center;">
                            ${day.condition}
                        </div>
                        
                        <div style="display: flex; flex-direction: column; gap: 0.25rem; font-size: 0.78rem; border-top: 1px solid var(--border); padding-top: 0.5rem; text-align: left;">
                            <div style="display: flex; justify-content: space-between;">
                                <span style="color: var(--text-muted);"><i class="fa-solid fa-cloud-rain" style="color: #3B82F6;"></i> Rain:</span>
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
                if (cityInput) cityInput.value = selected;
                fetchWeather(selected);
            }
        });
    }

    // Search form submit listener
    if (weatherForm) {
        weatherForm.addEventListener('submit', (e) => {
            e.preventDefault();
            if (!cityInput) return;
            const city = cityInput.value.trim();
            if (!city) return;
            fetchWeather(city);
        });
    }

    // Quick Hub pills click listener
    document.querySelectorAll('.btn-quick-city').forEach(btn => {
        btn.addEventListener('click', () => {
            const city = btn.getAttribute('data-city');
            if (city) {
                if (cityInput) cityInput.value = city;
                fetchWeather(city);
            }
        });
    });
}


/* ==========================================================================
   8. 6-Digit Email OTP Verification Logic & Timers
   ========================================================================== */
function initOtpVerification() {
    const otpForm = document.getElementById('otpForm');
    if (!otpForm) return;

    const otpInputs = document.querySelectorAll('.otp-box-input');
    const fullOtpInput = document.getElementById('otp_full_code');
    const verifyBtn = document.getElementById('verifyOtpBtn');
    const otpErrorMsg = document.getElementById('otpErrorMessage');

    const timerDisplay = document.getElementById('otpTimerDisplay');
    const timerWrapper = document.getElementById('otpTimerWrapper');
    const timerText = document.getElementById('otpCountdownText');

    const resendBtn = document.getElementById('resendOtpBtn');
    const resendBtnText = document.getElementById('resendBtnText');
    const resendNotice = document.getElementById('resendCooldownNotice');

    // 1. Auto-Focus First Input Box on Load
    if (otpInputs.length > 0) {
        setTimeout(() => {
            otpInputs[0].focus();
        }, 150);
    }

    // Helper: Collect all 6 box values
    function getCombinedOtp() {
        let code = '';
        otpInputs.forEach(input => {
            code += input.value.trim();
        });
        return code;
    }

    // Helper: Update filled class and full OTP hidden input
    function syncOtpState() {
        otpInputs.forEach(input => {
            if (input.value.length === 1) {
                input.classList.add('filled');
            } else {
                input.classList.remove('filled');
            }
        });
        const combined = getCombinedOtp();
        if (fullOtpInput) fullOtpInput.value = combined;
        return combined;
    }

    // 2. Input and Keyboard Event Handlers for 6 Boxes
    otpInputs.forEach((input, index) => {
        // Enforce numeric only on keydown & handle navigation
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Backspace') {
                if (input.value === '') {
                    // Move to previous box and clear
                    if (index > 0) {
                        otpInputs[index - 1].focus();
                        otpInputs[index - 1].value = '';
                        syncOtpState();
                        e.preventDefault();
                    }
                } else {
                    input.value = '';
                    syncOtpState();
                    e.preventDefault();
                }
            } else if (e.key === 'ArrowLeft' && index > 0) {
                otpInputs[index - 1].focus();
                e.preventDefault();
            } else if (e.key === 'ArrowRight' && index < otpInputs.length - 1) {
                otpInputs[index + 1].focus();
                e.preventDefault();
            }
        });

        input.addEventListener('input', (e) => {
            let val = input.value.replace(/[^0-9]/g, '');
            if (val.length > 0) {
                input.value = val.charAt(val.length - 1); // Take single digit
                syncOtpState();
                // Advance focus to next input
                if (index < otpInputs.length - 1) {
                    otpInputs[index + 1].focus();
                }
            } else {
                input.value = '';
                syncOtpState();
            }
        });

        // 3. Paste Event Handler (Pastes 6 digits across all boxes)
        input.addEventListener('paste', (e) => {
            e.preventDefault();
            const clipboardData = (e.clipboardData || window.clipboardData).getData('text');
            const digits = clipboardData.replace(/[^0-9]/g, '').slice(0, 6);

            if (digits.length > 0) {
                digits.split('').forEach((char, i) => {
                    if (otpInputs[i]) {
                        otpInputs[i].value = char;
                    }
                });
                syncOtpState();
                const focusIndex = Math.min(digits.length, otpInputs.length - 1);
                otpInputs[focusIndex].focus();
            }
        });
    });

    // 4. Form Submit Validation
    otpForm.addEventListener('submit', (e) => {
        const combined = syncOtpState();
        if (combined.length !== 6 || !/^\d{6}$/.test(combined)) {
            e.preventDefault();
            if (otpErrorMsg) {
                otpErrorMsg.textContent = 'Please enter all 6 digits of your OTP code.';
                otpErrorMsg.style.display = 'block';
            }
            // Focus first empty box
            for (let i = 0; i < otpInputs.length; i++) {
                if (!otpInputs[i].value) {
                    otpInputs[i].focus();
                    break;
                }
            }
        }
    });

    // 5. Expiration Countdown (10 Minutes)
    let remainingSeconds = parseInt(otpForm.getAttribute('data-remaining') || '0', 10);
    const isExpiredServer = otpForm.getAttribute('data-expired') === 'true';

    function formatTime(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }

    function setExpiredState() {
        if (timerWrapper) timerWrapper.classList.add('expired');
        if (timerText) {
            timerText.innerHTML = '<strong style="color: #DC2626;">OTP Expired. Please request a new OTP.</strong>';
        }
        if (verifyBtn) {
            verifyBtn.disabled = true;
            verifyBtn.classList.add('btn-disabled');
        }
        otpInputs.forEach(input => {
            input.disabled = true;
        });
    }

    if (isExpiredServer || remainingSeconds <= 0) {
        setExpiredState();
    } else {
        if (timerDisplay) timerDisplay.textContent = formatTime(remainingSeconds);

        const expiryInterval = setInterval(() => {
            remainingSeconds--;
            if (remainingSeconds <= 0) {
                clearInterval(expiryInterval);
                setExpiredState();
            } else {
                if (timerDisplay) timerDisplay.textContent = formatTime(remainingSeconds);
            }
        }, 1000);
    }

    // 6. Resend Cooldown Countdown (60 Seconds)
    let cooldownSeconds = parseInt(otpForm.getAttribute('data-cooldown') || '0', 10);

    if (resendBtn && cooldownSeconds > 0) {
        resendBtn.classList.add('btn-disabled');
        resendBtn.style.pointerEvents = 'none';
        if (resendNotice) resendNotice.style.display = 'block';
        if (resendBtnText) resendBtnText.textContent = `Resend OTP in ${cooldownSeconds}s`;

        const cooldownInterval = setInterval(() => {
            cooldownSeconds--;
            if (cooldownSeconds <= 0) {
                clearInterval(cooldownInterval);
                resendBtn.classList.remove('btn-disabled');
                resendBtn.style.pointerEvents = 'auto';
                if (resendBtnText) resendBtnText.textContent = 'Resend OTP';
                if (resendNotice) resendNotice.style.display = 'none';
            } else {
                if (resendBtnText) resendBtnText.textContent = `Resend OTP in ${cooldownSeconds}s`;
            }
        }, 1000);
    }
}

