// Main Application Controller
const App = {
    isConnected: false,
    
    // Initialize the application
    init() {
        this.setupConnectionForm();
        this.setupDisconnectButton();
        this.setupNavigation();
        this.showConnectionModal();
    },
    
    // Show connection modal on startup
    showConnectionModal() {
        document.getElementById('connectionModal').style.display = 'flex';
        document.getElementById('mainApp').style.display = 'none';
    },
    
    // Setup connection form
    setupConnectionForm() {
        const form = document.getElementById('connectionForm');
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            await this.connect();
        });
    },
    
    // Setup disconnect button
    setupDisconnectButton() {
        const disconnectBtn = document.getElementById('disconnectBtn');
        disconnectBtn.addEventListener('click', () => {
            if (UI.confirm('Are you sure you want to disconnect from the API server?')) {
                this.disconnect();
            }
        });
    },
    
    // Setup navigation
    setupNavigation() {
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const section = link.dataset.section;
                this.navigateToSection(section);
            });
        });
    },
    
    // Connect to API server
    async connect() {
        const host = document.getElementById('apiHost').value;
        const port = document.getElementById('apiPort').value;
        const password = document.getElementById('apiPassword').value;
        
        try {
            UI.showLoading();
            
            // Try to connect and authorize
            await API.init(host, port, password);
            
            this.isConnected = true;
            
            // Hide connection modal and show main app
            document.getElementById('connectionModal').style.display = 'none';
            document.getElementById('mainApp').style.display = 'flex';
            
            // Update connection info
            document.getElementById('connectionInfo').textContent = `${host}:${port}`;
            
            // Load initial section (orders)
            await this.navigateToSection('orders');
            
        } catch (error) {
            console.error('Connection error:', error);
            UI.showError('connectionError', 'Failed to connect: ' + error.message);
        } finally {
            UI.hideLoading();
        }
    },
    
    // Disconnect from API server
    async disconnect() {
        try {
            UI.showLoading();
            await API.logout();
            this.isConnected = false;
            
            // Show connection modal again
            this.showConnectionModal();
            
            // Clear form
            document.getElementById('apiPassword').value = '';
            
        } catch (error) {
            console.error('Disconnect error:', error);
        } finally {
            UI.hideLoading();
        }
    },
    
    // Navigate to a section and load its data
    async navigateToSection(sectionName) {
        UI.showSection(sectionName);
        
        // Load data for the section
        try {
            switch (sectionName) {
                case 'orders':
                    await Orders.loadOrders();
                    break;
                case 'products':
                    await Products.loadProducts();
                    break;
                case 'warehouses':
                    await Warehouses.loadWarehouses();
                    break;
                case 'reports':
                    // Reports section doesn't need to load data initially
                    break;
            }
        } catch (error) {
            console.error(`Error loading ${sectionName}:`, error);
            UI.alert(`Failed to load ${sectionName}: ` + error.message);
        }
    }
};

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    App.init();
});

// Handle page reload/close - warn if connected
window.addEventListener('beforeunload', (e) => {
    if (App.isConnected) {
        e.preventDefault();
        e.returnValue = 'You are still connected to the API server. Are you sure you want to leave?';
        return e.returnValue;
    }
});
