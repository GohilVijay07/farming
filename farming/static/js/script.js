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
});


/* ==========================================================================
   1. Mobile Navigation Toggle
   ========================================================================== */
function initMobileNav() {
    const hamburgerBtn = document.getElementById('hamburgerBtn');
    const navMenu = document.getElementById('navMenu');

    if (hamburgerBtn && navMenu) {
        hamburgerBtn.addEventListener('click', () => {
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
        // Auto-dismiss after 4500ms
        const timer = setTimeout(() => {
            dismissAlert(alert);
        }, 4500);

        // Allow manual close
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
                // Update active tab button
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

        // Close on clicking backdrop
        modalOverlay.addEventListener('click', (e) => {
            if (e.target === modalOverlay) {
                modalOverlay.classList.remove('active');
                deleteTargetUrl = '';
            }
        });
    }
}


/* ==========================================================================
   7. Interactive Weather Simulation & Lookup
   ========================================================================== */
function initWeatherSimulation() {
    const weatherForm = document.getElementById('weatherSearchForm');
    const locationCityEl = document.getElementById('weatherCityDisplay');
    const tempEl = document.getElementById('weatherTempDisplay');
    const conditionEl = document.getElementById('weatherConditionDisplay');
    const humidityEl = document.getElementById('weatherHumidityDisplay');
    const windEl = document.getElementById('weatherWindDisplay');
    const rainEl = document.getElementById('weatherRainDisplay');
    const advisoryEl = document.getElementById('weatherAdvisoryDisplay');

    const sampleLocations = {
        'green valley': {
            temp: '26°C',
            cond: 'Partly Cloudy',
            humidity: '65%',
            wind: '12 km/h',
            rain: '20%',
            advisory: 'Ideal conditions for field scouting and light fertilizer application. Favorable wind for spraying.'
        },
        'midwest farm': {
            temp: '22°C',
            cond: 'Clear & Sunny',
            humidity: '52%',
            wind: '9 km/h',
            rain: '5%',
            advisory: 'Excellent weather for harvesting and grain drying. Soil moisture levels are steady.'
        },
        'punjab': {
            temp: '29°C',
            cond: 'Warm & Sunny',
            humidity: '58%',
            wind: '14 km/h',
            rain: '10%',
            advisory: 'Morning irrigation is recommended. Check crop stands for early aphid activity.'
        },
        'california': {
            temp: '24°C',
            cond: 'Sunny',
            humidity: '45%',
            wind: '8 km/h',
            rain: '0%',
            advisory: 'Ensure optimal drip scheduling for fruit orchards. Low humidity helps avoid fungal outbreaks.'
        },
        'texas': {
            temp: '31°C',
            cond: 'Hot & Humid',
            humidity: '72%',
            wind: '18 km/h',
            rain: '35%',
            advisory: 'Monitor livestock shade and hydration. Afternoon showers possible; delay heavy pesticide spray.'
        }
    };

    if (weatherForm) {
        weatherForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const input = document.getElementById('weatherCityInput');
            if (!input) return;

            const city = input.value.trim();
            if (!city) return;

            const key = city.toLowerCase();
            const data = sampleLocations[key] || {
                temp: `${Math.floor(Math.random() * 12) + 20}°C`,
                cond: ['Partly Cloudy', 'Sunny', 'Light Breeze', 'Scattered Clouds'][Math.floor(Math.random() * 4)],
                humidity: `${Math.floor(Math.random() * 30) + 45}%`,
                wind: `${Math.floor(Math.random() * 15) + 8} km/h`,
                rain: `${Math.floor(Math.random() * 25)}%`,
                advisory: 'Standard agronomic conditions. Proceed with regular cultivation schedule and check soil moisture.'
            };

            if (locationCityEl) locationCityEl.textContent = city;
            if (tempEl) tempEl.textContent = data.temp;
            if (conditionEl) conditionEl.textContent = data.cond;
            if (humidityEl) humidityEl.textContent = data.humidity;
            if (windEl) windEl.textContent = data.wind;
            if (rainEl) rainEl.textContent = data.rain;
            if (advisoryEl) advisoryEl.textContent = data.advisory;
        });
    }
}
