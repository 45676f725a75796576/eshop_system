// API Configuration and Helper Functions
const API = {
    baseUrl: '',
    token: null,
    
    // Initialize API connection
    init(host, port, password) {
        this.baseUrl = `http://${host}:${port}`;
        return this.authorize(password);
    },
    
    // Authorize with API server
    async authorize(password) {
        try {
            const response = await fetch(`${this.baseUrl}/authorize?password=${encodeURIComponent(password)}`);
            if (!response.ok) {
                throw new Error('Invalid password or connection failed');
            }
            const data = await response.json();
            this.token = data.token;
            return true;
        } catch (error) {
            console.error('Authorization error:', error);
            throw error;
        }
    },
    
    // Logout from API server
    async logout() {
        if (this.token) {
            try {
                await fetch(`${this.baseUrl}/logout?token=${this.token}`, {
                    method: 'DELETE'
                });
            } catch (error) {
                console.error('Logout error:', error);
            }
            this.token = null;
            this.baseUrl = '';
        }
    },
    
    // Generic request handler
    async request(endpoint, method = 'GET', data = null) {
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            }
        };
        
        if (data) {
            options.body = JSON.stringify(data);
        }
        
        try {
            const response = await fetch(`${this.baseUrl}${endpoint}`, options);
            
            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`HTTP ${response.status}: ${errorText}`);
            }
            
            // Handle empty responses
            const text = await response.text();
            return text ? JSON.parse(text) : {};
        } catch (error) {
            console.error('API request error:', error);
            throw error;
        }
    },
    
    // Orders API
    orders: {
        getAll() {
            return API.request('/orders/all');
        },
        
        getById(id) {
            return API.request(`/orders/${id}`);
        },
        
        create(data) {
            return API.request('/orders', 'POST', data);
        },
        
        update(id, data) {
            return API.request(`/orders/${id}`, 'PUT', data);
        },
        
        delete(id) {
            return API.request(`/orders/${id}`, 'DELETE');
        },
        
        // Order items
        getItems(orderId) {
            return API.request(`/orders/${orderId}/items`);
        },
        
        addItem(orderId, productId, quantity) {
            return API.request(`/orders/${orderId}/items`, 'POST', {
                product_id: productId,
                quantity: quantity
            });
        },
        
        removeItem(orderId, productName) {
            return API.request(`/orders/${orderId}/items`, 'DELETE', {
                name: productName
            });
        }
    },
    
    // Products API
    products: {
        getAll() {
            return API.request('/products/all');
        },
        
        getById(id) {
            return API.request(`/products/${id}`);
        },
        
        create(data) {
            return API.request('/products', 'POST', data);
        },
        
        update(id, data) {
            return API.request(`/products/${id}`, 'PUT', data);
        },
        
        delete(id) {
            return API.request(`/products/${id}`, 'DELETE');
        }
    },
    
    // Warehouses API
    warehouses: {
        getAll() {
            return API.request('/warehouses/all');
        },
        
        getById(id) {
            return API.request(`/warehouses/${id}`);
        },
        
        create(data) {
            return API.request('/warehouses', 'POST', data);
        },
        
        update(id, data) {
            return API.request(`/warehouses/${id}`, 'PUT', data);
        },
        
        delete(id) {
            return API.request(`/warehouses/${id}`, 'DELETE');
        }
    },
    
    // Inventory API
    inventory: {
        getAll() {
            return API.request('/inventory/all');
        },
        
        getByWarehouse(warehouseId) {
            return API.request(`/inventory/warehouse/${warehouseId}`);
        },
        
        getByProduct(productId) {
            return API.request(`/inventory/product/${productId}`);
        },
        
        getById(id) {
            return API.request(`/inventory/${id}`);
        },
        
        create(data) {
            return API.request('/inventory', 'POST', data);
        },
        
        update(id, data) {
            return API.request(`/inventory/${id}`, 'PUT', data);
        },
        
        delete(id) {
            return API.request(`/inventory/${id}`, 'DELETE');
        }
    },
    
    // Payments API
    payments: {
        create(data) {
            return API.request('/payments', 'POST', data);
        }
    },
    
    // Reports API
    reports: {
        getSales() {
            return API.request('/report/sales');
        },
        
        getStock() {
            return API.request('/report/stock');
        }
    }
};
