# E-Shop Management Web Application

A minimalistic black and white web-based management interface for the e-shop backend API.

## Project Structure

```
.
├── index.html              # Main HTML file with all sections
├── css/
│   └── styles.css         # All styling (black/white minimalistic theme)
└── js/
    ├── api.js             # API communication layer
    ├── ui.js              # UI helper functions
    ├── app.js             # Main application controller
    ├── orders.js          # Orders management module
    ├── products.js        # Products management module
    ├── warehouses.js      # Warehouses & inventory management module
    └── reports.js         # Reports visualization module
```

## Features

### Connection Management
- **Initial Modal**: On startup, users must connect to the API server
- **Required fields**: Server IP, Port, and Password
- **Secure Connection**: Uses API token-based authentication
- **Disconnect Option**: Users can disconnect and reconnect at any time

### Orders Section
- **View All Orders**: Table with order ID, user ID, items preview, and status
- **Expandable Details**: Click any order to see full details including:
  - Shipping and billing addresses
  - Total amount
  - Creation date
  - Full list of ordered items
- **Order Items Management**: 
  - Add items to orders (via product dropdown)
  - Remove items from orders
  - Only editable when order is not confirmed/sent
- **Order Actions**:
  - Confirm Payment: Marks payment as confirmed
  - Send Order: Marks order as sent
  - Delete Order: Removes the order completely
- **Create New Order**: Add new orders with user ID, addresses, and currency

### Products Section
- **View All Products**: Table showing product details
- **Columns**: Product ID, Name, Price, Tax Rate
- **Actions**:
  - Edit Product: Modify name, price, or tax rate
  - Delete Product: Remove product from catalog
- **Create New Product**: Add new products with name, price, and tax rate

### Warehouses Section
- **View All Warehouses**: Table showing warehouse information
- **Columns**: Warehouse ID, Name, Location Code, Active Status, Inventory Button
- **Actions**:
  - View Inventory: Opens detailed inventory view for that warehouse
  - Edit Warehouse: Modify warehouse details
  - Delete Warehouse: Remove warehouse and all its inventory
- **Create New Warehouse**: Add new warehouses with name, location, and active status

### Inventory Management
- **Accessed via**: Warehouse "View Inventory" button
- **Displays**: All products in the selected warehouse
- **Columns**: Item name, Quantity Available, Quantity Reserved
- **Actions**:
  - Edit Inventory: Update quantities
  - Delete Inventory: Remove item from warehouse
- **Add Inventory Item**: Add new products to the warehouse with quantities

### Reports Section
- **Two Report Types**:
  1. **Sales Report**:
     - Total orders processed
     - Total revenue across all orders
     - Average order value
     - Top selling products
     - Detailed sales breakdown
  2. **Stock Report**:
     - Total unique products
     - Total warehouses
     - Total available and reserved stock
     - Low stock alerts (items with <10 units)
     - Product stock overview
     - Stock by warehouse breakdown
- **Auto-Update**: Reports show last update timestamp
- **Beautiful Visualization**: Clean cards and tables for easy reading

## Design Principles

### User-Friendly for Non-Technical Users
- Clear, descriptive button labels
- Confirmation dialogs for destructive actions
- Helpful error messages
- Consistent layout across all sections
- Intuitive navigation

### Minimalistic Black & White Theme
- **Sidebar**: Black background with white text
- **Main Content**: White background with black text
- **High Contrast**: Easy to read for long periods
- **Clean Typography**: Professional Segoe UI font
- **Consistent Borders**: 2px solid black borders throughout
- **Hover Effects**: Subtle transitions for better UX

### Accessibility
- Clear visual hierarchy
- High contrast ratios
- Large, clickable buttons
- Responsive table layouts
- Status indicators (badges for order status, active/inactive indicators)

## Usage Instructions

1. **Starting the Application**:
   - Open `index.html` in a web browser
   - Enter your API server details in the connection modal
   - Click "Connect"

2. **Navigation**:
   - Use the left sidebar to switch between sections
   - Current section is highlighted

3. **Working with Tables**:
   - Click column header buttons to create new records
   - Click row action buttons to edit or delete
   - Click expandable rows to see more details

4. **Managing Orders**:
   - Click any order row to expand and see details
   - Add/remove items when order is pending
   - Confirm payment → Send order workflow
   - Cannot modify items after confirmation

5. **Managing Inventory**:
   - Navigate to Warehouses
   - Click "View Inventory" for any warehouse
   - Add/edit/delete inventory items
   - Use "Back to Warehouses" to return

6. **Viewing Reports**:
   - Navigate to Reports section
   - Click "View Report" for Sales or Stock
   - Review visualized data
   - Use "Back to Reports" to return

## Technical Notes

### API Integration
- All API calls are handled through the `API` object in `api.js`
- Automatic error handling and user feedback
- Token-based authentication
- Supports all CRUD operations for each entity

### Error Handling
- User-friendly error messages
- Loading indicators during API calls
- Confirmation dialogs for destructive actions
- Network error recovery

### Data Flow
1. User interacts with UI
2. UI calls appropriate module (Orders, Products, Warehouses, Reports)
3. Module calls API layer
4. API communicates with Flask backend
5. Response rendered back to UI

### Browser Compatibility
- Modern browsers (Chrome, Firefox, Safari, Edge)
- No external dependencies (vanilla JavaScript)
- Responsive design for different screen sizes

## Future Enhancements (Not Implemented)
These features could be added but are not currently in the scope:
- User authentication and roles
- Advanced search and filtering
- Bulk operations
- Export reports to PDF/Excel
- Real-time updates via WebSockets
- Multi-language support

## Troubleshooting

**Connection Issues**:
- Verify API server is running
- Check IP address and port
- Ensure password is correct
- Check browser console for errors

**Data Not Loading**:
- Refresh the page and reconnect
- Check API server logs
- Verify database connection

**Actions Not Working**:
- Check browser console for JavaScript errors
- Verify API endpoints are accessible
- Ensure proper data format

## Credits

Built for e-shop management with a focus on simplicity and usability for office economists and non-technical users.
