# E-Shop Management Application - Visual Guide

## Application Layout

```
┌─────────────────────────────────────────────────────────────────┐
│                     CONNECTION MODAL (Initial)                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                  Connect to API Server                     │  │
│  │                                                            │  │
│  │  Server IP:  [127.0.0.1            ]                      │  │
│  │  Port:       [5000                 ]                      │  │
│  │  Password:   [••••••••••           ]                      │  │
│  │                                                            │  │
│  │              [      Connect       ]                       │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Main Application Interface

```
┌──────────────┬────────────────────────────────────────────────────────┐
│              │                                                         │
│  E-Shop      │                    ORDERS MANAGEMENT                    │
│  Manager     │  ┌────────────────────────────────────────────────────┐│
│              │  │ Order ID │ User ID │ Items       │ Status │ Actions ││
│ ● Connected  │  ├──────────┼─────────┼────────────┼────────┼─────────┤│
│ 127.0.0.1    │  │    1     │   101   │ Widget...  │Pending │[Confirm]││
│              │  │    2     │   102   │ Gadget, .. │ Sent   │[Delete] ││
│ • Orders     │  │    3     │   103   │ Tool       │Confirm │[Send]   ││
│   Products   │  └────────────────────────────────────────────────────┘│
│   Warehouses │                                                         │
│   Reports    │  When expanded:                                        │
│              │  ┌────────────────────────────────────────────────────┐│
│              │  │ Order Details:                                      ││
│              │  │ Created: Jan 10, 2026  |  Currency: USD             ││
│              │  │ Total: $299.99         |  Address: 123 Main St      ││
│              │  │                                                      ││
│              │  │ Order Items:                                        ││
│              │  │ Product      │ Qty │ Price  │ Actions               ││
│              │  │ Widget Pro   │  2  │ $49.99 │ [Remove]             ││
│              │  │ [Select...▼] │ [1] │   -    │ [Add Item]           ││
│              │  └────────────────────────────────────────────────────┘│
│              │                                                         │
│[Disconnect]  │                                                         │
└──────────────┴────────────────────────────────────────────────────────┘
```

## Products Section

```
┌──────────────┬────────────────────────────────────────────────────────┐
│              │                   PRODUCTS MANAGEMENT                   │
│  E-Shop      │  ┌────────────────────────────────────────────────────┐│
│  Manager     │  │ Product ID │ Name      │ Price   │Tax Rate│ Actions ││
│              │  ├────────────┼───────────┼─────────┼────────┼─────────┤│
│   Orders     │  │     1      │ Widget    │ $49.99  │  21%   │[Edit]   ││
│ • Products   │  │     2      │ Gadget    │ $79.99  │  21%   │[Delete] ││
│   Warehouses │  │     3      │ Tool      │ $29.99  │  21%   │         ││
│   Reports    │  │            │           │         │        │[+ New]  ││
│              │  └────────────────────────────────────────────────────┘│
└──────────────┴────────────────────────────────────────────────────────┘
```

## Warehouses Section

```
┌──────────────┬────────────────────────────────────────────────────────┐
│              │                  WAREHOUSES MANAGEMENT                  │
│  E-Shop      │  ┌────────────────────────────────────────────────────┐│
│  Manager     │  │ID│ Name  │Location│Active │Inventory│    Actions    ││
│              │  ├──┼───────┼────────┼───────┼─────────┼───────────────┤│
│   Orders     │  │1 │Main WH│  US-NY │Active │[View]   │[Edit][Delete] ││
│   Products   │  │2 │EU Hub │  DE-BE │Active │[View]   │[Edit][Delete] ││
│ • Warehouses │  │3 │Reserve│  US-CA │Inactiv│[View]   │[Edit][Delete] ││
│   Reports    │  │  │       │        │       │         │[+ New]        ││
│              │  └────────────────────────────────────────────────────┘│
└──────────────┴────────────────────────────────────────────────────────┘
```

## Inventory View (within Warehouse)

```
┌──────────────┬────────────────────────────────────────────────────────┐
│              │  [← Back]      INVENTORY FOR: Main Warehouse            │
│  E-Shop      │  ┌────────────────────────────────────────────────────┐│
│  Manager     │  │ Item       │ Qty Available │ Qty Reserved │ Actions ││
│              │  ├────────────┼───────────────┼──────────────┼─────────┤│
│   Orders     │  │ Widget     │      50       │      10      │[Edit]   ││
│   Products   │  │ Gadget     │      30       │       5      │[Delete] ││
│ • Warehouses │  │ Tool       │       8       │       2      │         ││
│   Reports    │  │            │               │              │[+ New]  ││
│              │  └────────────────────────────────────────────────────┘│
└──────────────┴────────────────────────────────────────────────────────┘
```

## Reports Section

```
┌──────────────┬────────────────────────────────────────────────────────┐
│              │                       REPORTS                           │
│  E-Shop      │  ┌────────────────────────────────────────────────────┐│
│  Manager     │  │ Report Name    │ Last Update      │    Actions      ││
│              │  ├────────────────┼──────────────────┼─────────────────┤│
│   Orders     │  │ Sales Report   │ Jan 10, 2:30 PM  │ [View Report]   ││
│   Products   │  │ Stock Report   │ Jan 10, 2:30 PM  │ [View Report]   ││
│   Warehouses │  └────────────────────────────────────────────────────┘│
│ • Reports    │                                                         │
└──────────────┴────────────────────────────────────────────────────────┘
```

## Sales Report View

```
┌──────────────┬────────────────────────────────────────────────────────┐
│              │  [← Back]              SALES REPORT                     │
│  E-Shop      │  ┌────────────┬────────────┬────────────────────────┐  │
│  Manager     │  │Total Orders│Total Revenue│ Avg Order Value       │  │
│              │  │    156     │  $45,678    │       $293            │  │
│   Orders     │  └────────────┴────────────┴────────────────────────┘  │
│   Products   │                                                         │
│   Warehouses │  TOP SELLING PRODUCTS                                  │
│ • Reports    │  ┌────────────────────────────────────────────────────┐│
│              │  │ Product      │ Quantity Sold │ Revenue             ││
│              │  ├──────────────┼───────────────┼─────────────────────┤│
│              │  │ Widget Pro   │     250       │  $12,497            ││
│              │  │ Super Gadget │     180       │   $8,999            ││
│              │  │ Magic Tool   │     145       │   $4,345            ││
│              │  └────────────────────────────────────────────────────┘│
└──────────────┴────────────────────────────────────────────────────────┘
```

## Stock Report View

```
┌──────────────┬────────────────────────────────────────────────────────┐
│              │  [← Back]              STOCK REPORT                     │
│  E-Shop      │  ┌──────────┬──────────┬────────────┬──────────────┐  │
│  Manager     │  │Total Prod│Total WH  │Total Stock │Reserved Stock│  │
│              │  │    45    │    3     │   2,450    │     245      │  │
│   Orders     │  └──────────┴──────────┴────────────┴──────────────┘  │
│   Products   │                                                         │
│   Warehouses │  ⚠️ LOW STOCK ALERT (Less than 10 units)               │
│ • Reports    │  ┌────────────────────────────────────────────────────┐│
│              │  │ Product      │ Warehouse    │ Quantity             ││
│              │  ├──────────────┼──────────────┼──────────────────────┤│
│              │  │ Widget Mini  │ Main WH      │      8               ││
│              │  │ Tool XL      │ EU Hub       │      5               ││
│              │  └────────────────────────────────────────────────────┘│
│              │                                                         │
│              │  PRODUCT STOCK OVERVIEW                                │
│              │  [Full detailed table follows...]                      │
└──────────────┴────────────────────────────────────────────────────────┘
```

## Color Scheme

- **Sidebar**: Black (#000000) background, White (#ffffff) text
- **Main Content**: White (#ffffff) background, Black (#000000) text
- **Borders**: Black (#000000), 2px solid throughout
- **Buttons**: 
  - Primary: Black background, white text
  - Secondary: White background, black border, black text
- **Hover Effects**: Subtle gray transitions
- **Tables**: 
  - Header: Black background, white text
  - Rows: White with hover effect (light gray)

## Key UI Elements

1. **Status Badges**: 
   - Pending: White background, black border
   - Confirmed: Gray background, black text
   - Sent: Black background, white text

2. **Active Indicators**:
   - Active: Black background, white text
   - Inactive: White background, black border

3. **Connection Indicator**: 
   - Green pulsing dot in sidebar

4. **Expandable Rows**: 
   - Triangle arrow (▶) that rotates when expanded

5. **Modal Dialogs**: 
   - Centered overlay with black border
   - White background
   - Form fields with black borders

## Responsive Behavior

- Tables scroll horizontally on smaller screens
- Sidebar remains fixed at 250px width
- Main content area adjusts to remaining space
- Mobile view: Sidebar width reduces to 200px
- Touch-friendly button sizes throughout
