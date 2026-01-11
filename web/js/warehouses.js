// Warehouses Management Module
const Warehouses = {
    currentWarehouses: [],
    currentWarehouseId: null, // For inventory view
    currentProducts: [], // Cache for products
    
    // Load all warehouses
    async loadWarehouses() {
        try {
            UI.showLoading();
            const warehouses = await API.warehouses.getAll();
            const products = await API.products.getAll();
            
            this.currentWarehouses = warehouses;
            this.currentProducts = products;
            this.renderWarehouses(warehouses);
        } catch (error) {
            console.error('Error loading warehouses:', error);
            UI.alert('Failed to load warehouses: ' + error.message);
        } finally {
            UI.hideLoading();
        }
    },
    
    // Render warehouses table
    renderWarehouses(warehouses) {
        const tbody = document.getElementById('warehousesTableBody');
        tbody.innerHTML = '';
        
        if (!warehouses || warehouses.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; padding: 40px;">No warehouses found</td></tr>';
            return;
        }
        
        warehouses.forEach(warehouse => {
            const row = document.createElement('tr');
            
            const activeIndicator = UI.createActiveIndicator(warehouse.is_active);
            
            row.innerHTML = `
                <td>${warehouse.id}</td>
                <td>${warehouse.warehouse_name}</td>
                <td>${warehouse.location_code || '-'}</td>
                <td>${activeIndicator.outerHTML}</td>
                <td>
                    <button class="btn-action" onclick="Warehouses.viewInventory(${warehouse.id}, '${warehouse.warehouse_name}')">View Inventory</button>
                </td>
                <td>
                    <button class="btn-action" onclick="Warehouses.editWarehouse(${warehouse.id})">Edit</button>
                    <button class="btn-action btn-delete" onclick="Warehouses.deleteWarehouse(${warehouse.id})">Delete</button>
                </td>
            `;
            tbody.appendChild(row);
        });
    },
    
    // View inventory for a warehouse
    async viewInventory(warehouseId, warehouseName) {
        this.currentWarehouseId = warehouseId;
        document.getElementById('inventoryWarehouseName').textContent = warehouseName;
        
        UI.showSection('inventory');
        await this.loadInventory(warehouseId);
    },
    
    // Load inventory for a warehouse
    async loadInventory(warehouseId) {
        try {
            UI.showLoading();
            const inventory = await API.inventory.getByWarehouse(warehouseId);
            this.renderInventory(inventory);
        } catch (error) {
            console.error('Error loading inventory:', error);
            UI.alert('Failed to load inventory: ' + error.message);
        } finally {
            UI.hideLoading();
        }
    },
    
    // Render inventory table
    renderInventory(inventory) {
        const tbody = document.getElementById('inventoryTableBody');
        tbody.innerHTML = '';
        
        if (!inventory || inventory.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" style="text-align: center; padding: 40px;">No inventory items found</td></tr>';
            return;
        }
        
        inventory.forEach(item => {
            const product = this.currentProducts.find(p => p.id === item.product_id);
            const productName = product ? product.product_name : `Product ID ${item.product_id}`;
            
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${productName}</td>
                <td>${item.quantity_available || 0}</td>
                <td>${item.quantity_reserved || 0}</td>
                <td>
                    <button class="btn-action" onclick="Warehouses.editInventoryItem(${item.id})">Edit</button>
                    <button class="btn-action btn-delete" onclick="Warehouses.deleteInventoryItem(${item.id})">Delete</button>
                </td>
            `;
            tbody.appendChild(row);
        });
    },
    
    // Edit warehouse
    editWarehouse(warehouseId) {
        const warehouse = this.currentWarehouses.find(w => w.id === warehouseId);
        if (!warehouse) {
            UI.alert('Warehouse not found');
            return;
        }
        
        openRecordModal('Edit Warehouse', [
            { name: 'warehouse_name', label: 'Warehouse Name', type: 'text', value: warehouse.warehouse_name, required: true },
            { name: 'location_code', label: 'Location Code', type: 'text', value: warehouse.location_code || '', required: false },
            { name: 'is_active', label: 'Active', type: 'checkbox', value: warehouse.is_active }
        ], async (data) => {
            await API.warehouses.update(warehouseId, data);
            await this.loadWarehouses();
        });
    },
    
    // Delete warehouse
    async deleteWarehouse(warehouseId) {
        const warehouse = this.currentWarehouses.find(w => w.id === warehouseId);
        const warehouseName = warehouse ? warehouse.warehouse_name : 'this warehouse';
        
        if (!UI.confirm(`Are you sure you want to delete ${warehouseName}? This will also delete all inventory records for this warehouse.`)) {
            return;
        }
        
        try {
            UI.showLoading();
            await API.warehouses.delete(warehouseId);
            await this.loadWarehouses();
        } catch (error) {
            console.error('Error deleting warehouse:', error);
            UI.alert('Failed to delete warehouse: ' + error.message);
        } finally {
            UI.hideLoading();
        }
    },
    
    // Edit inventory item
    async editInventoryItem(inventoryId) {
        try {
            const item = await API.inventory.getById(inventoryId);
            const product = this.currentProducts.find(p => p.id === item.product_id);
            const productName = product ? product.product_name : `Product ID ${item.product_id}`;
            
            openRecordModal(`Edit Inventory: ${productName}`, [
                { name: 'quantity_available', label: 'Quantity Available', type: 'number', value: item.quantity_available, required: true, min: '0' },
                { name: 'quantity_reserved', label: 'Quantity Reserved', type: 'number', value: item.quantity_reserved, required: false, min: '0' }
            ], async (data) => {
                await API.inventory.update(inventoryId, data);
                await this.loadInventory(this.currentWarehouseId);
            });
        } catch (error) {
            console.error('Error loading inventory item:', error);
            UI.alert('Failed to load inventory item: ' + error.message);
        }
    },
    
    // Delete inventory item
    async deleteInventoryItem(inventoryId) {
        if (!UI.confirm('Are you sure you want to delete this inventory item?')) {
            return;
        }
        
        try {
            UI.showLoading();
            await API.inventory.delete(inventoryId);
            await this.loadInventory(this.currentWarehouseId);
        } catch (error) {
            console.error('Error deleting inventory item:', error);
            UI.alert('Failed to delete inventory item: ' + error.message);
        } finally {
            UI.hideLoading();
        }
    }
};

// Global function to create new warehouse
function createWarehouse() {
    openRecordModal('Create New Warehouse', [
        { name: 'warehouse_name', label: 'Warehouse Name', type: 'text', required: true },
        { name: 'location_code', label: 'Location Code', type: 'text', required: false },
        { name: 'is_active', label: 'Active', type: 'checkbox', value: true }
    ], async (data) => {
        await API.warehouses.create(data);
        await Warehouses.loadWarehouses();
    });
}

// Global function to create new inventory item
function createInventoryItem() {
    if (!Warehouses.currentWarehouseId) {
        UI.alert('No warehouse selected');
        return;
    }
    
    // Create product options
    const productOptions = Warehouses.currentProducts.map(p => ({
        value: p.id,
        label: p.product_name
    }));
    
    openRecordModal('Add Inventory Item', [
        { 
            name: 'product_id', 
            label: 'Product', 
            type: 'select', 
            required: true,
            options: [{ value: '', label: 'Select product...' }, ...productOptions]
        },
        { name: 'quantity_available', label: 'Quantity Available', type: 'number', required: true, min: '0', value: 0 },
        { name: 'quantity_reserved', label: 'Quantity Reserved', type: 'number', required: false, min: '0', value: 0 }
    ], async (data) => {
        // Add warehouse_id to the data
        data.warehouse_id = Warehouses.currentWarehouseId;
        await API.inventory.create(data);
        await Warehouses.loadInventory(Warehouses.currentWarehouseId);
    });
}
