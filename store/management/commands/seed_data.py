from django.core.management.base import BaseCommand
from store.models import Category, Product, Review

class Command(BaseCommand):
    help = 'Seeds initial sample antique decor and artificial plant products'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting database seeding for Art Market Faridabad...")

        # 1. Categories
        categories_data = [
            {
                "name": "Antique Brass & Bronze",
                "description": "Authentic handcrafted solid brass statues, temple lamps, urulis, and heritage artifacts.",
                "image_url": "https://images.unsplash.com/photo-1579783902614-a3fb3927b675?auto=format&fit=crop&w=800&q=80",
                "icon": "fa-award"
            },
            {
                "name": "Artificial Plants & Trees",
                "description": "Zero-maintenance botanical faux greenery, lifelike fiddle leaf figs, bonsai, and hanging foliage.",
                "image_url": "https://images.unsplash.com/photo-1485955900006-10f4d324d411?auto=format&fit=crop&w=800&q=80",
                "icon": "fa-seedling"
            },
            {
                "name": "Vintage Clocks & Gramophones",
                "description": "Grand double-sided railway clocks, rustic pocket-watch wall clocks, and brass gramophones.",
                "image_url": "https://images.unsplash.com/photo-1563861826100-9cb868fdbe1c?auto=format&fit=crop&w=800&q=80",
                "icon": "fa-clock"
            },
            {
                "name": "Ceramic & Metal Planters",
                "description": "Artisan glazed ceramic pots, minimalist gold iron stands, and handcrafted terracotta planters.",
                "image_url": "https://images.unsplash.com/photo-1512428559087-560fa5ceab42?auto=format&fit=crop&w=800&q=80",
                "icon": "fa-wine-bottle"
            },
            {
                "name": "Hand-Carved Heritage Woodcraft",
                "description": "Intricate teakwood jharokha mirrors, distress finish temple shelves, and vintage wall panels.",
                "image_url": "https://images.unsplash.com/photo-1538688525198-9b88f6f53126?auto=format&fit=crop&w=800&q=80",
                "icon": "fa-tree"
            }
        ]

        cat_objs = {}
        for c in categories_data:
            cat, created = Category.objects.update_or_create(
                name=c["name"],
                defaults={
                    "description": c["description"],
                    "image_url": c["image_url"],
                    "icon": c["icon"]
                }
            )
            cat_objs[c["name"]] = cat

        # 2. Products
        products_data = [
            # Antiques
            {
                "name": "Heritage Royal Brass Uruli with Bell & Stand",
                "category": cat_objs["Antique Brass & Bronze"],
                "sku": "AMF-BRS-001",
                "original_price": 5499.00,
                "price": 3899.00,
                "short_description": "Traditional heavy brass uruli ideal for floating flowers and aroma candles at entrance foyers.",
                "description": "Exquisitely hand-cast by master artisans, this royal brass uruli is treated with a vintage patina finish. Perfect for festive celebrations, luxury living room centerpieces, and temple spaces.",
                "material": "100% Solid Brass with Antique Gold Patina",
                "dimensions": "14in Diameter x 7in Height",
                "weight": "4.2 kg",
                "room_type": "living_room",
                "stock": 15,
                "image_url": "https://images.unsplash.com/photo-1606744888344-498238f01777?auto=format&fit=crop&w=800&q=80",
                "is_featured": True,
                "is_bestseller": True,
                "is_new_arrival": False,
                "rating": 4.9,
                "reviews_count": 28
            },
            {
                "name": "Vintage Victorian Double-Sided Railway Station Clock",
                "category": cat_objs["Vintage Clocks & Gramophones"],
                "sku": "AMF-CLK-002",
                "original_price": 4200.00,
                "price": 2999.00,
                "short_description": "Classic wrought iron antique finish wall clock with 360-degree dual dial.",
                "description": "Add timeless colonial elegance to your corridor or living room. Features silent sweep Japanese quartz movement inside a weather-resistant antique bronze iron casing.",
                "material": "Wrought Iron & Distressed Brass Bezel",
                "dimensions": "16in Diameter x 18in Height with Bracket",
                "weight": "2.8 kg",
                "room_type": "living_room",
                "stock": 8,
                "image_url": "https://images.unsplash.com/photo-1563861826100-9cb868fdbe1c?auto=format&fit=crop&w=800&q=80",
                "is_featured": True,
                "is_bestseller": True,
                "is_new_arrival": False,
                "rating": 4.8,
                "reviews_count": 34
            },
            {
                "name": "Hand-Carved Rajasthani Jharokha Mirror Frame",
                "category": cat_objs["Hand-Carved Heritage Woodcraft"],
                "sku": "AMF-WOD-003",
                "original_price": 6999.00,
                "price": 4850.00,
                "short_description": "Rustic distressed blue & antique gold arched window frame with premium mirror.",
                "description": "Carved from seasoned teakwood featuring traditional floral jaali work and brass latch accents. Creates a stunning focal point in entryways, living rooms, and boutique cafes.",
                "material": "Seasoned Teakwood with Brass Accents",
                "dimensions": "24in Height x 16in Width x 3in Depth",
                "weight": "5.1 kg",
                "room_type": "living_room",
                "stock": 6,
                "image_url": "https://images.unsplash.com/photo-1538688525198-9b88f6f53126?auto=format&fit=crop&w=800&q=80",
                "is_featured": True,
                "is_bestseller": False,
                "is_new_arrival": True,
                "rating": 5.0,
                "reviews_count": 19
            },
            {
                "name": "Antique Brass Dancing Nataraja Idol (Museum Grade)",
                "category": cat_objs["Antique Brass & Bronze"],
                "sku": "AMF-BRS-004",
                "original_price": 8999.00,
                "price": 6499.00,
                "short_description": "Intricately detailed sacred Shiva Nataraja statue in antique finish.",
                "description": "Crafted following ancient lost-wax casting technique. Features detailed ring of fire (prabhavali) and serene expression. A masterwork for mandirs and collector showcases.",
                "material": "Heavyweight Solid Brass",
                "dimensions": "15in Height x 12in Width",
                "weight": "3.9 kg",
                "room_type": "mandir",
                "stock": 5,
                "image_url": "https://images.unsplash.com/photo-1579783902614-a3fb3927b675?auto=format&fit=crop&w=800&q=80",
                "is_featured": True,
                "is_bestseller": True,
                "is_new_arrival": False,
                "rating": 5.0,
                "reviews_count": 42
            },
            {
                "name": "Nautical Antique Brass Telescopic Spyglass on Wood Tripod",
                "category": cat_objs["Vintage Clocks & Gramophones"],
                "sku": "AMF-NAU-005",
                "original_price": 5999.00,
                "price": 3999.00,
                "short_description": "Vintage mariner brass telescope mounted on adjustable mahogany wood tripod.",
                "description": "Functional optics with focus adjustment. Gives an intellectual, aristocratic atmosphere to executive offices, libraries, and living spaces.",
                "material": "Pure Brass & Polished Rosewood",
                "dimensions": "Adjustable Height 28in - 45in",
                "weight": "2.4 kg",
                "room_type": "office",
                "stock": 10,
                "image_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=800&q=80",
                "is_featured": False,
                "is_bestseller": False,
                "is_new_arrival": True,
                "rating": 4.7,
                "reviews_count": 14
            },

            # Artificial Plants & Planters
            {
                "name": "5.5ft Real-Touch Luxury Fiddle Leaf Fig Tree in Pot",
                "category": cat_objs["Artificial Plants & Trees"],
                "sku": "AMF-PLN-006",
                "original_price": 4999.00,
                "price": 3499.00,
                "short_description": "Architectural faux fiddle leaf fig with 38 broad textured leaves and natural wood trunk.",
                "description": "Crafted with botanical precision, this fiddle leaf fig tree looks 100% natural without wilting, dropping leaves, or watering requirements. UV-resistant and long-lasting.",
                "material": "Real-Touch Silk Polymers & Natural Wood Trunk",
                "dimensions": "66in Height (5.5 Feet)",
                "weight": "4.5 kg",
                "room_type": "living_room",
                "stock": 20,
                "image_url": "https://images.unsplash.com/photo-1545241047-6083a3684587?auto=format&fit=crop&w=800&q=80",
                "is_featured": True,
                "is_bestseller": True,
                "is_new_arrival": False,
                "rating": 4.9,
                "reviews_count": 56
            },
            {
                "name": "Japanese Zen Juniper Bonsai Tree in Ceramic Dish",
                "category": cat_objs["Artificial Plants & Trees"],
                "sku": "AMF-PLN-007",
                "original_price": 2899.00,
                "price": 1899.00,
                "short_description": "Aesthetic twisted trunk miniature bonsai with lifelike moss bed and ceramic planter.",
                "description": "Bring serenity and zen harmony to your work desk, coffee table, or console. Hand-shaped branches that maintain vibrant evergreen foliage forever.",
                "material": "High-Grade Polymer, Preserved Moss & Glazed Ceramic",
                "dimensions": "14in Height x 16in Width",
                "weight": "1.8 kg",
                "room_type": "office",
                "stock": 25,
                "image_url": "https://images.unsplash.com/photo-1512428559087-560fa5ceab42?auto=format&fit=crop&w=800&q=80",
                "is_featured": True,
                "is_bestseller": True,
                "is_new_arrival": False,
                "rating": 4.8,
                "reviews_count": 39
            },
            {
                "name": "4ft Tropical Areca Palm Tree in Modern White Pot",
                "category": cat_objs["Artificial Plants & Trees"],
                "sku": "AMF-PLN-008",
                "original_price": 3899.00,
                "price": 2699.00,
                "short_description": "Lush cascading tropical palm fronds that instantly liven up empty corners.",
                "description": "Creates an oasis vibe in urban apartments and covered balconies. Requires zero sunlight and zero pest management. Easily wiped clean with a damp cloth.",
                "material": "Silk-Touch Polyethylene & Weighted Base",
                "dimensions": "48in Height (4 Feet)",
                "weight": "3.2 kg",
                "room_type": "balcony",
                "stock": 14,
                "image_url": "https://images.unsplash.com/photo-1485955900006-10f4d324d411?auto=format&fit=crop&w=800&q=80",
                "is_featured": True,
                "is_bestseller": False,
                "is_new_arrival": True,
                "rating": 4.9,
                "reviews_count": 21
            },
            {
                "name": "Set of 2 Hammered Gold Brass Planters with Iron Stands",
                "category": cat_objs["Ceramic & Metal Planters"],
                "sku": "AMF-POT-009",
                "original_price": 3499.00,
                "price": 2299.00,
                "short_description": "Modern mid-century metal floor planters with elevated matte black tripod stands.",
                "description": "Elevate your indoor botanical setup with metallic warm tones. Rust-free electroplated brass bowl with sturdy powder-coated iron stand.",
                "material": "Electroplated Iron & Brass Finish",
                "dimensions": "Large: 22in H, Medium: 18in H",
                "weight": "2.9 kg (Set)",
                "room_type": "living_room",
                "stock": 18,
                "image_url": "https://images.unsplash.com/photo-1509423350716-97f9360b4e09?auto=format&fit=crop&w=800&q=80",
                "is_featured": True,
                "is_bestseller": True,
                "is_new_arrival": False,
                "rating": 4.9,
                "reviews_count": 48
            },
            {
                "name": "Cascading Hanging String of Pearls & Eucalyptus Vines (Pack of 3)",
                "category": cat_objs["Artificial Plants & Trees"],
                "sku": "AMF-PLN-010",
                "original_price": 1899.00,
                "price": 1199.00,
                "short_description": "Lifelike trailing succulent vines perfect for wall shelves, macrame hangers, and balconies.",
                "description": "Ultra-realistic trailing foliage with subtle gradients and natural stem texture. Ideal for bookshelf accents and balcony partition walls.",
                "material": "Non-Toxic Flexible UV-Stabilized Polymer",
                "dimensions": "32in Length Each",
                "weight": "0.6 kg",
                "room_type": "balcony",
                "stock": 30,
                "image_url": "https://images.unsplash.com/photo-1517196084881-6494535bd93f?auto=format&fit=crop&w=800&q=80",
                "is_featured": False,
                "is_bestseller": False,
                "is_new_arrival": True,
                "rating": 4.8,
                "reviews_count": 17
            },
            {
                "name": "Artisan Moroccan Hand-Painted Ceramic Planter Pot",
                "category": cat_objs["Ceramic & Metal Planters"],
                "sku": "AMF-POT-011",
                "original_price": 1499.00,
                "price": 999.00,
                "short_description": "Vibrant cobalt blue & terracotta glazed ceramic pot with drainage hole.",
                "description": "Individually hand-glazed with Moroccan bohemian geometric motifs. Kiln fired for high durability and rich gloss.",
                "material": "High-Fired Glazed Ceramic",
                "dimensions": "8in Diameter x 7.5in Height",
                "weight": "1.5 kg",
                "room_type": "balcony",
                "stock": 22,
                "image_url": "https://images.unsplash.com/photo-1520412099551-62b6bafeb5bb?auto=format&fit=crop&w=800&q=80",
                "is_featured": False,
                "is_bestseller": False,
                "is_new_arrival": False,
                "rating": 4.7,
                "reviews_count": 13
            },
            {
                "name": "Antique Brass 7-Tier Hanging Peacock Diya (Temple Lamp)",
                "category": cat_objs["Antique Brass & Bronze"],
                "sku": "AMF-BRS-012",
                "original_price": 4499.00,
                "price": 3199.00,
                "short_description": "Traditional South Indian style hanging oil lamp with ornate peacock finial.",
                "description": "Cast in pure yellow brass with a long link chain. Infuses mandir rooms and entrances with spiritual serenity and classic royalty.",
                "material": "Pure Brass with Brass Chain",
                "dimensions": "10in Diya Diameter + 24in Chain",
                "weight": "3.1 kg",
                "room_type": "mandir",
                "stock": 11,
                "image_url": "https://images.unsplash.com/photo-1606744888344-498238f01777?auto=format&fit=crop&w=800&q=80",
                "is_featured": True,
                "is_bestseller": False,
                "is_new_arrival": True,
                "rating": 5.0,
                "reviews_count": 27
            }
        ]

        for p in products_data:
            Product.objects.update_or_create(
                sku=p["sku"],
                defaults=p
            )

        # 3. Reviews
        reviews_data = [
            {
                "name": "Rohit Sharma",
                "city": "Sector 14, Faridabad",
                "rating": 5,
                "title": "Stunning quality antiques right here in Faridabad!",
                "comment": "Visited their showroom in Faridabad and bought the Victorian Railway Clock and 5ft Fiddle Leaf Fig. The brass weight and details are exceptional. Saved me a trip to Delhi!",
                "product_name": "Victorian Railway Station Clock & Fiddle Fig",
                "is_verified": True
            },
            {
                "name": "Pooja Verma",
                "city": "Charmwood Village, Faridabad",
                "rating": 5,
                "title": "The artificial plants look 100% natural",
                "comment": "Ordered via WhatsApp and got it delivered within 2 hours in Faridabad. Guests keep asking if the Bonsai is real! Highly recommended for home decor lovers.",
                "product_name": "Japanese Zen Juniper Bonsai",
                "is_verified": True
            },
            {
                "name": "Amit Bhatia",
                "city": "Greater Faridabad (Neharpar)",
                "rating": 5,
                "title": "Best store for Diwali & Housewarming Gifting",
                "comment": "Bought 10 brass urulis for corporate Diwali gifts. The packaging was immaculate and customer service over WhatsApp was super helpful.",
                "product_name": "Heritage Royal Brass Uruli",
                "is_verified": True
            },
            {
                "name": "Dr. Neha Malik",
                "city": "Sainik Colony, Faridabad",
                "rating": 5,
                "title": "Transformed our clinic lobby",
                "comment": "The gold metal planters and Areca palm gave our reception a luxurious 5-star hotel feel. Zero maintenance and stunning aesthetics.",
                "product_name": "Hammered Gold Brass Planters",
                "is_verified": True
            }
        ]

        for r in reviews_data:
            Review.objects.get_or_create(
                name=r["name"],
                title=r["title"],
                defaults=r
            )

        self.stdout.write(self.style.SUCCESS("Successfully seeded Art Market Faridabad catalog and reviews!"))
