# mock_ecommerce.py

# A dictionary acting as a mock database for D2C E-commerce Orders
MOCK_ORDERS = {
    "+919876543210": {
        "order_id": "ORD-12345",
        "status": "Out for Delivery",
        "items": ["Wireless Earbuds", "Phone Case"],
        "estimated_delivery": "Today by 8 PM",
        "refund_status": None
    },
    "+919988776655": {
        "order_id": "ORD-67890",
        "status": "Delivered",
        "items": ["Smart Watch"],
        "estimated_delivery": "Delivered on 5th Oct",
        "refund_status": "Processing"  # Indicates a refund was requested
    },
    "+918877665544": {
        "order_id": "ORD-11223",
        "status": "Processing",
        "items": ["Running Shoes"],
        "estimated_delivery": "10th Oct",
        "refund_status": None
    },
    "+917766554433": {
        "order_id": "ORD-44556",
        "status": "Cancelled",
        "items": ["Yoga Mat"],
        "estimated_delivery": "N/A",
        "refund_status": "Refunded"
    }
}

def get_order_by_phone(phone_number: str):
    """Retrieve an order using the customer's phone number."""
    # Normalize phone number to include +91 if purely 10 digits
    if len(phone_number) == 10 and phone_number.isdigit():
        phone_number = f"+91{phone_number}"
        
    return MOCK_ORDERS.get(phone_number)

def get_order_by_id(order_id: str):
    """Retrieve an order using the order ID."""
    for phone, order_data in MOCK_ORDERS.items():
        if order_data.get("order_id") == order_id:
            order_data_with_phone = order_data.copy()
            order_data_with_phone["phone"] = phone
            return order_data_with_phone
    return None

def process_refund(order_id: str):
    """Mock process a refund."""
    order = get_order_by_id(order_id)
    if order:
        phone = order["phone"]
        if MOCK_ORDERS[phone]["status"] in ["Delivered", "Processing"]:
             if not MOCK_ORDERS[phone]["refund_status"]:
                 MOCK_ORDERS[phone]["refund_status"] = "Initiated"
                 return {"success": True, "message": f"Refund initiated for order {order_id}"}
             return {"success": False, "message": f"Refund already in status: {MOCK_ORDERS[phone]['refund_status']}"}
        return {"success": False, "message": f"Cannot refund order in status: {MOCK_ORDERS[phone]['status']}"}
    return {"success": False, "message": "Order not found."}
