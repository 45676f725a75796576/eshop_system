// UI Helper Functions
const UI = {
    // Show loading overlay
    showLoading() {
        document.getElementById('loadingOverlay').classList.add('show');
    },
    
    // Hide loading overlay
    hideLoading() {
        document.getElementById('loadingOverlay').classList.remove('show');
    },
    
    // Show error message
    showError(elementId, message) {
        const errorElement = document.getElementById(elementId);
        if (errorElement) {
            errorElement.textContent = message;
            errorElement.classList.add('show');
            setTimeout(() => {
                errorElement.classList.remove('show');
            }, 5000);
        }
    },
    
    // Show section
    showSection(sectionName) {
        // Hide all sections
        document.querySelectorAll('.content-section').forEach(section => {
            section.classList.remove('active');
        });
        
        // Show selected section
        const section = document.getElementById(`${sectionName}Section`);
        if (section) {
            section.classList.add('active');
        }
        
        // Update navigation active state
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
            if (link.dataset.section === sectionName) {
                link.classList.add('active');
            }
        });
    },
    
    // Confirm dialog (using browser's confirm for simplicity)
    confirm(message) {
        return window.confirm(message);
    },
    
    // Alert dialog
    alert(message) {
        window.alert(message);
    },
    
    // Format currency
    formatCurrency(amount, currency = 'USD') {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: currency
        }).format(amount);
    },
    
    // Format date
    formatDate(dateString) {
        if (!dateString) return '-';
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    },
    
    // Truncate text with ellipsis
    truncate(text, maxLength = 50) {
        if (!text) return '';
        return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
    },
    
    // Create status badge
    createStatusBadge(status) {
        const badge = document.createElement('span');
        badge.className = `status-badge ${status.toLowerCase()}`;
        badge.textContent = status;
        return badge;
    },
    
    // Create active indicator
    createActiveIndicator(isActive) {
        const indicator = document.createElement('span');
        indicator.className = `active-indicator ${isActive ? 'active' : 'inactive'}`;
        indicator.textContent = isActive ? 'Active' : 'Inactive';
        return indicator;
    }
};

// Global function to show section (called from HTML)
function showSection(sectionName) {
    UI.showSection(sectionName);
}

// Modal management functions
function openRecordModal(title, fields, onSubmit) {
    const modal = document.getElementById('recordModal');
    const modalTitle = document.getElementById('modalTitle');
    const formFields = document.getElementById('modalFormFields');
    const form = document.getElementById('recordForm');
    
    modalTitle.textContent = title;
    formFields.innerHTML = '';
    
    // Create form fields
    fields.forEach(field => {
        const formGroup = document.createElement('div');
        formGroup.className = 'form-group';
        
        const label = document.createElement('label');
        label.textContent = field.label;
        label.htmlFor = field.name;
        
        let input;
        if (field.type === 'select') {
            input = document.createElement('select');
            input.id = field.name;
            input.name = field.name;
            input.required = field.required || false;
            
            // Add options
            if (field.options) {
                field.options.forEach(option => {
                    const opt = document.createElement('option');
                    opt.value = option.value;
                    opt.textContent = option.label;
                    if (option.value === field.value) {
                        opt.selected = true;
                    }
                    input.appendChild(opt);
                });
            }
        } else if (field.type === 'textarea') {
            input = document.createElement('textarea');
            input.id = field.name;
            input.name = field.name;
            input.value = field.value || '';
            input.required = field.required || false;
            input.rows = 4;
        } else if (field.type === 'checkbox') {
            input = document.createElement('input');
            input.type = 'checkbox';
            input.id = field.name;
            input.name = field.name;
            input.checked = field.value || false;
        } else {
            input = document.createElement('input');
            input.type = field.type || 'text';
            input.id = field.name;
            input.name = field.name;
            input.value = field.value || '';
            input.required = field.required || false;
            if (field.type === 'number') {
                input.step = field.step || 'any';
                input.min = field.min !== undefined ? field.min : '';
            }
        }
        
        formGroup.appendChild(label);
        formGroup.appendChild(input);
        formFields.appendChild(formGroup);
    });
    
    // Set up form submission
    form.onsubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData(form);
        const data = {};
        
        fields.forEach(field => {
            if (field.type === 'checkbox') {
                data[field.name] = formData.get(field.name) === 'on';
            } else if (field.type === 'number') {
                const value = formData.get(field.name);
                data[field.name] = value ? parseFloat(value) : 0;
            } else if (field.type === 'json') {
                try {
                    data[field.name] = JSON.parse(formData.get(field.name));
                } catch (e) {
                    data[field.name] = {};
                }
            } else {
                data[field.name] = formData.get(field.name);
            }
        });
        
        try {
            UI.showLoading();
            await onSubmit(data);
            closeRecordModal();
        } catch (error) {
            UI.showError('recordError', error.message);
        } finally {
            UI.hideLoading();
        }
    };
    
    modal.style.display = 'flex';
}

function closeRecordModal() {
    const modal = document.getElementById('recordModal');
    modal.style.display = 'none';
    document.getElementById('recordError').classList.remove('show');
}

// Toggle expandable rows
function toggleExpandableRow(rowId) {
    const row = document.getElementById(rowId);
    const expandedContent = document.getElementById(`${rowId}-expanded`);
    
    if (row && expandedContent) {
        row.classList.toggle('expanded');
        expandedContent.classList.toggle('show');
    }
}
