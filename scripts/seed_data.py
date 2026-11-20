import sys
from pathlib import Path
from datetime import datetime, date, time, timedelta
from decimal import Decimal

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.core.database import SessionLocal, engine, Base
from app.core.security import get_password_hash, generate_shareable_token
import app.models as models

def seed():
    db = SessionLocal()
    try:
        # Check if already seeded
        if db.query(models.User).filter_by(email="admin@peacock.com").first():
            print("Database already contains seed data.")
            return

        print("Seeding database with realistic wedding data...")

        # 1. Admin User
        admin = models.User(
            full_name="Peacock Administrator",
            email="admin@peacock.com",
            phone="09450012345",
            password_hash=get_password_hash("AdminPassword123!"),
            address="Peacock Tower, No. 12 Bogyoke Road, Yangon",
            role="admin",
            is_active=True
        )
        db.add(admin)

        # 2. Customers
        customer1 = models.User(
            full_name="Cherry",
            email="customer@peacock.com",
            phone="09790098765",
            password_hash=get_password_hash("CustomerPassword123!"),
            address="Inya Road, Bahan Township, Yangon",
            role="customer",
            is_active=True
        )
        customer2 = models.User(
            full_name="Thura Aung",
            email="thura@gmail.com",
            phone="09971234567",
            password_hash=get_password_hash("CustomerPassword123!"),
            address="Chanayethazan Township, Mandalay",
            role="customer",
            is_active=True
        )
        customer3 = models.User(
            full_name="May Thu Zin",
            email="maythu@gmail.com",
            phone="09250112233",
            password_hash=get_password_hash("CustomerPassword123!"),
            address="Pyay Road, Kamayut Township, Yangon",
            role="customer",
            is_active=True
        )
        db.add_all([customer1, customer2, customer3])
        db.flush()

        # 3. Venues
        venue1 = models.Venue(
            venue_name="The Grand Peacock Ballroom",
            description="Our premier flagship banquet ballroom featuring grand Austrian crystal chandeliers, opulent Champagne Gold finishes, and state-of-the-art audiovisual systems.",
            address="No. 88 University Avenue Road, Bahan",
            city="Yangon",
            capacity=600,
            base_price=Decimal("3500000.00"),
            facilities="Air Conditioning, Grand Crystal Chandeliers, Bridal Suite, Grand Stage, Valet Parking, Backup Generator, VIP Holding Room",
            status="active",
            is_active=True
        )
        venue2 = models.Venue(
            venue_name="Inle Serene Lakeside Garden",
            description="An ethereal outdoor and glasshouse garden sanctuary perched on the tranquil shores of Inle Lake, perfect for dreamy sunset ceremonies and romantic cloud walks.",
            address="Nyaung Shwe Lakefront District",
            city="Taunggyi / Inle",
            capacity=350,
            base_price=Decimal("2800000.00"),
            facilities="Scenic Lake View, Outdoor Floral Gazebo, Glasshouse Marquee, Bridal Dressing Lounge, Drone Zone, Ambient Acoustic Sound System",
            status="active",
            is_active=True
        )
        venue3 = models.Venue(
            venue_name="Kandawgyi Royal Pavilion",
            description="A majestic heritage pavilion overlooking the golden reflections of the Shwedagon Pagoda, blending traditional royal Burmese architecture with modern luxury.",
            address="Kandawgyi Nature Park, Mingalar Taung Nyunt",
            city="Yangon",
            capacity=450,
            base_price=Decimal("3000000.00"),
            facilities="Waterfront Deck, Shwedagon Pagoda View, Romantic Illumination, VIP Dining Suite, Dedicated Service Staff, On-site Kitchen",
            status="active",
            is_active=True
        )
        venue4 = models.Venue(
            venue_name="Mandalay Heritage Palace Court",
            description="Exquisite golden teak architecture with sweeping open-air courtyards, ideal for regal traditional ceremonies and high-capacity celebratory banquets.",
            address="73rd Street, Near Mandalay Hill",
            city="Mandalay",
            capacity=500,
            base_price=Decimal("2500000.00"),
            facilities="Traditional Teak Architecture, Royal Aisle, Heritage Photo Booth, Ample Parking, Dedicated Banquet Kitchen",
            status="active",
            is_active=True
        )
        db.add_all([venue1, venue2, venue3, venue4])
        db.flush()

        # Venue Images
        v1_img1 = models.VenueImage(venue_id=venue1.venue_id, image_url="/static/images/venues/hall_01_2dbec22580a0f12882132969d4819f84.jpg", is_primary=True, caption="Main Reception Stage & Loveseat")
        v2_img1 = models.VenueImage(venue_id=venue2.venue_id, image_url="/static/images/venues/hall_02_38ac43b6f5f5d2aa2f5e87ce570fbcd8.jpg", is_primary=True, caption="Lakeside Wedding Ceremony Walkway")
        v3_img1 = models.VenueImage(venue_id=venue3.venue_id, image_url="/static/images/venues/hall_03_65d117f1c0cd9228ad361fa00d35aa5f.jpg", is_primary=True, caption="Royal Pavilion Grand Hall")
        v4_img1 = models.VenueImage(venue_id=venue4.venue_id, image_url="/static/images/venues/hall_04_79cdec21d90259ae2266d3317e716791.jpg", is_primary=True, caption="Teak Heritage Courtyard")
        v1_img2 = models.VenueImage(venue_id=venue1.venue_id, image_url="/static/images/venues/hall_05_8097a228f71513036509555f47261de2.jpg", is_primary=False, caption="Grand Ballroom Ceiling & Crystal Chandeliers")
        v1_img3 = models.VenueImage(venue_id=venue1.venue_id, image_url="/static/images/venues/hall_06_a417b7d31c0aa94e7465cc5ac5461af6.jpg", is_primary=False, caption="VIP Banquet Table Layout")
        v2_img2 = models.VenueImage(venue_id=venue2.venue_id, image_url="/static/images/venues/hall_07_d295a2e366e6c9fec9f020135f045168.jpg", is_primary=False, caption="Garden Twilight Floral Walkway")
        v3_img2 = models.VenueImage(venue_id=venue3.venue_id, image_url="/static/images/venues/hall_08_f03844f1b439ca32515ea42777fd52c0.jpg", is_primary=False, caption="Royal Pavilion Stage Lighting")
        db.add_all([v1_img1, v2_img1, v3_img1, v4_img1, v1_img2, v1_img3, v2_img2, v3_img2])

        # 4. Wedding Packages
        pkg1 = models.Package(
            package_name="Imperial Gold Royal Package",
            description="A comprehensive luxury experience designed for grand celebrations. Includes full floral stage styling, multi-tier wedding cake, live orchestra, and VIP services.",
            price=Decimal("4800000.00"),
            status="active",
            is_active=True,
            image_url="/static/images/venues/hall_05_8097a228f71513036509555f47261de2.jpg"
        )
        pkg2 = models.Package(
            package_name="Sapphire Romance Garden Package",
            description="A romantic outdoor and garden package featuring fresh floral arches, acoustic musical ensemble, welcome cocktail bar, and personalized styling.",
            price=Decimal("3200000.00"),
            status="active",
            is_active=True,
            image_url="/static/images/venues/hall_06_a417b7d31c0aa94e7465cc5ac5461af6.jpg"
        )
        pkg3 = models.Package(
            package_name="Classic Ivory Elegance Package",
            description="A sophisticated package focusing on timeless aesthetics, professional sound & lighting, customized reception backdrops, and dedicated coordination.",
            price=Decimal("2200000.00"),
            status="active",
            is_active=True,
            image_url="/static/images/venues/hall_07_d295a2e366e6c9fec9f020135f045168.jpg"
        )
        db.add_all([pkg1, pkg2, pkg3])
        db.flush()

        # Package Services
        pkg1_services = [
            "Grand Floral Stage & Arch Decoration with Custom Loveseat",
            "Master of Ceremonies (MC) for Ceremony & Reception",
            "Live Classical String Quartet & Acoustic Ensemble",
            "Complimentary 3-Tier Luxury Wedding Cake & Champagne Tower",
            "Digital Invitation & Seating Planner Suite with RSVP Tracking",
            "Full Day Concert-Grade Sound & Intelligent Lighting System"
        ]
        for s in pkg1_services:
            db.add(models.PackageService(package_id=pkg1.package_id, service_name=s, is_included=True))

        pkg2_services = [
            "Lakeside Floral Aisle, Walkway & Entrance Gazebo",
            "Acoustic Duo Performance (Guitar & Violin)",
            "Bridal Makeup & Hair Styling Assistant On-site",
            "Welcome Drink & Fresh Mocktail Reception Bar",
            "Digital Guest RSVP Management & Floor Seating Planner"
        ]
        for s in pkg2_services:
            db.add(models.PackageService(package_id=pkg2.package_id, service_name=s, is_included=True))

        pkg3_services = [
            "Ivory & Gold Elegant Stage Backdrop & Chair Sashes",
            "Professional Sound System & Wireless Microphones",
            "Guest Welcome Reception Table & Guestbook Setup",
            "Dedicated Event Timeline & Coordination Assistant"
        ]
        for s in pkg3_services:
            db.add(models.PackageService(package_id=pkg3.package_id, service_name=s, is_included=True))

        # 5. Vendors
        vendor_data = [
            ("Aura Wedding Photography & Films", "Photography", "Award-winning fine-art wedding photography team capturing candid emotions and timeless royal portraits.", "Ko Aung Kyaw", "095123456", "aura@peacockweddings.com", Decimal("1200000.00"), "/static/images/hero_wedding_couple.jpg"),
            ("CineLove Cinematic Videography", "Videography", "Cinematic 4K drone coverage, same-day edit highlights, and complete documentary wedding films.", "Daw Htet Htet", "095234567", "cinelove@peacockweddings.com", Decimal("1500000.00"), "/static/images/hero_wedding_couple.jpg"),
            ("Royal Velvet Stage & Decor", "Decoration", "Luxury wedding stage stylists specializing in bespoke floral installations, chandeliers, and royal drapes.", "U Soe Myint", "095456789", "royalvelvet@peacockweddings.com", Decimal("1400000.00"), "/static/images/luxury_ballroom.jpg"),
            ("Blossom & Petals Floral Atelier", "Florist", "Imported fresh roses, lilies, and customized bridal bouquets, corsages, and centerpiece arrangements.", "Ma Khin Thida", "095345678", "blossom@peacockweddings.com", Decimal("850000.00"), "/static/images/luxury_ballroom.jpg"),
            ("Glamour By May Wedding Makeup", "Makeup Artist", "Celebrity makeup artist and hair designer dedicated to creating radiant, long-lasting bridal looks.", "May Zin", "095567890", "glamourby@peacockweddings.com", Decimal("450000.00"), "/static/images/hero_wedding_couple.jpg"),
            ("Harmony Strings Classical Ensemble", "Entertainment", "Symphonic 4-piece string quartet playing romantic classics, pop ballads, and traditional wedding marches.", "Ko Nay Lin", "095678901", "harmony@peacockweddings.com", Decimal("750000.00"), "/static/images/luxury_ballroom.jpg"),
            ("DJ Zenith Wedding Beats", "Music/DJ", "Professional wedding DJ with high-energy party sets, custom playlists, and wireless party lighting.", "DJ Zenith", "095789012", "zenith@peacockweddings.com", Decimal("600000.00"), "/static/images/luxury_ballroom.jpg"),
            ("U Kyaw Swar – Master of Ceremonies", "Master of Ceremonies", "Bilingual, charismatic MC experienced in hosting grand VIP banquets and traditional nuptials.", "U Kyaw Swar", "095890123", "kyawswar@peacockweddings.com", Decimal("500000.00"), "/static/images/hero_wedding_couple.jpg")
        ]
        vendors = []
        for v in vendor_data:
            vend = models.Vendor(
                vendor_name=v[0], category=v[1], description=v[2], contact_name=v[3],
                phone=v[4], email=v[5], price=v[6], image_url=v[7], is_active=True
            )
            db.add(vend)
            vendors.append(vend)
        db.flush()

        # 6. Menus (Catering - All authentic Myanmar and International menus)
        menus_data = [
            ("Traditional Myanmar Grand Feast", "Traditional Myanmar", "Authentic banana-leaf presentation with fragrant steamed rice, golden river prawns, tender beef curry, fried duck, boiled eggs, fresh salad relishes, and side soups.", Decimal("25000.00"), "/static/images/menus/myanmar/mm_food_01_4faac189e641956510656f911aeaa905.jpg"),
            ("Shwe Yin Aye Royal Dessert", "Dessert", "Chilled traditional coconut cream dessert with pandan jelly, sago, sweet bread, and sticky rice.", Decimal("4500.00"), "/static/images/menus/myanmar/mm_food_02_833f0484d0b473dd67cd9f28211fb437.jpg"),
            ("Fresh Passionfruit & Lychee Mocktail", "Beverage", "Refreshing welcome mocktail infused with natural fruit puree, mint leaves, and sparkling soda.", Decimal("3500.00"), "/static/images/menus/myanmar/mm_food_03_FB_IMG_1795003259437.jpg"),
            ("Traditional Burmese Mohinga & Crispy Fritter Station", "Traditional Myanmar", "Aromatic slow-simmered fish broth with lemongrass, rice vermicelli, crispy golden pe-gyaw (bean fritters), boiled eggs, and fresh coriander.", Decimal("5500.00"), "/static/images/menus/myanmar/mm_food_04_FB_IMG_1795003393297.jpg"),
            ("Royal Golden Coconut Sticky Rice & Kyauk Kyaw Platter", "Dessert", "Heritage wedding sweet spread with multi-layered coconut agar agar jelly, palm sugar sticky rice cakes, and roasted sesame.", Decimal("4000.00"), "/static/images/menus/myanmar/mm_food_05_FB_IMG_1795003498994.jpg"),
            ("Mandalay Style Meeshay & Braised Pork Ribs", "Traditional Myanmar", "Traditional rice noodles tossed in rich meat sauce, roasted chili oil, crushed garlic oil, spring onions, and braised pork ribs.", Decimal("8000.00"), "/static/images/menus/myanmar/mm_food_06_FB_IMG_1795004865322.jpg"),
            ("Shan Royal Khauk Swe & Crisp Tofu Live Buffet", "Traditional Myanmar", "Warm chicken curry noodles with Shan pickled greens, crisp Shan mountain tofu fritters, and fragrant chili paste.", Decimal("7000.00"), "/static/images/menus/myanmar/mm_food_07_Screenshot_20261118_182808_Google.jpg"),
            ("Borcelle Royal Indian Thali", "Main Course", "Palace-style dining with aromatic Dal Rice, buttery Paneer Makhani, Dum Aloo cooked in rich spiced gravy, warm naan, and accompaniments.", Decimal("18000.00"), "/static/images/menus/international/intl_food_01_501aed016a10a6cf5ecf0acc2dff0ff9.jpg"),
            ("Royal Kitchen Imperial Biryani", "Main Course", "Fragrant saffron Basmati dum biryani with marinated tender mutton or chicken, rich Dal Makhani, Butter Chicken, and cooling raita.", Decimal("22000.00"), "/static/images/menus/international/intl_food_02_657b6b0a195f00cec0faf6277b496340.jpg"),
            ("Gold Leaf Velvet Cupcake & Macaron Platter", "Dessert", "Assorted artisanal French macarons and gold-dusted red velvet mini cupcakes with cream cheese frosting.", Decimal("6000.00"), "/static/images/menus/international/intl_food_03_6f0c34b0238dd6ad040379ba6f618e24.jpg"),
            ("Continental Herb-Crusted Prime Beef & Glazed Salmon", "Main Course", "Slow-roasted rosemary Angus beef with red wine reduction, paired with Norwegian Atlantic salmon glazed in lemon butter sauce.", Decimal("32000.00"), "/static/images/menus/international/intl_food_04_c9e42259e7d0bfb37a41b6a64884162a.jpg"),
            ("Mediterranean Artisan Antipasto & Cheese Grazing Table", "Main Course", "Gourmet grazing table with Italian prosciutto, imported aged cheeses, Kalamata olives, artisan crackers, and fresh seasonal grapes.", Decimal("16000.00"), "/static/images/menus/international/intl_food_05_d97c163c8073413e68110b7886bf5dab.jpg")
        ]
        menus = []
        for m in menus_data:
            menu_obj = models.Menu(
                name=m[0], category=m[1], description=m[2], price_per_person=m[3], image_url=m[4], is_active=True
            )
            db.add(menu_obj)
            menus.append(menu_obj)
        db.flush()

        # 7. Sample Confirmed Booking for Customer 1 (Aye Chan Moe)
        target_date = date(2026, 12, 28)
        booking1 = models.Booking(
            booking_reference="BK-202611-001",
            customer_id=customer1.user_id,
            venue_id=venue1.venue_id,
            package_id=pkg1.package_id,
            event_date=target_date,
            start_time=time(17, 0),
            end_time=time(22, 0),
            guest_count=250,
            special_requirements="Bride requested champagne gold chair ribbons and an extra photo booth area near entrance.",
            venue_cost=Decimal("3500000.00"),
            package_cost=Decimal("4800000.00"),
            vendors_cost=Decimal("1200000.00"),  # Aura Photography
            catering_cost=Decimal("0.00"),
            total_cost=Decimal("9500000.00"),
            paid_amount=Decimal("5000000.00"),
            balance_amount=Decimal("4500000.00"),
            booking_status="Confirmed"
        )
        db.add(booking1)
        db.flush()

        # Add Booking Vendor
        db.add(models.BookingVendor(
            booking_id=booking1.booking_id,
            vendor_id=vendors[0].vendor_id,  # Photography
            price_agreed=Decimal("1200000.00"),
            notes="Full day photo shoot with 2 photographers"
        ))

        # Add Budget
        budget1 = models.Budget(
            booking_id=booking1.booking_id,
            total_budget=Decimal("15000000.00"),
            estimated_cost=Decimal("11000000.00"),
            actual_spent=Decimal("5000000.00"),
            remaining_budget=Decimal("10000000.00"),
            notes="Primary wedding budget tracked for reception and attire."
        )
        db.add(budget1)
        db.flush()

        # Add Budget Expenses
        exp1 = models.Expense(
            budget_id=budget1.budget_id,
            category="Venue",
            item_name="The Grand Peacock Ballroom Booking",
            estimated_cost=Decimal("3500000.00"),
            actual_cost=Decimal("3500000.00"),
            is_paid=True,
            payment_reference="PAY-202611-001"
        )
        exp2 = models.Expense(
            budget_id=budget1.budget_id,
            category="Package",
            item_name="Imperial Gold Royal Package",
            estimated_cost=Decimal("4800000.00"),
            actual_cost=Decimal("4800000.00"),
            is_paid=False
        )
        exp3 = models.Expense(
            budget_id=budget1.budget_id,
            category="Vendors",
            item_name="Aura Wedding Photography",
            estimated_cost=Decimal("1200000.00"),
            actual_cost=Decimal("1200000.00"),
            is_paid=False
        )
        db.add_all([exp1, exp2, exp3])

        # Add Payment (KBZPay deposit verified by Admin)
        payment1 = models.Payment(
            payment_reference="PAY-202611-001",
            booking_id=booking1.booking_id,
            amount=Decimal("5000000.00"),
            payment_method="KBZPay",
            transaction_reference="KPay-TXN-88492019482",
            receipt_image="/static/images/receipts/kpay_receipt_sample.jpg",
            payment_status="Verified",
            notes="Deposit payment transferred via KPay mobile app.",
            admin_notes="Payment receipt verified with KBZ Merchant account. Approved.",
            payment_date=datetime.utcnow() - timedelta(days=2),
            verified_by=admin.user_id,
            verified_at=datetime.utcnow() - timedelta(days=2, hours=1)
        )
        db.add(payment1)

        # Add Digital Invitation
        invitation1 = models.Invitation(
            booking_id=booking1.booking_id,
            template_name="royal_rose",
            custom_title="Aye Chan Moe & Min Thant",
            custom_message="Together with their families, Aye Chan Moe and Min Thant joyfully invite you to celebrate their wedding reception and join them in an evening of love, laughter, and lifelong memories.",
            wedding_date=target_date,
            start_time=time(17, 0),
            end_time=time(22, 0),
            venue_name="The Grand Peacock Ballroom",
            venue_address="No. 88 University Avenue Road, Bahan, Yangon",
            shareable_token="peacock-acm-minthant-2026",
            views_count=42
        )
        db.add(invitation1)

        # Add Reception Tables
        table1 = models.ReceptionTable(booking_id=booking1.booking_id, table_number=1, table_name="Table 1 - VIP Bride Family", capacity=10, notes="Front row left")
        table2 = models.ReceptionTable(booking_id=booking1.booking_id, table_number=2, table_name="Table 2 - VIP Groom Family", capacity=10, notes="Front row right")
        table3 = models.ReceptionTable(booking_id=booking1.booking_id, table_number=3, table_name="Table 3 - University Friends", capacity=10, notes="Center stage view")
        table4 = models.ReceptionTable(booking_id=booking1.booking_id, table_number=4, table_name="Table 4 - Colleagues", capacity=10, notes="Near garden terrace")
        db.add_all([table1, table2, table3, table4])
        db.flush()

        # Add Guests
        guests_info = [
            ("U Myint Thu", "09450099881", "myintthu@family.com", "Bride Family", "Accepted", "None", 1),
            ("Daw San San Nwe", "09450099882", "sansan@family.com", "Bride Family", "Accepted", "Vegetarian", 0),
            ("U Kyaw Min", "09450099883", "kyawmin@family.com", "Groom Family", "Accepted", "None", 1),
            ("Daw Ni Ni Win", "09450099884", "nini@family.com", "Groom Family", "Accepted", "None", 0),
            ("Ko Sithu Aung", "09781122334", "sithu@friends.com", "Close Friends", "Accepted", "No spicy food", 1),
            ("Ma Phyu Phyu Htwe", "09781122335", "phyu@friends.com", "Close Friends", "Accepted", "Halal", 0),
            ("Ko Zin Ko Ko", "09781122336", "zin@friends.com", "Colleagues", "Pending", "None", 0),
            ("Ma Hnin Nu Wai", "09781122337", "hnin@friends.com", "Colleagues", "Pending", "None", 0),
            ("Dr. Tin Maung", "09210099887", "tinmaung@vip.com", "VIP", "Accepted", "Diabetic menu", 1),
            ("Sayama Daw Khin May", "09210099888", "khinmay@vip.com", "VIP", "Accepted", "Vegetarian", 0),
        ]
        created_guests = []
        for g in guests_info:
            guest_obj = models.Guest(
                booking_id=booking1.booking_id,
                guest_name=g[0],
                phone=g[1],
                email=g[2],
                category=g[3],
                rsvp_status=g[4],
                dietary_requirements=g[5],
                plus_ones=g[6],
                invitation_token=generate_shareable_token()
            )
            db.add(guest_obj)
            created_guests.append(guest_obj)
        db.flush()

        # Add Seating Assignments
        db.add(models.SeatingAssignment(table_id=table1.table_id, guest_id=created_guests[0].guest_id, seat_number=1))
        db.add(models.SeatingAssignment(table_id=table1.table_id, guest_id=created_guests[1].guest_id, seat_number=2))
        db.add(models.SeatingAssignment(table_id=table2.table_id, guest_id=created_guests[2].guest_id, seat_number=1))
        db.add(models.SeatingAssignment(table_id=table2.table_id, guest_id=created_guests[3].guest_id, seat_number=2))
        db.add(models.SeatingAssignment(table_id=table3.table_id, guest_id=created_guests[4].guest_id, seat_number=1))
        db.add(models.SeatingAssignment(table_id=table3.table_id, guest_id=created_guests[5].guest_id, seat_number=2))
        db.add(models.SeatingAssignment(table_id=table1.table_id, guest_id=created_guests[8].guest_id, seat_number=3))
        db.add(models.SeatingAssignment(table_id=table1.table_id, guest_id=created_guests[9].guest_id, seat_number=4))

        # Add Event Schedule
        schedule_items = [
            ("Guest Arrival & Welcome Cocktails", time(17, 0), time(18, 0), "Guests arrive, receive mocktails, and sign the digital guestbook.", 1),
            ("Grand Entrance & Welcome Speech", time(18, 0), time(18, 45), "Grand entrance of the bride and groom accompanied by string ensemble.", 2),
            ("Ceremonial Blessing & Ring Exchange", time(18, 45), time(19, 30), "Parents blessings, exchange of vows and rings on the main stage.", 3),
            ("Royal Banquet Dinner & Live Performances", time(19, 30), time(20, 30), "Grand catering dinner service with classical music accompaniment.", 4),
            ("Wedding Cake Cutting & Champagne Toast", time(20, 30), time(21, 0), "3-Tier cake cutting, champagne tower toast with all guests.", 5),
            ("Bouquet Toss & Farewell Celebration", time(21, 0), time(22, 0), "Photography sessions, bridal bouquet toss, and heartfelt farewell.", 6),
        ]
        for it in schedule_items:
            db.add(models.EventSchedule(
                booking_id=booking1.booking_id,
                activity_name=it[0],
                start_time=it[1],
                end_time=it[2],
                description=it[3],
                order_index=it[4]
            ))

        # 8. Pending Booking for Customer 2 (Thura Aung) to test Admin approval flow
        booking2 = models.Booking(
            booking_reference="BK-202611-002",
            customer_id=customer2.user_id,
            venue_id=venue2.venue_id,
            package_id=pkg2.package_id,
            event_date=date(2027, 1, 15),
            start_time=time(16, 0),
            end_time=time(21, 0),
            guest_count=200,
            special_requirements="Requires outdoor drone photography clearance and traditional harpist.",
            venue_cost=Decimal("2800000.00"),
            package_cost=Decimal("3200000.00"),
            vendors_cost=Decimal("0.00"),
            catering_cost=Decimal("0.00"),
            total_cost=Decimal("6000000.00"),
            paid_amount=Decimal("0.00"),
            balance_amount=Decimal("6000000.00"),
            booking_status="Pending"
        )
        db.add(booking2)

        # 9. Completed Booking for Customer 3 (May Thu Zin) with Feedback to show on public Home page
        booking3 = models.Booking(
            booking_reference="BK-202610-003",
            customer_id=customer3.user_id,
            venue_id=venue3.venue_id,
            package_id=pkg3.package_id,
            event_date=date(2026, 10, 20),
            start_time=time(17, 0),
            end_time=time(22, 0),
            guest_count=300,
            special_requirements="Waterfront lighting and evening fireworks display.",
            venue_cost=Decimal("3000000.00"),
            package_cost=Decimal("2200000.00"),
            vendors_cost=Decimal("1200000.00"),
            catering_cost=Decimal("0.00"),
            total_cost=Decimal("6400000.00"),
            paid_amount=Decimal("6400000.00"),
            balance_amount=Decimal("0.00"),
            booking_status="Completed"
        )
        db.add(booking3)
        db.flush()

        feedback3 = models.Feedback(
            booking_id=booking3.booking_id,
            customer_id=customer3.user_id,
            rating=5,
            review_title="An Unforgettable Fairytale Wedding!",
            comments="Peacock made our wedding planning effortless! The Kandawgyi Royal Pavilion looked absolutely magical at sunset. The digital invitation system and seating planner saved us dozens of hours. Thank you so much for the exceptional service!",
            is_approved=True,
            admin_response="It was an absolute pleasure hosting your special celebration, May Thu Zin! We wish you and your partner a lifetime of happiness.",
            response_at=datetime.utcnow() - timedelta(days=20)
        )
        db.add(feedback3)

        # Notifications
        db.add(models.Notification(
            user_id=customer1.user_id,
            title="Booking Confirmed!",
            message="Your wedding booking BK-202611-001 at The Grand Peacock Ballroom is confirmed. Deposit payment of 5,000,000 MMK has been verified.",
            notification_type="booking",
            is_read=True,
            link_url="/customer/bookings"
        ))
        db.add(models.Notification(
            user_id=customer1.user_id,
            title="RSVP Milestone",
            message="Over 8 guests have responded to your digital wedding invitation! Check your Seating Planner to arrange tables.",
            notification_type="reminder",
            is_read=False,
            link_url="/customer/seating"
        ))
        db.add(models.Notification(
            user_id=admin.user_id,
            title="New Booking Request",
            message="Customer Thura Aung submitted a new booking request (BK-202611-002) for Inle Serene Lakeside Garden.",
            notification_type="booking",
            is_read=False,
            link_url="/admin/bookings"
        ))

        # Initial Audit Log
        db.add(models.AuditLog(
            user_id=admin.user_id,
            action="SYSTEM_INIT",
            entity_type="System",
            entity_id=None,
            details="Initial database seeded with realistic venues, packages, vendors, catering menus, and sample bookings.",
            ip_address="127.0.0.1"
        ))

        db.commit()
        print("Database seeded successfully with all initial records!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed()
