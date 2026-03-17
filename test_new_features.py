import asyncio
import os
import sys

# Add backend directory to path so we can import modules directly
sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

import database as db
from support_graph import process_message

# Let's seed the DB
db.init_db()

def test_product_search():
    print("--- Test 1: Product Search ---")
    response = process_message(
        sender_phone="+1234567890",
        message="Show me your smartwatches and running shoes please"
    )
    print(f"Reply:\n{response}\n")

def test_vision():
    print("--- Test 2: Vision Defect Analysis ---")
    # Using a dummy URL that points to a generic image, but asking it to act as if it is damaged
    dummy_image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Image_created_with_a_mobile_phone.png/220px-Image_created_with_a_mobile_phone.png"
    
    response = process_message(
        sender_phone="+1234567890",
        message="My order arrived with a shattered screen. I want a replacement.",
        image_url=dummy_image_url
    )
    print(f"Reply:\n{response}\n")

if __name__ == "__main__":
    test_product_search()
    test_vision()
