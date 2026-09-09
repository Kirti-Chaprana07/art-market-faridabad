# ?? Art Market Faridabad ? Full-Stack Antique Decor & Botanical E-Commerce Platform

> **Live Local Hub & Online Storefront for Handcrafted Antique Heirlooms & Lush Zero-Maintenance Artificial Botanicals in Faridabad, Delhi NCR.**

---

## ?? Overview & Business Objective
**Art Market Faridabad** is a full-featured, customer-conversion-focused web platform designed for an antique and home decor showroom based in Faridabad, Haryana.

The website bridges physical showroom visits with high-conversion digital selling, allowing local customers across Faridabad and Delhi NCR to discover authentic brass statues, vintage railway clocks, hand-carved jharokhas, and lifelike faux plants.

---

## ?? Key Features Built for Customer Acquisition

### 1. ?? Instant WhatsApp Ordering & Inquiry Engine
* Every product card and product detail view features an **"Order on WhatsApp"** button.
* Automatically constructs a pre-formatted message with **Product Title, SKU, Price, and Image link** directly to the shop owner's WhatsApp for instant booking.
* Complete shopping carts can be sent as an itemized WhatsApp order with one click.

### 2. ??? Faridabad Showroom VIP Visit Booking
* Integrated booking form for personalized in-store consultations in Sector 15 / Mathura Road, Faridabad.
* Allows customers to schedule VIP showroom slots, select areas of interest (Antiques, Plants, Gifting), and receive confirmation.

### 3. ?? Live Instant Search & Room-by-Room Filtering
* Instant client-side debounced search with dropdown suggestions.
* Dynamic category and space filtering (*Living Room, Balcony & Garden, Mandir Room, Executive Office*).
* Price range slider and sorting (*Price Low-to-High, High-to-Low, Customer Rating, New Arrivals*).

### 4. ?? Full E-Commerce Cart & Multi-Payment Checkout
* Slide-out slide-over cart drawer with real-time quantity adjustment.
* Dynamic Free Delivery progress indicator for Faridabad & NCR orders.
* Checkout flow supporting **Cash on Delivery (COD)**, **UPI QR / NetBanking**, and card payment options.
* Unique order reference IDs (e.g. `#AMF-B3C91A`) with database persistence.

### 5. ??? Django Admin & Product Management
* Complete backend administrative dashboard to manage inventory, product pricing, stock levels, orders, inquiries, and customer reviews.

---

## ??? Tech Stack & Architecture

| Layer | Technology |
| :--- | :--- |
| **Backend Framework** | **Django 5.2** (Python 3.11) |
| **Database** | **PostgreSQL** (with zero-config **SQLite** fallback) |
| **Frontend UI** | **HTML5, CSS3, Tailwind CSS (Play CDN), FontAwesome 6** |
| **Client-Side State** | **Vanilla JavaScript (ES6+), LocalStorage Cart Engine, Fetch API** |
| **Typography** | Cinzel (Luxury Antique Headings), Plus Jakarta Sans, Playfair Display |
| **Database Driver** | `psycopg2-binary`, `python-dotenv`, `Pillow` |

---

## ?? Project Structure

```text
art-market-faridabad/
?
??? artmarket/                     # Django Project Settings
?   ??? settings.py                # Postgres / SQLite DB engine & static config
?   ??? urls.py                    # Root URL routing
?   ??? wsgi.py
?
??? store/                         # Main Store Application
?   ??? models.py                  # Category, Product, Order, Inquiry, Booking, Review
?   ??? views.py                   # Frontend & AJAX API Controllers
?   ??? urls.py                    # Store endpoints & REST APIs
?   ??? admin.py                   # Django Admin customizations
?   ??? context_processors.py      # Store-wide address, WhatsApp, phone context
?   ??? management/commands/
?       ??? seed_data.py           # Auto-seeder for 12+ antique & botanical products
?
??? templates/                     # Semantic HTML5 Templates
?   ??? base.html                  # Master layout with Navbar, Cart Drawer & Footer
?   ??? store/
?       ??? index.html             # Homepage with Hero, Categories & Reviews
?       ??? shop.html              # Catalog with dynamic sidebar filters & sorting
?       ??? product_detail.html    # Product specs, gallery & WhatsApp instant buy
?       ??? cart.html              # Full cart review & promo manager
?       ??? checkout.html          # Order address & payment selection
?       ??? order_success.html     # Receipt & WhatsApp order tracking
?       ??? visit.html             # Faridabad showroom booking
?       ??? about.html             # Artisan heritage & story
?       ??? contact.html           # Inquiries & Google Maps store guide
?
??? static/                        # Static Assets
?   ??? css/styles.css             # Antique brass palette & smooth animations
?   ??? js/main.js                 # Cart state, live search, WhatsApp generators
?
??? requirements.txt               # Python dependencies
??? .env.example                   # Environment configuration template
??? README.md                      # Documentation
```

---

## ? Quick Start / Local Setup Guide

### 1. Clone or Open the Repository
```bash
cd D:\art-market-faridabad
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Seed Initial Antique & Plant Products
```bash
python manage.py seed_data
```

### 5. (Optional) Create Admin Superuser
```bash
python manage.py createsuperuser
```

### 6. Start the Development Server
```bash
python manage.py runserver
```

Now open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your web browser!

---

## ?? Connecting to PostgreSQL (Optional)

To switch from SQLite to PostgreSQL:
1. Open `.env` and set:
   ```env
   DB_ENGINE=postgres
   POSTGRES_DB=artmarket_db
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=your_postgres_password
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   ```
2. Create the database in PostgreSQL: `CREATE DATABASE artmarket_db;`
3. Run `python manage.py migrate` and `python manage.py seed_data`.

---

## ?? Resume Highlights (How to describe this project)
* *"Developed a full-stack e-commerce and local customer acquisition platform for an antique decor & botanical retailer using Django, PostgreSQL/SQLite, and Tailwind CSS."*
* *"Engineered a friction-free WhatsApp lead conversion engine generating pre-populated item inquiries and itemized order payloads, boosting retail conversion rates."*
* *"Implemented dynamic AJAX search and multi-criteria product filtering (space, price, category) alongside full cart persistence using LocalStorage and Django REST endpoints."*

---

**Author**: Kirti Chaprana ([GitHub: @Kirti-Chaprana07](https://github.com/Kirti-Chaprana07))
