// Main JavaScript file for Expense Tracker

// Utility functions
const utils = {
    /**
     * Format currency value
     * @param {number} amount - The amount to format
     * @returns {string} - Formatted currency string
     */
    formatCurrency(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(amount);
    },

    /**
     * Format date
     * @param {string|Date} date - The date to format
     * @returns {string} - Formatted date string
     */
    formatDate(date) {
        return new Date(date).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    },

    /**
     * Show toast notification
     * @param {string} message - The message to show
     * @param {string} type - The type of notification (success, error, info)
     */
    showToast(message, type = 'info') {
        // Create toast element
        const toastContainer = document.getElementById('toast-container') || this.createToastContainer();
        
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white bg-${type === 'error' ? 'danger' : type === 'success' ? 'success' : 'primary'} border-0`;
        toast.setAttribute('role', 'alert');
        toast.setAttribute('aria-live', 'assertive');
        toast.setAttribute('aria-atomic', 'true');
        
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        
        toastContainer.appendChild(toast);
        
        // Initialize and show toast
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
        
        // Remove toast element after it's hidden
        toast.addEventListener('hidden.bs.toast', () => {
            toast.remove();
        });
    },

    /**
     * Create toast container if it doesn't exist
     * @returns {HTMLElement} - The toast container element
     */
    createToastContainer() {
        const container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        container.style.zIndex = '1055';
        document.body.appendChild(container);
        return container;
    },

    /**
     * Make API request
     * @param {string} url - The API endpoint
     * @param {object} options - Fetch options
     * @returns {Promise} - The fetch promise
     */
    async apiRequest(url, options = {}) {
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            }
        };

        const config = { ...defaultOptions, ...options };
        
        try {
            const response = await fetch(url, config);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || `HTTP error! status: ${response.status}`);
            }
            
            return data;
        } catch (error) {
            console.error('API Request Error:', error);
            throw error;
        }
    },

    /**
     * Debounce function
     * @param {function} func - The function to debounce
     * @param {number} wait - The number of milliseconds to delay
     * @returns {function} - The debounced function
     */
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
};

// Global expense management functions
const expenseManager = {
    /**
     * Load expenses with optional filters
     * @param {object} filters - Filter parameters
     * @returns {Promise} - Promise resolving to expenses data
     */
    async loadExpenses(filters = {}) {
        const queryParams = new URLSearchParams(filters).toString();
        const url = `/api/expenses${queryParams ? '?' + queryParams : ''}`;
        
        try {
            return await utils.apiRequest(url);
        } catch (error) {
            utils.showToast('Failed to load expenses', 'error');
            throw error;
        }
    },

    /**
     * Create new expense
     * @param {object} expenseData - The expense data
     * @returns {Promise} - Promise resolving to created expense
     */
    async createExpense(expenseData) {
        try {
            const response = await utils.apiRequest('/api/expenses', {
                method: 'POST',
                body: JSON.stringify(expenseData)
            });
            
            utils.showToast('Expense added successfully!', 'success');
            return response;
        } catch (error) {
            utils.showToast(error.message || 'Failed to add expense', 'error');
            throw error;
        }
    },

    /**
     * Update existing expense
     * @param {number} id - The expense ID
     * @param {object} expenseData - The updated expense data
     * @returns {Promise} - Promise resolving to updated expense
     */
    async updateExpense(id, expenseData) {
        try {
            const response = await utils.apiRequest(`/api/expenses/${id}`, {
                method: 'PUT',
                body: JSON.stringify(expenseData)
            });
            
            utils.showToast('Expense updated successfully!', 'success');
            return response;
        } catch (error) {
            utils.showToast(error.message || 'Failed to update expense', 'error');
            throw error;
        }
    },

    /**
     * Delete expense
     * @param {number} id - The expense ID
     * @returns {Promise} - Promise resolving to deletion confirmation
     */
    async deleteExpense(id) {
        try {
            const response = await utils.apiRequest(`/api/expenses/${id}`, {
                method: 'DELETE'
            });
            
            utils.showToast('Expense deleted successfully!', 'success');
            return response;
        } catch (error) {
            utils.showToast(error.message || 'Failed to delete expense', 'error');
            throw error;
        }
    }
};

// Category management functions
const categoryManager = {
    /**
     * Load all categories
     * @returns {Promise} - Promise resolving to categories data
     */
    async loadCategories() {
        try {
            return await utils.apiRequest('/api/categories');
        } catch (error) {
            utils.showToast('Failed to load categories', 'error');
            throw error;
        }
    },

    /**
     * Create new category
     * @param {object} categoryData - The category data
     * @returns {Promise} - Promise resolving to created category
     */
    async createCategory(categoryData) {
        try {
            const response = await utils.apiRequest('/api/categories', {
                method: 'POST',
                body: JSON.stringify(categoryData)
            });
            
            utils.showToast('Category created successfully!', 'success');
            return response;
        } catch (error) {
            utils.showToast(error.message || 'Failed to create category', 'error');
            throw error;
        }
    }
};

// Form validation functions
const validation = {
    /**
     * Validate expense form data
     * @param {object} data - The form data to validate
     * @returns {object} - Validation result with isValid and errors
     */
    validateExpense(data) {
        const errors = [];
        
        if (!data.title?.trim()) {
            errors.push('Title is required');
        }
        
        if (!data.amount || isNaN(data.amount) || parseFloat(data.amount) <= 0) {
            errors.push('Amount must be a positive number');
        }
        
        if (!data.category_id) {
            errors.push('Category is required');
        }
        
        if (!data.date) {
            errors.push('Date is required');
        }
        
        return {
            isValid: errors.length === 0,
            errors
        };
    },

    /**
     * Validate category form data
     * @param {object} data - The form data to validate
     * @returns {object} - Validation result with isValid and errors
     */
    validateCategory(data) {
        const errors = [];
        
        if (!data.name?.trim()) {
            errors.push('Category name is required');
        }
        
        return {
            isValid: errors.length === 0,
            errors
        };
    }
};

// Chart utilities
const chartUtils = {
    /**
     * Create a pie chart
     * @param {string} canvasId - The canvas element ID
     * @param {object} data - The chart data
     * @param {object} options - Chart options
     */
    createPieChart(canvasId, data, options = {}) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return null;
        
        const defaultOptions = {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        };
        
        return new Chart(ctx, {
            type: 'doughnut',
            data: data,
            options: { ...defaultOptions, ...options }
        });
    },

    /**
     * Create a line chart
     * @param {string} canvasId - The canvas element ID
     * @param {object} data - The chart data
     * @param {object} options - Chart options
     */
    createLineChart(canvasId, data, options = {}) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return null;
        
        const defaultOptions = {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return utils.formatCurrency(value);
                        }
                    }
                }
            }
        };
        
        return new Chart(ctx, {
            type: 'line',
            data: data,
            options: { ...defaultOptions, ...options }
        });
    }
};

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});

// Export utilities for use in other scripts
window.ExpenseTracker = {
    utils,
    expenseManager,
    categoryManager,
    validation,
    chartUtils
};
