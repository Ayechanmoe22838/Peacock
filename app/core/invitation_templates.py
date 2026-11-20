"""
Official Peacock Wedding Digital Invitation Templates
Maps template designs to real card assets extracted from Card.zip
"""

INVITATION_TEMPLATES = [
    {
        "id": "royal_rose",
        "name": "Royal Rose & Baroque Gold",
        "description": "Opulent rose gold borders with classical Burmese scrollwork and ornate floral crests.",
        "image": "/static/images/cards/card_01_07aceb5af207c5980c832d1484ac0f8a.jpg"
    },
    {
        "id": "classic_gold",
        "name": "Classic Champagne Gold Crest",
        "description": "Timeless champagne gold foil typography with elegant royal monogram emblem.",
        "image": "/static/images/cards/card_02_15c048f959ed1906e9127aa1afe2e814.jpg"
    },
    {
        "id": "sage_elegance",
        "name": "Emerald Garden Botanical",
        "description": "Delicate watercolor olive and eucalyptus leaves with warm ivory paper texture.",
        "image": "/static/images/cards/card_03_1f0f0f93bb90d6fc361a5aa4270c1017.jpg"
    },
    {
        "id": "modern_minimal",
        "name": "Modern Minimalist Ivory",
        "description": "Ultra-clean serif typography on crisp ivory linen cardstock.",
        "image": "/static/images/cards/card_04_35e5f665fa8a981ada0116e0df2a9df4.jpg"
    },
    {
        "id": "burgundy_luxury",
        "name": "Burgundy Wine & Golden Arch",
        "description": "Rich burgundy background crowned with architectural geometric golden arches.",
        "image": "/static/images/cards/card_05_41b3172266ba0258b3df1061c5284042.jpg"
    },
    {
        "id": "peacock_sapphire",
        "name": "Royal Peacock Sapphire & Gold",
        "description": "Deep peacock sapphire tones accented with feather filigree and gold shimmer.",
        "image": "/static/images/cards/card_06_7349e305c62bc06ec54cfd206cc18503.jpg"
    },
    {
        "id": "celestial_stars",
        "name": "Celestial Night & Golden Constellations",
        "description": "Midnight blue backdrop speckled with golden stardust and celestial constellations.",
        "image": "/static/images/cards/card_07_7f2402db52c04dae211c030a1ba8d575.jpg"
    },
    {
        "id": "vintage_lace",
        "name": "Vintage Lace & Golden Filigree",
        "description": "Intricate French lace patterns with shimmering gold embossed borders.",
        "image": "/static/images/cards/card_08_8359a6652951c3637d658d15fe59532f.jpg"
    },
    {
        "id": "floral_blush",
        "name": "Blush Blossom Romance",
        "description": "Soft peony and cherry blossom watercolor petals embracing graceful cursive calligraphy.",
        "image": "/static/images/cards/card_09_954b9742fa9f0af3f21fc2cdbeaf7841.jpg"
    },
    {
        "id": "imperial_brocade",
        "name": "Imperial Gold Brocade",
        "description": "Inspired by royal Mandalay court fabrics with raised golden brocade motifs.",
        "image": "/static/images/cards/card_10_ba97c9af8165e52e7eb29a8797b38f98.jpg"
    },
    {
        "id": "garden_eucalyptus",
        "name": "Garden Eucalyptus & Glasshouse",
        "description": "Lush greenery frame tailored for botanical garden and glasshouse ceremonies.",
        "image": "/static/images/cards/card_11_c8cd0809373831d1138a8cd1e5db4daa.jpg"
    },
    {
        "id": "monogram_crest",
        "name": "Regal Monogram Royal Crest",
        "description": "Distinguished coat of arms with custom initials set in burnished antique gold.",
        "image": "/static/images/cards/card_12_db37a1edf166c67b0776c108ad31aae1.jpg"
    },
    {
        "id": "watercolour_sunset",
        "name": "Watercolour Sunset Serenade",
        "description": "Warm sunset gradient shades reminiscent of tranquil Inle Lake evening nuptials.",
        "image": "/static/images/cards/card_13_dc00a627cd0304335a978ec9caaab01d.jpg"
    }
]

def get_template_image(template_id: str) -> str:
    for t in INVITATION_TEMPLATES:
        if t["id"] == template_id:
            return t["image"]
    return INVITATION_TEMPLATES[0]["image"]
