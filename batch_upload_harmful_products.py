from firebase_config import db

harmful_products = [
    {
        "product_name": "Styrofoam Plate",
        "price": 10,
        "carbon_footprint": 0.8,
        "recyclable": False,
        "ethical_score": 4,
        "material_type": "styrofoam"
    },
    {
        "product_name": "Disposable Cup",
        "price": 5,
        "carbon_footprint": 0.5,
        "recyclable": False,
        "ethical_score": 4,
        "material_type": "styrofoam"
    },
    {
        "product_name": "Button Cell Battery",
        "price": 15,
        "carbon_footprint": 1.5,
        "recyclable": False,
        "ethical_score": 3,
        "material_type": "heavy metal"
    },
    {
        "product_name": "AA Battery",
        "price": 20,
        "carbon_footprint": 1.8,
        "recyclable": False,
        "ethical_score": 3,
        "material_type": "heavy metal"
    },
    {
        "product_name": "CFL Bulb",
        "price": 60,
        "carbon_footprint": 2.0,
        "recyclable": False,
        "ethical_score": 4,
        "material_type": "heavy metal"
    },
    {
        "product_name": "Chip Packet (Multi-layered)",
        "price": 20,
        "carbon_footprint": 0.7,
        "recyclable": False,
        "ethical_score": 5,
        "material_type": "multilayered"
    },
    {
        "product_name": "Tetra Pack Juice",
        "price": 30,
        "carbon_footprint": 1.0,
        "recyclable": False,
        "ethical_score": 5,
        "material_type": "multilayered"
    },
    {
        "product_name": "Pesticide Bottle",
        "price": 80,
        "carbon_footprint": 2.5,
        "recyclable": False,
        "ethical_score": 2,
        "material_type": "chemical"
    },
    {
        "product_name": "Toilet Cleaner",
        "price": 50,
        "carbon_footprint": 1.2,
        "recyclable": False,
        "ethical_score": 3,
        "material_type": "chemical"
    },
    {
        "product_name": "Eraser (Rubber)",
        "price": 3,
        "carbon_footprint": 0.05,
        "recyclable": False,
        "ethical_score": 6,
        "material_type": "rubber"
    },
    {
        "product_name": "Old Mobile Phone",
        "price": 2000,
        "carbon_footprint": 10.0,
        "recyclable": False,
        "ethical_score": 2,
        "material_type": "e-waste"
    },
    {
        "product_name": "Broken Glass Piece",
        "price": 2,
        "carbon_footprint": 0.2,
        "recyclable": False,
        "ethical_score": 4,
        "material_type": "glass"
    }
]

collection_name = "products"

for product in harmful_products:
    doc_ref = db.collection(collection_name).document(product["product_name"])
    firestore_data = {k: v for k, v in product.items() if k != "price"}
    doc_ref.set(firestore_data)
    print(f'Uploaded: {product["product_name"]}')

print("Batch upload of harmful products complete!")