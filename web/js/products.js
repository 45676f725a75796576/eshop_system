// Products Management Module
const Products = {
    currentProducts: [],
    
    // Load all products
    async loadProducts() {
        try {
            UI.showLoading();
            const products = await API.products.getAll();
            this.currentProducts = products;
            this.renderProducts(products);
        } catch (error) {
            console.error('Error loading products:', error);
            UI.alert('Failed to load products: ' + error.message);
        } finally {
            UI.hideLoading();
        }
    },
    
    // Render products table
    renderProducts(products) {
        const tbody = document.getElementById('productsTableBody');
        tbody.innerHTML = '';
        
        if (!products || products.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; padding: 40px;">No products found</td></tr>';
            return;
        }
        
        products.forEach(product => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${product.id}</td>
                <td>${product.product_name}</td>
                <td>${UI.formatCurrency(product.unit_price)}</td>
                <td>${(product.tax_rate * 100).toFixed(2)}%</td>
                <td>
                    <button class="btn-action" onclick="Products.editProduct(${product.id})">Edit</button>
                    <button class="btn-action btn-delete" onclick="Products.deleteProduct(${product.id})">Delete</button>
                </td>
            `;
            tbody.appendChild(row);
        });
    },
    
    // Edit product
    editProduct(productId) {
        const product = this.currentProducts.find(p => p.id === productId);
        if (!product) {
            UI.alert('Product not found');
            return;
        }
        
        openRecordModal('Edit Product', [
            { name: 'product_name', label: 'Product Name', type: 'text', value: product.product_name, required: true },
            { name: 'unit_price', label: 'Unit Price', type: 'number', value: product.unit_price, required: true, step: '0.01', min: '0' },
            { name: 'tax_rate', label: 'Tax Rate (0-1)', type: 'number', value: product.tax_rate, required: true, step: '0.01', min: '0', max: '1' }
        ], async (data) => {
            await API.products.update(productId, data);
            await this.loadProducts();
        });
    },
    
    // Delete product
    async deleteProduct(productId) {
        const product = this.currentProducts.find(p => p.id === productId);
        const productName = product ? product.product_name : 'this product';
        
        if (!UI.confirm(`Are you sure you want to delete ${productName}? This action cannot be undone.`)) {
            return;
        }
        
        try {
            UI.showLoading();
            await API.products.delete(productId);
            await this.loadProducts();
        } catch (error) {
            console.error('Error deleting product:', error);
            UI.alert('Failed to delete product: ' + error.message);
        } finally {
            UI.hideLoading();
        }
    }
};

// Global function to create new product
function createProduct() {
    openRecordModal('Create New Product', [
        { name: 'product_name', label: 'Product Name', type: 'text', required: true },
        { name: 'unit_price', label: 'Unit Price', type: 'number', required: true, step: '0.01', min: '0' },
        { name: 'tax_rate', label: 'Tax Rate (0-1, e.g., 0.21 for 21%)', type: 'number', required: true, step: '0.01', min: '0', max: '1' }
    ], async (data) => {
        await API.products.create(data);
        await Products.loadProducts();
    });
}
