from flask import Flask, render_template, request, session, make_response, redirect, url_for, jsonify
from firebase_config import db
from products import PRODUCTS
import pdfkit
import io
import os
import smtplib
from email.message import EmailMessage
import json
import random
import string
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for session

# Hardcoded
OWNER_USERNAME = os.getenv("OWNER_USERNAME", "default_admin")
OWNER_PASSWORD = os.getenv("OWNER_PASSWORD", "default_password")

# Add a mapping of product to category
CATEGORY_MAP = {
    "Milk Packet": "Dairy",
    "Bread Loaf": "Bakery",
    "Eggs (Dozen)": "Dairy",
    "Rice (1kg)": "Grains",
    "Wheat Flour (1kg)": "Grains",
    "Sugar (1kg)": "Grains",
    "Salt (1kg)": "Grains",
    "Cooking Oil (1L)": "Grocery",
    "Tea (250g)": "Beverages",
    "Soap Bar": "Personal Care",
    "Biscuit Packet": "Snacks",
    "Cream Biscuit Packet": "Snacks",
    "Marie Biscuit Packet": "Snacks",
    "Shampoo (100ml)": "Personal Care",
    "Shampoo (200ml)": "Personal Care",
    "Face Cream (50g)": "Personal Care",
    "Body Lotion (100ml)": "Personal Care",
    "Toothpaste (100g)": "Personal Care",
    "Toothbrush": "Personal Care",
    "Steel Plate": "Cutlery",
    "Nonstick Pan": "Cutlery",
    "Glass Tumbler": "Cutlery",
    "Plastic Bowl": "Cutlery",
    "Ceramic Mug": "Cutlery",
    "Ball Pen": "Stationery",
    "Pencil": "Stationery",
    "Notebook (100pg)": "Stationery",
    "Eraser": "Stationery",
    "Sharpener": "Stationery",
    "Ruler (Plastic)": "Stationery",
    "Glue Stick": "Stationery",
    "Marker Pen": "Stationery",
    "Stapler": "Stationery",
    "Styrofoam Plate": "Harmful",
    "Disposable Cup": "Harmful",
    "Button Cell Battery": "Harmful",
    "AA Battery": "Harmful",
    "CFL Bulb": "Harmful",
    "Chip Packet (Multi-layered)": "Harmful",
    "Tetra Pack Juice": "Harmful",
    "Pesticide Bottle": "Harmful",
    "Toilet Cleaner": "Harmful",
    "Eraser (Rubber)": "Harmful",
    "Old Mobile Phone": "Harmful",
    "Broken Glass Piece": "Harmful"
}

USERS_FILE = 'users.json'
OTP_EXPIRY_MINUTES = 10

# Helper to load users
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

# Helper to save users
def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

# Helper to send OTP
def send_otp_email(email, otp):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_user = 'sustanabillsupermarket@gmail.com'
    smtp_password = os.getenv('SMTP_PASSWORD')
    msg = EmailMessage()
    msg['Subject'] = 'Your OTP for SustainaBILL Signup'
    msg['From'] = smtp_user
    msg['To'] = email
    msg.set_content(f'Your OTP for signup is: {otp}')
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    step = request.form.get('step') or request.args.get('step', 'email')
    if request.method == 'POST':
        users = load_users()
        if step == 'email':
            email = request.form.get('email')
            if not email or '@' not in email:
                error = 'Enter a valid email.'
            elif email in users:
                error = 'Email already registered.'
            else:
                otp = ''.join(random.choices(string.digits, k=6))
                session['signup_otp'] = otp
                session['signup_email'] = email
                session['otp_time'] = datetime.utcnow().isoformat()
                send_otp_email(email, otp)
                return render_template('signup.html', step='otp', email=email)
        elif step == 'otp':
            otp = request.form.get('otp')
            email = session.get('signup_email')
            real_otp = session.get('signup_otp')
            otp_time = session.get('otp_time')
            if not (otp and real_otp and email and otp_time):
                error = 'Session expired. Please start again.'
                return render_template('signup.html', step='email', error=error)
            if datetime.utcnow() > datetime.fromisoformat(otp_time) + timedelta(minutes=OTP_EXPIRY_MINUTES):
                error = 'OTP expired. Please request again.'
                return render_template('signup.html', step='email', error=error)
            if otp != real_otp:
                error = 'Incorrect OTP.'
                return render_template('signup.html', step='otp', email=email, error=error)
            return render_template('signup.html', step='set_password', email=email)
        elif step == 'set_password':
            email = session.get('signup_email')
            password = request.form.get('password')
            username = request.form.get('username')
            if not (email and password and username):
                error = 'All fields required.'
                return render_template('signup.html', step='set_password', email=email, error=error)
            users[email] = {'username': username, 'password': password}
            save_users(users)
            session.pop('signup_otp', None)
            session.pop('signup_email', None)
            session.pop('otp_time', None)
            return redirect(url_for('login'))
    return render_template('signup.html', step=step, error=error)

@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        users = load_users()
        # Check against registered users
        for email, user in users.items():
            if user['username'] == username and user['password'] == password:
                session["logged_in"] = True
                session["user_email"] = email
                return redirect(url_for("dashboard"))
        # Fallback to OWNER_USERNAME/PASSWORD for legacy admin
        if username == OWNER_USERNAME and password == OWNER_PASSWORD:
            session["logged_in"] = True
            session["user_email"] = None
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid username or password."
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("login"))

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    if request.method == "POST":
        items = []
        total_price = 0
        total_carbon = 0
        plastic_count = 0
        # Add counters for other harmful materials
        styrofoam_count = 0
        heavy_metal_count = 0
        multilayered_count = 0
        chemical_count = 0
        ewaste_count = 0
        rubber_count = 0
        glass_count = 0
        foil_count = 0
        paper_count = 0

        flat_products = {}
        for category, category_items in PRODUCTS.items():
            flat_products.update(category_items)

        for product, price in flat_products.items():
            qty = int(request.form.get(product, 0))
            if qty > 0:
                # Fetch environmental data from Firestore
                doc = db.collection("products").where("product_name", "==", product).get()
                if doc:
                    data = doc[0].to_dict()
                    carbon = data.get("carbon_footprint", 0) * qty
                    recyclable = data.get("recyclable", False)
                    ethical_score = data.get("ethical_score", 0)
                    material_type = data.get("material_type", "").strip().lower()
                    if "plastic" in material_type:
                        plastic_count += qty
                    if "styrofoam" in material_type:
                        styrofoam_count += qty
                    if "heavy metal" in material_type:
                        heavy_metal_count += qty
                    if "multilayered" in material_type:
                        multilayered_count += qty
                    if "chemical" in material_type:
                        chemical_count += qty
                    if "e-waste" in material_type:
                        ewaste_count += qty
                    if material_type == "rubber":
                        rubber_count += qty
                    if material_type == "glass":
                        glass_count += qty
                    if "foil" in material_type or "aluminum" in material_type:
                        foil_count += qty
                    if "paper" in material_type or "cardboard" in material_type:
                        paper_count += qty
                else:
                    carbon = 0
                    recyclable = False
                    ethical_score = 0

                item_total = price * qty
                total_price += item_total
                total_carbon += carbon
                items.append({
                    "name": product,
                    "price": price,
                    "qty": qty,
                    "item_total": item_total,
                    "carbon": carbon,
                    "recyclable": recyclable,
                    "ethical_score": ethical_score
                })

        customer_name = request.form.get("customer_name", "")
        customer_contact = request.form.get("customer_contact", "")

        # Store receipt data in session for PDF download
        session['receipt'] = {
            'items': items,
            'total_price': total_price,
            'total_carbon': total_carbon,
            'plastic_count': plastic_count,
            'styrofoam_count': styrofoam_count,
            'heavy_metal_count': heavy_metal_count,
            'multilayered_count': multilayered_count,
            'chemical_count': chemical_count,
            'ewaste_count': ewaste_count,
            'rubber_count': rubber_count,
            'glass_count': glass_count,
            'foil_count': foil_count,
            'paper_count': paper_count,
            'customer_name': customer_name,
            'customer_contact': customer_contact
        }

        return render_template(
            "receipt.html",
            items=items,
            total_price=total_price,
            total_carbon=total_carbon,
            plastic_count=plastic_count,
            styrofoam_count=styrofoam_count,
            heavy_metal_count=heavy_metal_count,
            multilayered_count=multilayered_count,
            chemical_count=chemical_count,
            ewaste_count=ewaste_count,
            rubber_count=rubber_count,
            glass_count=glass_count,
            foil_count=foil_count,
            paper_count=paper_count,
            customer_name=customer_name,
            customer_contact=customer_contact
        )

    grouped_products = get_grouped_products()
    return render_template("index.html", grouped_products=grouped_products, products=PRODUCTS)

@app.route("/download_pdf")
def download_pdf():
    receipt = session.get('receipt')
    if not receipt:
        return "No receipt data found.", 400
    rendered = render_template(
        "receipt.html",
        items=receipt['items'],
        total_price=receipt['total_price'],
        total_carbon=receipt['total_carbon'],
        plastic_count=receipt['plastic_count'],
        styrofoam_count=receipt['styrofoam_count'],
        heavy_metal_count=receipt['heavy_metal_count'],
        multilayered_count=receipt['multilayered_count'],
        chemical_count=receipt['chemical_count'],
        ewaste_count=receipt['ewaste_count'],
        rubber_count=receipt['rubber_count'],
        glass_count=receipt['glass_count'],
        foil_count=receipt.get('foil_count', 0),
        paper_count=receipt.get('paper_count', 0),
        pdf_mode=True,
        customer_name=receipt.get('customer_name', ''),
        customer_contact=receipt.get('customer_contact', '')
    )
    response = make_response(rendered)
    response.headers["Content-Type"] = "text/html"
    response.headers["Content-Disposition"] = "attachment; filename=SustainaBill-Receipt.pdf"
    return response

def send_pdf_email(to_email, content_bytes, is_pdf=True):
    smtp_server = 'smtp.gmail.com'  # Change if using another provider
    smtp_port = 587
    smtp_user = 'sustanabillsupermarket@gmail.com'  
    smtp_password = os.getenv('SMTP_PASSWORD')
  

    msg = EmailMessage()
    msg['Subject'] = 'Your SustainaBill Eco Receipt'
    msg['From'] = smtp_user
    msg['To'] = to_email
    
    if is_pdf:
        msg.set_content('Thank you for shopping! Your receipt is attached as a PDF.')
        msg.add_alternative("""
        <html>
          <body>
            <p>Thank you for shopping! Your receipt is attached.</p>
            <b>To download your receipt, open the attached PDF file.</b>
          </body>
        </html>
        """, subtype='html')
        msg.add_attachment(content_bytes, maintype='application', subtype='pdf', filename='receipt.pdf')
    else:
        # For text content
        msg.set_content(content_bytes.decode('utf-8'))
        msg.add_alternative(f"""
        <html>
          <body>
            <h2>🧾 SustainaBill – Smart Receipt</h2>
            <p>Thank you for choosing sustainable shopping!</p>
            <pre style="font-family: monospace; background: #f5f5f5; padding: 15px; border-radius: 5px;">{content_bytes.decode('utf-8')}</pre>
          </body>
        </html>
        """, subtype='html')

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False

@app.route('/send_receipt_email', methods=['POST'])
def send_receipt_email():
    receipt = session.get('receipt')
    if not receipt:
        return "No receipt data found.", 400
    customer_email = receipt.get('customer_contact', '')
    if not customer_email or '@' not in customer_email:
        return "No valid email found in customer contact.", 400
    
    # For now, just send a text email with receipt details
    msg = EmailMessage()
    msg['Subject'] = 'Your SustainaBill Eco Receipt'
    msg['From'] = 'sustanabillsupermarket@gmail.com'
    msg['To'] = customer_email
    
    # Create a simple text version of the receipt
    receipt_text = f"""
    🧾 SustainaBill – Smart Receipt
    
    Customer: {receipt.get('customer_name', '')}
    Contact: {receipt.get('customer_contact', '')}
    
    Items Purchased:
    """
    
    for item in receipt['items']:
        receipt_text += f"\n• {item['name']} x{item['qty']} - ₹{item['price']} (CO₂: {item['carbon']} kg)"
    
    receipt_text += f"""
    
    💳 Total Price: ₹{receipt['total_price']}
    🌱 Total Carbon Emission: {receipt['total_carbon']} kg CO₂e
    🧼 Plastic Items: {receipt['plastic_count']}
    
    Thank you for choosing sustainable shopping!
    """
    
    msg.set_content(receipt_text)
    if send_pdf_email(customer_email, receipt_text.encode('utf-8'), is_pdf=False):
        return "Receipt sent to email successfully!"
    else:
        return "Failed to send email. Please check your email credentials."

@app.route('/send_receipt_pdf', methods=['POST'])
def send_receipt_pdf():
    try:
        receipt = session.get('receipt')
        if not receipt:
            return "No receipt data found.", 400
        customer_email = receipt.get('customer_contact', '')
        if not customer_email or '@' not in customer_email:
            return "No valid email found in customer contact.", 400

        pdf_file = request.files.get('pdf')
        if not pdf_file:
            return "No PDF uploaded.", 400

        # Render the template with pdf_mode=True to hide buttons in the PDF
        rendered = render_template(
            "receipt.html",
            items=receipt['items'],
            total_price=receipt['total_price'],
            total_carbon=receipt['total_carbon'],
            plastic_count=receipt['plastic_count'],
            styrofoam_count=receipt['styrofoam_count'],
            heavy_metal_count=receipt['heavy_metal_count'],
            multilayered_count=receipt['multilayered_count'],
            chemical_count=receipt['chemical_count'],
            ewaste_count=receipt['ewaste_count'],
            rubber_count=receipt['rubber_count'],
            glass_count=receipt['glass_count'],
            foil_count=receipt.get('foil_count', 0),
            paper_count=receipt.get('paper_count', 0),
            pdf_mode=True,
            customer_name=receipt.get('customer_name', ''),
            customer_contact=receipt.get('customer_contact', '')
        )
        # The rest of your email sending logic remains unchanged
        msg = EmailMessage()
        msg['Subject'] = 'Your Eco-Friendly Receipt'
        msg['From'] = 'sustanabillsupermarket@gmail.com'
        msg['To'] = customer_email
        msg.set_content('Thank you for shopping! Your receipt is attached as a PDF.')
        msg.add_attachment(pdf_file.read(), maintype='application', subtype='pdf', filename='receipt.pdf')

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login('sustanabillsupermarket@gmail.com', 'bmko bywj jcnm ened')
            server.send_message(msg)

        return "Receipt PDF sent to email!"
    except Exception as e:
        return f"Server error: {str(e)}", 500

def get_grouped_products():
    grouped = {}
    for product, price in PRODUCTS.items():
        category = CATEGORY_MAP.get(product, "Other")
        grouped.setdefault(category, []).append((product, price))
    return grouped

if __name__ == "__main__":
    app.run(debug=True)