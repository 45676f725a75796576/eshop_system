// Orders Management Module
const Orders = {
    currentOrders: [],
    currentProducts: [], // Cache for product list used in dropdowns
    
    // Load all orders
    async loadOrders() {
        try {
            UI.showLoading();
            const orders = await API.orders.getAll();
            const products = await API.products.getAll();
            
            this.currentOrders = orders;
            this.currentProducts = products;
            this.renderOrders(orders);
        } catch (error) {
            console.error('Error loading orders:', error);
            UI.alert('Failed to load orders: ' + error.message);
        } finally {
            UI.hideLoading();
        }
    },
    
    // Render orders table
    renderOrders(orders) {
        const tbody = document.getElementById('ordersTableBody');
        tbody.innerHTML = '';
        
        if (!orders || orders.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; padding: 40px;">No orders found</td></tr>';
            return;
        }
        
        orders.forEach(order => {
            // Main order row
            const row = document.createElement('tr');
            row.id = `order-${order.id}`;
            row.className = 'expandable-row';
            row.onclick = () => this.toggleOrderDetails(order.id);
            
            row.innerHTML = `
                <td>${order.id}</td>
                <td>${order.id_user || '-'}</td>
                <td id="order-${order.id}-items">Loading...</td>
                <td>${this.getOrderStatusBadge(order)}</td>
                <td onclick="event.stopPropagation()">
                    ${this.getOrderActions(order)}
                </td>
            `;
            
            tbody.appendChild(row);
            
            // Expanded content row
            const expandedRow = document.createElement('tr');
            expandedRow.id = `order-${order.id}-expanded`;
            expandedRow.className = 'expanded-content';
            expandedRow.innerHTML = `
                <td colspan="6">
                    <div id="order-${order.id}-details">Loading details...</div>
                </td>
            `;
            
            tbody.appendChild(expandedRow);
            
            // Load order items preview
            this.loadOrderItemsPreview(order.id);
        });
    },
    
    // Get order status badge HTML
    getOrderStatusBadge(order) {
        // Determine status based on payment_status field
        let status = 'Pending';
        let statusClass = 'pending';
        
        if (order.payment_status === 'confirmed') {
            status = 'Confirmed';
            statusClass = 'confirmed';
        } else if (order.payment_status === 'sent') {
            status = 'Sent';
            statusClass = 'sent';
        }
        
        return `<span class="status-badge ${statusClass}">${status}</span>`;
    },
    
    // Get order action buttons based on status
    getOrderActions(order) {
        let actions = '';
        
        // Show confirm payment button if not confirmed or sent
        if (order.payment_status !== 'confirmed' && order.payment_status !== 'sent') {
            actions += `<button class="btn-action" onclick="Orders.confirmPayment(${order.id})">Confirm Payment</button>`;
        }
        
        // Show send order button if confirmed but not sent
        if (order.payment_status === 'confirmed' && order.payment_status !== 'sent') {
            actions += `<button class="btn-action" onclick="Orders.sendOrder(${order.id})">Send Order</button>`;
        }
        
        // Always show delete button
        actions += `<button class="btn-action btn-delete" onclick="Orders.deleteOrder(${order.id})">Delete</button>`;
        
        return actions;
    },
    
    // Load order items preview (just names)
    async loadOrderItemsPreview(orderId) {
        try {
            const items = await API.orders.getItems(orderId);
            const cell = document.getElementById(`order-${orderId}-items`);
            
            if (!items || items.length === 0) {
                cell.textContent = 'No items';
                return;
            }
            
            // Get product names
            const itemNames = [];
            for (const item of items) {
                const product = this.currentProducts.find(p => p.id === item.product_id);
                if (product) {
                    itemNames.push(product.product_name);
                }
            }
            
            // Show first few items with ellipsis if more
            if (itemNames.length <= 3) {
                cell.textContent = itemNames.join(', ');
            } else {
                cell.textContent = itemNames.slice(0, 3).join(', ') + '...';
            }
        } catch (error) {
            console.error('Error loading order items preview:', error);
            const cell = document.getElementById(`order-${orderId}-items`);
            cell.textContent = 'Error loading';
        }
    },
    
    // Toggle order details expansion
    async toggleOrderDetails(orderId) {
        const row = document.getElementById(`order-${orderId}`);
        const expandedRow = document.getElementById(`order-${orderId}-expanded`);
        const arrow = document.getElementById(`arrow-${orderId}`);
        
        row.classList.toggle('expanded');
        expandedRow.classList.toggle('show');
        
        // Rotate arrow
        if (arrow) {
            arrow.style.transform = expandedRow.classList.contains('show') ? 'rotate(90deg)' : 'rotate(0deg)';
        }
        
        // Load full details if expanding for the first time
        if (expandedRow.classList.contains('show')) {
            await this.loadOrderDetails(orderId);
        }
    },
    
    // Load full order details
    async loadOrderDetails(orderId) {
        try {
            const order = await API.orders.getById(orderId);
            const items = await API.orders.getItems(orderId);
            
            const detailsContainer = document.getElementById(`order-${orderId}-details`);
            
            // Format addresses
            const shippingAddr = typeof order.shipping_address === 'string' 
                ? order.shipping_address 
                : JSON.stringify(order.shipping_address);
            const billingAddr = typeof order.billing_address === 'string' 
                ? order.billing_address 
                : JSON.stringify(order.billing_address);
            
            // Calculate actual total from items
            let calculatedTotal = 0;
            items.forEach(item => {
                const product = this.currentProducts.find(p => p.id === item.product_id);
                if (product) {
                    const itemTotal = product.unit_price * item.quantity * (1 + product.tax_rate);
                    calculatedTotal += itemTotal;
                }
            });
            
            const isEditable = order.payment_status !== 'confirmed' && order.payment_status !== 'sent';
            
            detailsContainer.innerHTML = `
                <div class="order-details">
                    <div class="detail-item">
                        <strong>Created At</strong>
                        <div>${UI.formatDate(order.created_at)}</div>
                    </div>
                    <div class="detail-item">
                        <strong>Currency</strong>
                        <div>${order.currency || 'USD'}</div>
                    </div>
                    <div class="detail-item">
                        <strong>Total Amount (Saved)</strong>
                        <div>${UI.formatCurrency(order.total_amount || 0, order.currency)}</div>
                    </div>
                    <div class="detail-item">
                        <strong>Calculated Total</strong>
                        <div>${UI.formatCurrency(calculatedTotal, order.currency)}</div>
                        ${isEditable ? `<button class="btn-action" style="margin-top: 10px;" onclick="Orders.updateOrderTotal(${orderId}).then(() => Orders.loadOrderDetails(${orderId})).then(() => Orders.loadOrders())">Recalculate</button>` : ''}
                    </div>
                    <div class="detail-item">
                        <strong>Shipping Address</strong>
                        <div>${shippingAddr}</div>
                    </div>
                    <div class="detail-item">
                        <strong>Billing Address</strong>
                        <div>${billingAddr}</div>
                    </div>
                </div>
                <h4 style="margin-top: 20px; margin-bottom: 10px;">Order Items</h4>
                <table class="order-items-table">
                    <thead>
                        <tr>
                            <th>Product</th>
                            <th>Quantity</th>
                            <th>Unit Price</th>
                            <th>Tax Rate</th>
                            <th>Item Total</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody id="order-${orderId}-items-tbody">
                        ${this.renderOrderItems(orderId, items)}
                    </tbody>
                </table>
            `;
        } catch (error) {
            console.error('Error loading order details:', error);
            const detailsContainer = document.getElementById(`order-${orderId}-details`);
            detailsContainer.innerHTML = '<p>Error loading order details</p>';
        }
    },
    
    // Render order items with editable fields (if order not confirmed/sent)
    renderOrderItems(orderId, items) {
        const order = this.currentOrders.find(o => o.id === orderId);
        const isEditable = order && order.payment_status !== 'confirmed' && order.payment_status !== 'sent';
        
        let html = '';
        
        items.forEach(item => {
            const product = this.currentProducts.find(p => p.id === item.product_id);
            const productName = product ? product.product_name : 'Unknown';
            const unitPrice = product ? product.unit_price : 0;
            const taxRate = product ? product.tax_rate : 0;
            const itemTotal = unitPrice * item.quantity * (1 + taxRate);
            
            html += `
                <tr>
                    <td>${productName}</td>
                    <td>${item.quantity}</td>
                    <td>${UI.formatCurrency(unitPrice)}</td>
                    <td>${(taxRate * 100).toFixed(2)}%</td>
                    <td>${UI.formatCurrency(itemTotal)}</td>
                    <td>
                        ${isEditable ? `<button class="btn-action btn-delete" onclick="Orders.removeOrderItem(${orderId}, '${productName}')">Remove</button>` : '-'}
                    </td>
                </tr>
            `;
        });
        
        // Add new item row if editable
        if (isEditable) {
            html += `
                <tr>
                    <td>
                        <select id="new-item-product-${orderId}">
                            <option value="">Select product...</option>
                            ${this.currentProducts.map(p => `<option value="${p.id}">${p.product_name}</option>`).join('')}
                        </select>
                    </td>
                    <td>
                        <input type="number" id="new-item-quantity-${orderId}" min="1" value="1" />
                    </td>
                    <td colspan="3">-</td>
                    <td>
                        <button class="btn-action btn-create" onclick="Orders.addOrderItem(${orderId})">Add Item</button>
                    </td>
                </tr>
            `;
        }
        
        return html;
    },
    
    // Calculate and update order total
    async updateOrderTotal(orderId) {
        try {
            const items = await API.orders.getItems(orderId);
            let total = 0;
            
            for (const item of items) {
                const product = this.currentProducts.find(p => p.id === item.product_id);
                if (product) {
                    const itemTotal = product.unit_price * item.quantity * (1 + product.tax_rate);
                    total += itemTotal;
                }
            }
            
            // Update the order with the calculated total
            await API.orders.update(orderId, { total_amount: total });
        } catch (error) {
            console.error('Error updating order total:', error);
        }
    },
    
    // Add item to order
    async addOrderItem(orderId) {
        const productSelect = document.getElementById(`new-item-product-${orderId}`);
        const quantityInput = document.getElementById(`new-item-quantity-${orderId}`);
        
        const productId = parseInt(productSelect.value);
        const quantity = parseInt(quantityInput.value);
        
        if (!productId || !quantity || quantity < 1) {
            UI.alert('Please select a product and enter a valid quantity');
            return;
        }
        
        try {
            UI.showLoading();
            await API.orders.addItem(orderId, productId, quantity);
            await this.updateOrderTotal(orderId);  // Recalculate total
            await this.loadOrderDetails(orderId);
            await this.loadOrderItemsPreview(orderId);
            await this.loadOrders();  // Refresh to show updated total
        } catch (error) {
            console.error('Error adding order item:', error);
            UI.alert('Failed to add item: ' + error.message);
        } finally {
            UI.hideLoading();
        }
    },
    
    // Remove item from order
    async removeOrderItem(orderId, productName) {
        if (!UI.confirm(`Remove ${productName} from this order?`)) {
            return;
        }
        
        try {
            UI.showLoading();
            await API.orders.removeItem(orderId, productName);
            await this.updateOrderTotal(orderId);  // Recalculate total
            await this.loadOrderDetails(orderId);
            await this.loadOrderItemsPreview(orderId);
            await this.loadOrders();  // Refresh to show updated total
        } catch (error) {
            console.error('Error removing order item:', error);
            UI.alert('Failed to remove item: ' + error.message);
        } finally {
            UI.hideLoading();
        }
    },
    
    // Confirm payment for order
    async confirmPayment(orderId) {
        if (!UI.confirm('Confirm payment for this order?')) {
            return;
        }
        
        try {
            UI.showLoading();
            await API.orders.update(orderId, { payment_status: 'confirmed' });
            await this.loadOrders();
        } catch (error) {
            console.error('Error confirming payment:', error);
            UI.alert('Failed to confirm payment: ' + error.message);
        } finally {
            UI.hideLoading();
        }
    },
    
    // Send order
    async sendOrder(orderId) {
        if (!UI.confirm('Mark this order as sent?')) {
            return;
        }
        
        try {
            UI.showLoading();
            await API.orders.update(orderId, { payment_status: 'sent' });
            await this.loadOrders();
        } catch (error) {
            console.error('Error sending order:', error);
            UI.alert('Failed to send order: ' + error.message);
        } finally {
            UI.hideLoading();
        }
    },
    
    // Delete order
    async deleteOrder(orderId) {
        if (!UI.confirm('Are you sure you want to delete this order? This action cannot be undone.')) {
            return;
        }
        
        try {
            UI.showLoading();
            await API.orders.delete(orderId);
            await this.loadOrders();
        } catch (error) {
            console.error('Error deleting order:', error);
            UI.alert('Failed to delete order: ' + error.message);
        } finally {
            UI.hideLoading();
        }
    }
};

// Global function to create new order
function createOrder() {
    openRecordModal('Create New Order', [
        { name: 'user_id', label: 'User ID', type: 'number', required: true },
        { name: 'shipping_address', label: 'Shipping Address', type: 'textarea', required: true },
        { name: 'billing_address', label: 'Billing Address', type: 'textarea', required: true },
        { name: 'currency', label: 'Currency', type: 'text', value: 'USD', required: true }
    ], async (data) => {
        // Convert addresses to JSON if they're plain text
        // For simplicity, treating them as strings for now
        await API.orders.create({
            user_id: data.user_id,
            shipping_address: data.shipping_address,
            billing_address: data.billing_address,
            currency: data.currency
        });
        await Orders.loadOrders();
    });
}
