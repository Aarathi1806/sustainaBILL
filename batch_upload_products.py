from firebase_config import db

products = [
    {"product_name": "Milk Packet", "price": 50, "carbon_footprint": 1.2, "recyclable": True, "ethical_score": 7, "material_type": "plastic"},
    {"product_name": "Bread Loaf", "price": 40, "carbon_footprint": 0.8, "recyclable": True, "ethical_score": 8, "material_type": "paper"},
    {"product_name": "Eggs (Dozen)", "price": 70, "carbon_footprint": 2.0, "recyclable": False, "ethical_score": 6, "material_type": "biodegradable"},
    {"product_name": "Rice (1kg)", "price": 60, "carbon_footprint": 1.5, "recyclable": False, "ethical_score": 7, "material_type": "biodegradable"},
    {"product_name": "Wheat Flour (1kg)", "price": 55, "carbon_footprint": 1.3, "recyclable": False, "ethical_score": 7, "material_type": "biodegradable"},
    {"product_name": "Sugar (1kg)", "price": 45, "carbon_footprint": 1.1, "recyclable": False, "ethical_score": 7, "material_type": "biodegradable"},
    {"product_name": "Salt (1kg)", "price": 20, "carbon_footprint": 0.5, "recyclable": False, "ethical_score": 8, "material_type": "biodegradable"},
    {"product_name": "Cooking Oil (1L)", "price": 120, "carbon_footprint": 2.5, "recyclable": True, "ethical_score": 6, "material_type": "plastic"},
    {"product_name": "Tea (250g)", "price": 90, "carbon_footprint": 0.9, "recyclable": True, "ethical_score": 8, "material_type": "paper"},
    {"product_name": "Soap Bar", "price": 30, "carbon_footprint": 0.7, "recyclable": True, "ethical_score": 8, "material_type": "paper"},
    {"product_name": "Biscuit Packet", "price": 25, "carbon_footprint": 0.6, "recyclable": True, "ethical_score": 7, "material_type": "plastic"},
    {"product_name": "Cream Biscuit Packet", "price": 30, "carbon_footprint": 0.7, "recyclable": True, "ethical_score": 7, "material_type": "plastic"},
    {"product_name": "Marie Biscuit Packet", "price": 20, "carbon_footprint": 0.5, "recyclable": True, "ethical_score": 8, "material_type": "plastic"},
    {"product_name": "Shampoo (100ml)", "price": 60, "carbon_footprint": 1.0, "recyclable": True, "ethical_score": 6, "material_type": "plastic"},
    {"product_name": "Shampoo (200ml)", "price": 110, "carbon_footprint": 1.8, "recyclable": True, "ethical_score": 6, "material_type": "plastic"},
    {"product_name": "Face Cream (50g)", "price": 80, "carbon_footprint": 0.9, "recyclable": True, "ethical_score": 7, "material_type": "plastic"},
    {"product_name": "Body Lotion (100ml)", "price": 90, "carbon_footprint": 1.2, "recyclable": True, "ethical_score": 7, "material_type": "plastic"},
    {"product_name": "Toothpaste (100g)", "price": 45, "carbon_footprint": 0.8, "recyclable": True, "ethical_score": 7, "material_type": "plastic"},
    {"product_name": "Toothbrush", "price": 20, "carbon_footprint": 0.3, "recyclable": True, "ethical_score": 7, "material_type": "plastic"},
    {"product_name": "Steel Plate", "price": 120, "carbon_footprint": 2.0, "recyclable": True, "ethical_score": 9, "material_type": "metal"},
    {"product_name": "Nonstick Pan", "price": 350, "carbon_footprint": 3.0, "recyclable": True, "ethical_score": 8, "material_type": "metal"},
    {"product_name": "Glass Tumbler", "price": 60, "carbon_footprint": 1.5, "recyclable": True, "ethical_score": 8, "material_type": "glass"},
    {"product_name": "Plastic Bowl", "price": 30, "carbon_footprint": 0.7, "recyclable": True, "ethical_score": 6, "material_type": "plastic"},
    {"product_name": "Ceramic Mug", "price": 80, "carbon_footprint": 1.2, "recyclable": True, "ethical_score": 8, "material_type": "ceramic"},
    {"product_name": "Ball Pen", "price": 10, "carbon_footprint": 0.2, "recyclable": True, "ethical_score": 7, "material_type": "plastic"},
    {"product_name": "Pencil", "price": 5, "carbon_footprint": 0.1, "recyclable": True, "ethical_score": 8, "material_type": "wood"},
    {"product_name": "Notebook (100pg)", "price": 40, "carbon_footprint": 0.5, "recyclable": True, "ethical_score": 8, "material_type": "paper"},
    {"product_name": "Eraser", "price": 3, "carbon_footprint": 0.05, "recyclable": False, "ethical_score": 7, "material_type": "rubber"},
    {"product_name": "Sharpener", "price": 5, "carbon_footprint": 0.1, "recyclable": True, "ethical_score": 8, "material_type": "metal"},
    {"product_name": "Ruler (Plastic)", "price": 8, "carbon_footprint": 0.1, "recyclable": True, "ethical_score": 7, "material_type": "plastic"},
    {"product_name": "Glue Stick", "price": 15, "carbon_footprint": 0.2, "recyclable": True, "ethical_score": 7, "material_type": "plastic"},
    {"product_name": "Marker Pen", "price": 20, "carbon_footprint": 0.3, "recyclable": True, "ethical_score": 7, "material_type": "plastic"},
    {"product_name": "Stapler", "price": 30, "carbon_footprint": 0.4, "recyclable": True, "ethical_score": 8, "material_type": "metal"},
]

collection_name = "products"

for product in products:
    doc_ref = db.collection(collection_name).document(product["product_name"])
    firestore_data = {k: v for k, v in product.items() if k != "price"}
    doc_ref.set(firestore_data)
    print(f'Uploaded: {product["product_name"]}')

print("Batch upload complete!")