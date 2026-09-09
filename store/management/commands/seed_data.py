from django.core.management.base import BaseCommand
from store.models import Category, Product, Review

class Command(BaseCommand):
    help = 'Seeds authentic inventory from @artmarketfaridabad (Artificial Plants, Planters, Wall Art, Antiques)'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding verified @artmarketfaridabad catalog...")

        # 1. Categories
        categories_data = [
            {
                "name": "Artificial Plants & Trees",
                "description": "Premium real-touch Monstera deliciosa, 5.5ft Fiddle Leaf Figs, Areca Palms, and Japanese Bonsai trees.",
                "image_url": "https://images.unsplash.com/photo-1545241047-6083a3684587?auto=format&fit=crop&w=800&q=80",
                "icon": "fa-leaf"
            },
            {
                "name": "Ceramic Pots & Designer Planters",
                "description": "Nordic face sculpted planters, donut vases, ribbed ceramic pots, and elevated metal floor stands.",
                "image_url": "https://images.unsplash.com/photo-1509423350716-97f9360b4e09?auto=format&fit=crop&w=800&q=80",
                "icon": "fa-wine-bottle"
            },
            {
                "name": "Antique Brass & Heritage Decor",
                "description": "Authentic heavy brass urulis, traditional hanging peacock diyas, and museum-finish brass idols.",
                "image_url": "https://images.unsplash.com/photo-1606744888344-498238f01777?auto=format&fit=crop&w=800&q=80",
                "icon": "fa-gem"
            },
            {
                "name": "Vintage Clocks & Water Fountains",
                "description": "Double-sided railway corridor wall clocks, tabletop zen waterfall fountains, and antique gramophones.",
                "image_url": "https://images.unsplash.com/photo-1563861826100-9cb868fdbe1c?auto=format&fit=crop&w=800&q=80",
                "icon": "fa-clock"
            },
            {
                "name": "Custom Canvas Art & Wall Decor",
                "description": "Textured 3D acrylic paintings, serene Buddha canvas art, and hand-carved decorative wall panels.",
                "image_url": "https://images.unsplash.com/photo-1579783902614-a3fb3927b675?auto=format&fit=crop&w=800&q=80",
                "icon": "fa-palette"
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

        # 2. Specific Real-Life Products from Art Market Faridabad
        products_data = [
            # Artificial Plants
            {
                "name": "4.5ft Real-Touch Artificial Monstera Deliciosa Tree",
                "category": cat_objs["Artificial Plants & Trees"],
                "sku": "AMF-MON-101",
                "original_price": 4499.00,
                "price": 2999.00,
                "short_description": "Signature split-leaf swiss cheese plant with textured stems in modern nursery pot.",
                "description": "As featured on our @artmarketfaridabad Instagram! High-density Real-Touch Monstera with realistic aerial roots and broad split leaves. Perfect for corners, balconies, and living rooms. Zero maintenance, no yellowing leaves.",
                "material": "Polyurethane Real-Touch Silk & Weighted Base",
                "dimensions": "54in Height (4.5 Feet)",
                "weight": "3.8 kg",
                "room_type": "living_room",
                "stock": 18,
                "image_url": "https://images.unsplash.com/photo-1614594975525-e45190c55d0b?auto=format&fit=crop&w=800&q=80",
                "is_featured": True,
                "is_bestseller": True,
                "is_new_arrival": False,
                "rating": 5.0,
                "reviews_count": 48
            },
            {
                "name": "5.5ft Luxury Artificial Fiddle Leaf Fig Tree (Multi-Stem)",
                "category": cat_objs["Artificial Plants & Trees"],
                "sku": "AMF-FID-102",
                "original_price": 5499.00,
                "price": 3799.00,
                "short_description": "Large violin-shaped textured foliage with natural wooden stem.",
                "description": "The most popular statement tree in modern luxury interior design. Features 42 large deep-green leaves with subtle veining. Shipped securely in heavy shockproof packaging from our Sector 87-88 Faridabad store.",
                "material": "Botanical Silk Polymers & Hardwood Trunk",
                "dimensions": "66in Height (5.5 Feet)",
                "weight": "4.6 kg",
                "room_type": "living_room",
                "stock": 14,
                "image_url": "https://images.unsplash.com/photo-1545241047-6083a3684587?auto=format&fit=crop&w=800&q=80",
                "is_featured": True,
                "is_bestseller": True,
                "is_new_arrival": False,
                "rating": 4.9,
                "reviews_count": 62
            },
            {
                "name": "Japanese Zen Evergreen Bonsai in Ceramic Dish",
                "category": cat_objs["Artificial Plants & Trees"],
                "sku": "AMF-BON-103",
                "original_price": 2899.00,
                "price": 1899.00,
                "short_description": "Curved rustic trunk tabletop bonsai with preserved moss bed.",
                "description": "Handcrafted miniature bonsai tree with authentic bark texture. Designed for study tables, executive desks, and coffee tables. Zero shedding and evergreen vibrant appearance.",
                "material": "High-Grade Polymers & Glazed Ceramic Dish",
                "dimensions": "15in Height x 16in Width",
                "weight": "1.9 kg",
                "room_type": "office",
                "stock": 25,
                "image_url": "https://images.unsplash.com/photo-1512428559087-560fa5ceab42?auto=format&fit=crop&w=800&q=80",
                "is_featured": True,
                "is_bestseller": True,
                "is_new_arrival": False,
                "rating": 4.9,
                "reviews_count": 39
            },
            {
                "name": "5ft Tropical Areca Palm Tree with Weighted Pot",
                "category": cat_objs["Artificial Plants & Trees"],
                "sku": "AMF-PLM-104",
                "original_price": 4200.00,
                "price": 2799.00,
                "short_description": "Cascading lush tropical feather palm fronds for indoor and covered balconies.",
                "description": "Dense tropical palm fronds with multi-stem base. Instantly brings resort-style relaxation to your home. Dusts off easily with a soft cloth.",
                "material": "UV-Stabilized Silk Touch Polymer",
                "dimensions": "60in Height (5 Feet)",
                "weight": "3.9 kg",
                "room_type": "balcony",
                "stock": 16,
                "image_url": "https://images.unsplash.com/photo-1485955900006-10f4d324d411?auto=format&fit=crop&w=800&q=80",
                "is_featured": False,
                "is_bestseller": True,
                "is_new_arrival": False,
                "rating": 4.8,
                "reviews_count": 31
            },
            {
                "name": "Vertical Garden Green Wall Artificial Foliage Panel (50x50 cm)",
                "category": cat_objs["Artificial Plants & Trees"],
                "sku": "AMF-WLL-105",
                "original_price": 1299.00,
                "price": 799.00,
                "short_description": "Interlocking dense boxwood & fern wall grid for accent walls and balcony partitions.",
                "description": "Create instant privacy and breathtaking green walls on your balcony, living room backdrop, or cafe. Easy snap-lock grid system.",
                "material": "Heavy-Duty Weather-Proof Flexible Polymer",
                "dimensions": "50cm x 50cm Panel",
                "weight": "0.7 kg",
                "room_type": "balcony",
                "stock": 60,
                "image_url": "https://images.unsplash.com/photo-1517196084881-6494535bd93f?auto=format&fit=crop&w=800&q=80",
                "is_featured": False,
                "is_bestseller": False,
                "is_new_arrival": True,
                "rating": 4.7,
                "reviews_count": 22
            },

            # Planters & Pots
            {
                "name": "Nordic Sculpted Face Head Ceramic Planter Pot",
                "category": cat_objs["Ceramic Pots & Designer Planters"],
                "sku": "AMF-POT-106",
                "original_price": 1899.00,
                "price": 1199.00,
                "short_description": "Matte finish abstract human sculpture pot for string of pearls and succulents.",
                "description": "Trending modern ceramic art piece that doubles as a plant holder. Looks stunning on bookshelf consoles and work desks. Matte finish with smooth edges.",
                "material": "High-Fired Matte Glazed Ceramic",
                "dimensions": "9in Height x 6.5in Width",
                "weight": "1.3 kg",
                "room_type": "living_room",
                "stock": 20,
                "image_url": "https://images.unsplash.com/photo-1520412099551-62b6bafeb5bb?auto=format&fit=crop&w=800&q=80",
                "is_featured": True,
                "is_bestseller": True,
                "is_new_arrival": False,
                "rating": 4.9,
                "reviews_count": 27
            },
            {
                "name": "Set of 2 Hammered Metal Floor Planters with Elevated Tripod",
                "category": cat_objs["Ceramic Pots & Designer Planters"],
                "sku": "AMF-POT-107",
                "original_price": 3899.00,
                "price": 2499.00,
                "short_description": "Modern mid-century metal pots on sturdy matte black iron stands.",
                "description": "Elevate your indoor trees and monsteras with sleek metallic finish floor planters. Electroplated rust-free iron designed for durability.",
                "material": "Electroplated Iron & Powder-Coated Stand",
                "dimensions": "Large: 22in H, Medium: 18in H",
                "weight": "3.1 kg (Set)",
                "room_type": "living_room",
                "stock": 15,
                "image_url": "https://images.unsplash.com/photo-1509423350716-97f9360b4e09?auto=format&fit=crop&w=800&q=80",
                "is_featured": True,
                "is_bestseller": True,
                "is_new_arrival": False,
                "rating": 4.9,
                "reviews_count": 44
            },

            # Antiques & Decor
            {
                "name": "Heritage Solid Brass Uruli with Peacocks & Diya Stand",
                "category": cat_objs["Antique Brass & Heritage Decor"],
                "sku": "AMF-BRS-108",
                "original_price": 5899.00,
                "price": 3899.00,
                "short_description": "Traditional heavy brass uruli ideal for floating flowers and tea lights at entrances.",
                "description": "Authentic lost-wax cast solid brass uruli featuring intricate peacock motifs. Perfect for festive celebrations, mandir entrances, and luxury foyer decor.",
                "material": "100% Solid Brass with Antique Patina",
                "dimensions": "14in Diameter x 7in Height",
                "weight": "4.4 kg",
                "room_type": "mandir",
                "stock": 12,
                "image_url": "https://images.unsplash.com/photo-1606744888344-498238f01777?auto=format&fit=crop&w=800&q=80",
                "is_featured": True,
                "is_bestseller": True,
                "is_new_arrival": False,
                "rating": 5.0,
                "reviews_count": 53
            },
            {
                "name": "Vintage Victorian Double-Sided Railway Station Wall Clock",
                "category": cat_objs["Vintage Clocks & Water Fountains"],
                "sku": "AMF-CLK-109",
                "original_price": 4499.00,
                "price": 2999.00,
                "short_description": "Classic wrought iron corridor clock with 360-degree dual dials and Roman numerals.",
                "description": "Colonial railway station clock with silent sweep movement. Mounted on an ornate wrought iron wall bracket. A timeless focal point for hallways and living rooms.",
                "material": "Wrought Iron & Antique Bronze Bezel",
                "dimensions": "16in Dial x 18in Bracket Height",
                "weight": "2.9 kg",
                "room_type": "living_room",
                "stock": 9,
                "image_url": "https://images.unsplash.com/photo-1563861826100-9cb868fdbe1c?auto=format&fit=crop&w=800&q=80",
                "is_featured": True,
                "is_bestseller": True,
                "is_new_arrival": False,
                "rating": 4.8,
                "reviews_count": 35
            },
            {
                "name": "Antique Brass 7-Tier Hanging Peacock Temple Diya",
                "category": cat_objs["Antique Brass & Heritage Decor"],
                "sku": "AMF-BRS-110",
                "original_price": 4299.00,
                "price": 2999.00,
                "short_description": "South Indian temple style hanging oil lamp with long link chain.",
                "description": "Heavy yellow brass hanging lamp with deep oil wicks. Brings divine auspicious energy to home pooja rooms and festive decor.",
                "material": "Pure Brass with Solid Brass Chain",
                "dimensions": "10in Diya Diameter + 24in Chain",
                "weight": "3.2 kg",
                "room_type": "mandir",
                "stock": 10,
                "image_url": "https://images.unsplash.com/photo-1606744888344-498238f01777?auto=format&fit=crop&w=800&q=80",
                "is_featured": False,
                "is_bestseller": False,
                "is_new_arrival": True,
                "rating": 5.0,
                "reviews_count": 18
            },
            {
                "name": "Textured 3D Modern Abstract Acrylic Canvas Wall Painting",
                "category": cat_objs["Custom Canvas Art & Wall Decor"],
                "sku": "AMF-ART-111",
                "original_price": 6999.00,
                "price": 4500.00,
                "short_description": "Handmade textured knife work canvas painting with floating floater frame.",
                "description": "Custom wall art by our Faridabad studio artists. Features rich 3D tactile knife textures and calming neutral tones. Stretched and framed ready to hang.",
                "material": "100% Cotton Canvas, Heavy Texture Acrylic, Teak Floater Frame",
                "dimensions": "36in Height x 24in Width",
                "weight": "3.5 kg",
                "room_type": "living_room",
                "stock": 7,
                "image_url": "https://images.unsplash.com/photo-1579783902614-a3fb3927b675?auto=format&fit=crop&w=800&q=80",
                "is_featured": True,
                "is_bestseller": False,
                "is_new_arrival": True,
                "rating": 4.9,
                "reviews_count": 15
            },
            {
                "name": "Indoor Zen Meditation Tabletop Rock Waterfall Fountain",
                "category": cat_objs["Vintage Clocks & Water Fountains"],
                "sku": "AMF-FNT-112",
                "original_price": 3499.00,
                "price": 2299.00,
                "short_description": "Soothing cascading water stream with built-in LED warm illumination and silent pump.",
                "description": "Brings the tranquil sound of flowing water and positive Vastu energy into living spaces, balconies, and office receptions.",
                "material": "Durable Lightweight Polyresin with Submersible Pump",
                "dimensions": "14in Height x 10in Base",
                "weight": "2.2 kg",
                "room_type": "living_room",
                "stock": 12,
                "image_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=800&q=80",
                "is_featured": False,
                "is_bestseller": False,
                "is_new_arrival": True,
                "rating": 4.8,
                "reviews_count": 21
            }
        ]

        for p in products_data:
            Product.objects.update_or_create(
                sku=p["sku"],
                defaults=p
            )

        # 3. Reviews matching real Faridabad local customers
        reviews_data = [
            {
                "name": "Neha Sharma",
                "city": "Sector 88, Faridabad",
                "rating": 5,
                "title": "Best home decor shop in Greater Faridabad!",
                "comment": "Found them on Instagram (@artmarketfaridabad) and visited their Sector 87-88 store near Barfiwala. Bought the 4.5ft Monstera and face planter. The leaf quality is outstanding, looks 100% real!",
                "product_name": "Artificial Monstera Deliciosa & Face Planter",
                "is_verified": True
            },
            {
                "name": "Vikas Chawla",
                "city": "Sector 14, Faridabad",
                "rating": 5,
                "title": "Ordered on WhatsApp, got home delivery in 2 hours",
                "comment": "Very responsive on WhatsApp. The brass uruli with peacock stand came in safe shockproof packaging. Will definitely visit the showroom for more items.",
                "product_name": "Heritage Brass Uruli",
                "is_verified": True
            },
            {
                "name": "Ritu Khattar",
                "city": "Neharpar / BPTP, Faridabad",
                "rating": 5,
                "title": "Transformed our living room aesthetic",
                "comment": "The Fiddle Leaf Fig tree and textured canvas painting look like they were bought from a luxury Delhi boutique at half the price. Highly recommended!",
                "product_name": "5.5ft Fiddle Leaf Fig Tree",
                "is_verified": True
            }
        ]

        for r in reviews_data:
            Review.objects.get_or_create(
                name=r["name"],
                title=r["title"],
                defaults=r
            )

        self.stdout.write(self.style.SUCCESS("Successfully seeded real @artmarketfaridabad inventory!"))
