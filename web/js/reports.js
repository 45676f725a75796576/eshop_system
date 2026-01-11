// Reports Management Module
const Reports = {
    // View a report
    async viewReport(reportType) {
        UI.showSection('reportView');
        
        const titleElement = document.getElementById('reportViewTitle');
        const contentElement = document.getElementById('reportViewContent');
        
        try {
            UI.showLoading();
            
            if (reportType === 'sales') {
                titleElement.textContent = 'Sales Report';
                const data = await API.reports.getSales();
                console.log('Sales report data:', data);
                console.log('First item:', data && data.length > 0 ? data[0] : 'No data');
                this.renderSalesReport(data, contentElement);
                document.getElementById('salesReportUpdate').textContent = new Date().toLocaleString();
            } else if (reportType === 'stock') {
                titleElement.textContent = 'Stock Report';
                const data = await API.reports.getStock();
                console.log('Stock report data:', data);
                this.renderStockReport(data, contentElement);
                document.getElementById('stockReportUpdate').textContent = new Date().toLocaleString();
            }
        } catch (error) {
            console.error('Error loading report:', error);
            contentElement.innerHTML = `<p style="text-align: center; padding: 40px;">Failed to load report: ${error.message}</p>`;
        } finally {
            UI.hideLoading();
        }
    },
    
    // Render sales report
    renderSalesReport(data, container) {
        if (!data || data.length === 0) {
            container.innerHTML = '<p style="text-align: center; padding: 40px;">No sales data available</p>';
            return;
        }
        
        // Debug: log the first item to see what fields we have
        console.log('Sales report data sample:', data[0]);
        
        // Calculate summary statistics - handle different possible field names
        const totalOrders = new Set(data.map(item => item.order_id || item.id_order)).size;
        const totalRevenue = data.reduce((sum, item) => {
            const total = parseFloat(item.total_amount || item.item_total || item.total || 0);
            return sum + total;
        }, 0);
        const avgOrderValue = totalOrders > 0 ? totalRevenue / totalOrders : 0;
        
        // Group by product - handle various field name possibilities
        const productSales = {};
        data.forEach(item => {
            const productName = item.product_name || item.name || item.productName;
            if (!productName || productName === 'undefined') return; // Skip if no product name
            
            if (!productSales[productName]) {
                productSales[productName] = {
                    quantity: 0,
                    revenue: 0
                };
            }
            const qty = parseInt(item.quantity || item.qty || 0);
            const itemTotal = parseFloat(item.item_total || item.total || item.total_amount || 0);
            
            productSales[productName].quantity += isNaN(qty) ? 0 : qty;
            productSales[productName].revenue += isNaN(itemTotal) ? 0 : itemTotal;
        });
        
        // Convert to array and sort by revenue
        const topProducts = Object.entries(productSales)
            .map(([name, stats]) => ({ name, ...stats }))
            .filter(p => p.name && p.name !== 'undefined') // Filter out undefined names
            .sort((a, b) => b.revenue - a.revenue)
            .slice(0, 10);
        
        container.innerHTML = `
            <div class="report-grid">
                <div class="report-card">
                    <h3>Total Orders</h3>
                    <div class="value">${totalOrders}</div>
                    <div class="label">Orders processed</div>
                </div>
                <div class="report-card">
                    <h3>Total Revenue</h3>
                    <div class="value">${UI.formatCurrency(totalRevenue)}</div>
                    <div class="label">Across all orders</div>
                </div>
                <div class="report-card">
                    <h3>Average Order Value</h3>
                    <div class="value">${UI.formatCurrency(avgOrderValue)}</div>
                    <div class="label">Per order</div>
                </div>
            </div>
            
            ${topProducts.length > 0 ? `
            <div class="report-table">
                <h3>Top Selling Products</h3>
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Product Name</th>
                            <th>Quantity Sold</th>
                            <th>Revenue</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${topProducts.map(product => `
                            <tr>
                                <td>${product.name}</td>
                                <td>${product.quantity}</td>
                                <td>${UI.formatCurrency(product.revenue)}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
            ` : '<p style="text-align: center; padding: 20px;">No product sales data available</p>'}
            
            <div class="report-table">
                <h3>All Sales Details</h3>
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Order ID</th>
                            <th>Product</th>
                            <th>Quantity</th>
                            <th>Unit Price</th>
                            <th>Total</th>
                            <th>Date</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${data.map(item => {
                            const orderId = item.order_id || item.id_order || '-';
                            const productName = item.product_name || item.name || item.productName || 'Unknown';
                            const quantity = item.quantity || item.qty || 0;
                            const unitPrice = parseFloat(item.unit_price || item.price || 0);
                            const total = parseFloat(item.item_total || item.total || 0);
                            const date = item.order_date || item.created_at || item.date || null;
                            
                            return `
                                <tr>
                                    <td>${orderId}</td>
                                    <td>${productName}</td>
                                    <td>${quantity}</td>
                                    <td>${isNaN(unitPrice) ? '-' : UI.formatCurrency(unitPrice)}</td>
                                    <td>${isNaN(total) ? '-' : UI.formatCurrency(total)}</td>
                                    <td>${UI.formatDate(date)}</td>
                                </tr>
                            `;
                        }).join('')}
                    </tbody>
                </table>
            </div>
        `;
    },
    
    // Render stock report
    renderStockReport(data, container) {
        if (!data || data.length === 0) {
            container.innerHTML = '<p style="text-align: center; padding: 40px;">No stock data available</p>';
            return;
        }
        
        // Debug: log the first item to see what fields we have
        console.log('Stock report data sample:', data[0]);
        
        // Calculate summary statistics
        const totalProducts = new Set(data.map(item => item.product_name)).size;
        const totalWarehouses = new Set(data.map(item => item.warehouse_name)).size;
        const totalStock = data.reduce((sum, item) => sum + (parseFloat(item.quantity_available) || 0), 0);
        const totalReserved = data.reduce((sum, item) => sum + (parseFloat(item.quantity_reserved) || 0), 0);
        
        // Low stock items (less than 10 units available)
        const lowStockItems = data.filter(item => parseFloat(item.quantity_available) < 10);
        
        // Group by product to show total across warehouses
        const productStock = {};
        data.forEach(item => {
            if (!productStock[item.product_name]) {
                productStock[item.product_name] = {
                    available: 0,
                    reserved: 0,
                    warehouses: new Set()
                };
            }
            productStock[item.product_name].available += parseFloat(item.quantity_available) || 0;
            productStock[item.product_name].reserved += parseFloat(item.quantity_reserved) || 0;
            productStock[item.product_name].warehouses.add(item.warehouse_name);
        });
        
        const productStockArray = Object.entries(productStock)
            .map(([name, stats]) => ({ 
                name, 
                available: stats.available, 
                reserved: stats.reserved,
                warehouseCount: stats.warehouses.size
            }))
            .sort((a, b) => b.available - a.available);
        
        container.innerHTML = `
            <div class="report-grid">
                <div class="report-card">
                    <h3>Total Products</h3>
                    <div class="value">${totalProducts}</div>
                    <div class="label">Unique products in stock</div>
                </div>
                <div class="report-card">
                    <h3>Total Warehouses</h3>
                    <div class="value">${totalWarehouses}</div>
                    <div class="label">Active warehouses</div>
                </div>
                <div class="report-card">
                    <h3>Total Available Stock</h3>
                    <div class="value">${totalStock.toFixed(0)}</div>
                    <div class="label">Units available</div>
                </div>
                <div class="report-card">
                    <h3>Reserved Stock</h3>
                    <div class="value">${totalReserved.toFixed(0)}</div>
                    <div class="label">Units reserved</div>
                </div>
            </div>
            
            ${lowStockItems.length > 0 ? `
                <div class="report-table">
                    <h3 style="color: #000;">⚠️ Low Stock Alert (Less than 10 units)</h3>
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Product</th>
                                <th>Warehouse</th>
                                <th>Quantity Available</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${lowStockItems.map(item => `
                                <tr>
                                    <td>${item.product_name}</td>
                                    <td>${item.warehouse_name}</td>
                                    <td>${item.quantity_available}</td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            ` : ''}
            
            <div class="report-table">
                <h3>Product Stock Overview</h3>
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Product Name</th>
                            <th>Total Available</th>
                            <th>Total Reserved</th>
                            <th>Warehouses</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${productStockArray.map(product => `
                            <tr>
                                <td>${product.name}</td>
                                <td>${product.available.toFixed(0)}</td>
                                <td>${product.reserved.toFixed(0)}</td>
                                <td>${product.warehouseCount}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
            
            <div class="report-table">
                <h3>Stock by Warehouse</h3>
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Warehouse</th>
                            <th>Product</th>
                            <th>Available</th>
                            <th>Reserved</th>
                            <th>Location</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${data.map(item => `
                            <tr>
                                <td>${item.warehouse_name || item.name || '-'}</td>
                                <td>${item.product_name || item.product || '-'}</td>
                                <td>${item.quantity_available || item.available || 0}</td>
                                <td>${item.quantity_reserved || item.reserved || 0}</td>
                                <td>${item.location_code || item.location || '-'}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;
    }
};

// Global function to view report
function viewReport(reportType) {
    Reports.viewReport(reportType);
}
