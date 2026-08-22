/**
 * AgriConnect — Professional Admin Dashboard Scripts
 * Handles mobile sidebar toggle, instant search filters, delete confirmation dialogs, and alerts.
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Mobile Sidebar Toggle & Backdrop
    const sidebarToggleBtn = document.getElementById('sidebarToggleBtn');
    const adminSidebar = document.getElementById('adminSidebar');
    const sidebarBackdrop = document.getElementById('sidebarBackdrop');

    if (sidebarToggleBtn && adminSidebar) {
        sidebarToggleBtn.addEventListener('click', () => {
            adminSidebar.classList.toggle('sidebar-open');
            if (sidebarBackdrop) {
                sidebarBackdrop.classList.toggle('active');
            }
        });
    }

    if (sidebarBackdrop) {
        sidebarBackdrop.addEventListener('click', () => {
            if (adminSidebar) adminSidebar.classList.remove('sidebar-open');
            sidebarBackdrop.classList.remove('active');
        });
    }

    // 2. Auto-dismiss Flash Alerts after 5 seconds
    const alertCloseBtns = document.querySelectorAll('.admin-alert-close');
    alertCloseBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const alertEl = e.target.closest('.admin-alert');
            if (alertEl) {
                alertEl.style.opacity = '0';
                alertEl.style.transform = 'translateX(50px)';
                setTimeout(() => alertEl.remove(), 250);
            }
        });
    });

    const floatingAlerts = document.querySelectorAll('.admin-alert');
    floatingAlerts.forEach(alert => {
        setTimeout(() => {
            if (alert && alert.parentElement) {
                alert.style.opacity = '0';
                alert.style.transform = 'translateX(50px)';
                setTimeout(() => alert.remove(), 250);
            }
        }, 5000);
    });

    // 3. Client-side Instant Table Filter (Search Box)
    const instantSearchInputs = document.querySelectorAll('[data-table-search]');
    instantSearchInputs.forEach(input => {
        const targetTableId = input.getAttribute('data-table-search');
        const targetTable = document.getElementById(targetTableId);
        if (!targetTable) return;

        input.addEventListener('keyup', () => {
            const term = input.value.toLowerCase().trim();
            const rows = targetTable.querySelectorAll('tbody tr');

            rows.forEach(row => {
                const text = row.innerText.toLowerCase();
                if (text.includes(term)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    });

    // 4. Modal Confirmation System
    const confirmModalBackdrop = document.getElementById('confirmModalBackdrop');
    const confirmModalForm = document.getElementById('confirmModalForm');
    const confirmModalText = document.getElementById('confirmModalText');
    const confirmModalCancel = document.getElementById('confirmModalCancel');

    window.openDeleteConfirmModal = function(actionUrl, message) {
        if (!confirmModalBackdrop || !confirmModalForm) {
            if (confirm(message || 'Are you sure you want to proceed?')) {
                const form = document.createElement('form');
                form.method = 'POST';
                form.action = actionUrl;
                const csrf = document.querySelector('[name=csrfmiddlewaretoken]');
                if (csrf) {
                    const input = document.createElement('input');
                    input.type = 'hidden';
                    input.name = 'csrfmiddlewaretoken';
                    input.value = csrf.value;
                    form.appendChild(input);
                }
                document.body.appendChild(form);
                form.submit();
            }
            return;
        }

        confirmModalForm.action = actionUrl;
        if (confirmModalText) {
            confirmModalText.innerText = message || 'Are you sure you want to delete this record? This action cannot be undone.';
        }
        confirmModalBackdrop.classList.add('active');
    };

    if (confirmModalCancel && confirmModalBackdrop) {
        confirmModalCancel.addEventListener('click', () => {
            confirmModalBackdrop.classList.remove('active');
        });
    }

    if (confirmModalBackdrop) {
        confirmModalBackdrop.addEventListener('click', (e) => {
            if (e.target === confirmModalBackdrop) {
                confirmModalBackdrop.classList.remove('active');
            }
        });
    }
});
